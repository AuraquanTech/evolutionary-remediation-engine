#!/usr/bin/env python3
"""
Production-grade GitHub PR collector for evolutionary remediation research.
Analyzes merge patterns from high-quality repositories.
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Generator
import os

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN not set. Set it in .env or export GITHUB_TOKEN='ghp_...'"
    )

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}",
    "User-Agent": "evolutionary-remediation-engine"
}

# Timeout for rate limit reset (seconds)
RATE_LIMIT_BUFFER = 5


@dataclass
class PRMetadata:
    """Complete metadata for a single PR."""
    repo: str
    owner: str
    pr_number: int
    title: str
    body: str
    created_at: str
    merged_at: str
    closed_at: str
    merge_time_hours: float
    author: str
    files_changed: int
    additions: int
    deletions: int
    comments: int
    review_comments: int
    commits: int
    labels: List[str]
    merged: bool
    is_security_related: bool
    has_revert: bool
    revert_time_hours: Optional[float]


class GitHubCollector:
    """Collect and analyze PRs from GitHub repositories."""

    def __init__(
        self,
        repositories: List[str],
        output_file: str = "data/raw_prs.jsonl",
        max_prs_per_repo: int = 100,
        min_merge_time_hours: float = 0.5
    ):
        """
        Initialize collector.
        
        Args:
            repositories: List of "owner/repo" strings
            output_file: Path to write JSONL output
            max_prs_per_repo: Maximum PRs to collect per repository
            min_merge_time_hours: Minimum merge time to include
        """
        self.repositories = repositories
        self.output_file = Path(output_file)
        self.max_prs_per_repo = max_prs_per_repo
        self.min_merge_time_hours = min_merge_time_hours
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.collected_count = 0
        self.skipped_count = 0

    def _handle_rate_limit(self, response: requests.Response):
        """Handle GitHub rate limiting."""
        if response.status_code == 403:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            now = time.time()
            wait_seconds = max(reset_time - now + RATE_LIMIT_BUFFER, 0)
            logger.warning(f"Rate limited. Waiting {wait_seconds:.0f} seconds...")
            time.sleep(wait_seconds)
            return True
        return False

    def _is_security_related(self, pr: dict) -> bool:
        """Detect if PR is security-related."""
        title_body = (pr.get('title', '') + ' ' + pr.get('body', '')).lower()
        labels = [l['name'].lower() for l in pr.get('labels', [])]
        
        security_keywords = {
            'security', 'vulnerability', 'cve', 'xss', 'sql injection',
            'csrf', 'secret', 'credential', 'auth', 'password',
            'encryption', 'hash', 'sensitive', 'vulnerability',
            'dependency', 'dependencies', 'npm', 'package',
            'deprecated', 'warning', 'critical', 'fix'
        }
        
        title_keywords = set(title_body.split()) & security_keywords
        label_keywords = any(
            any(keyword in label for keyword in security_keywords)
            for label in labels
        )
        
        return bool(title_keywords) or label_keywords or 'security' in labels

    def _detect_revert(self, repo: str, original_pr: dict) -> tuple[bool, Optional[float]]:
        """
        Detect if a PR was reverted by searching for related reverts.
        
        Returns:
            (was_reverted, revert_time_hours)
        """
        try:
            original_merged_at = datetime.fromisoformat(
                original_pr['merged_at'].replace('Z', '+00:00')
            )
            
            # Search for PRs that reference this one
            search_url = (
                f"{GITHUB_API_BASE}/search/issues"
                f"?q=repo:{repo}+type:pr+in:body+#{original_pr['number']}"
                f"&sort=created&order=desc"
            )
            
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            if self._handle_rate_limit(response):
                return self._detect_revert(repo, original_pr)
            
            if response.status_code != 200:
                return False, None
            
            items = response.json().get('items', [])
            for item in items:
                if 'revert' in item['title'].lower():
                    revert_merged_at = datetime.fromisoformat(
                        item['merged_at'].replace('Z', '+00:00')
                    )
                    if revert_merged_at > original_merged_at:
                        revert_hours = (
                            revert_merged_at - original_merged_at
                        ).total_seconds() / 3600
                        return True, revert_hours
            
            return False, None
        except Exception as e:
            logger.debug(f"Revert detection failed: {e}")
            return False, None

    def _get_pr_details(self, owner: str, repo: str, pr_number: int) -> Optional[PRMetadata]:
        """Fetch complete PR details from GitHub API."""
        try:
            pr_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}"
            response = requests.get(pr_url, headers=HEADERS, timeout=10)
            
            if self._handle_rate_limit(response):
                return self._get_pr_details(owner, repo, pr_number)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch {owner}/{repo}#{pr_number}")
                return None
            
            pr = response.json()
            
            # Skip if not merged
            if not pr.get('merged_at'):
                self.skipped_count += 1
                return None
            
            # Calculate merge time
            created = datetime.fromisoformat(
                pr['created_at'].replace('Z', '+00:00')
            )
            merged = datetime.fromisoformat(
                pr['merged_at'].replace('Z', '+00:00')
            )
            merge_time_hours = (merged - created).total_seconds() / 3600
            
            # Skip if below minimum threshold
            if merge_time_hours < self.min_merge_time_hours:
                self.skipped_count += 1
                return None
            
            # Check if security-related
            is_security = self._is_security_related(pr)
            
            # Detect revert
            was_reverted, revert_hours = self._detect_revert(f"{owner}/{repo}", pr)
            
            metadata = PRMetadata(
                repo=repo,
                owner=owner,
                pr_number=pr['number'],
                title=pr['title'],
                body=pr.get('body', ''),
                created_at=pr['created_at'],
                merged_at=pr['merged_at'],
                closed_at=pr.get('closed_at', ''),
                merge_time_hours=merge_time_hours,
                author=pr['user']['login'],
                files_changed=pr['changed_files'],
                additions=pr['additions'],
                deletions=pr['deletions'],
                comments=pr['comments'],
                review_comments=pr['review_comments'],
                commits=pr['commits'],
                labels=[label['name'] for label in pr.get('labels', [])],
                merged=pr['merged'],
                is_security_related=is_security,
                has_revert=was_reverted,
                revert_time_hours=revert_hours
            )
            
            self.collected_count += 1
            return metadata
            
        except Exception as e:
            logger.error(f"Error fetching PR details: {e}")
            return None

    def collect_prs(self, include_security_only: bool = True) -> Generator[PRMetadata, None, None]:
        """
        Collect PRs from all repositories.
        
        Args:
            include_security_only: Only include security-related PRs
            
        Yields:
            PRMetadata objects
        """
        with open(self.output_file, 'w') as f:
            for repo_spec in self.repositories:
                owner, repo = repo_spec.split('/')
                logger.info(f"Collecting from {owner}/{repo}")
                
                prs_collected = 0
                page = 1
                
                while prs_collected < self.max_prs_per_repo:
                    # Fetch PR list
                    list_url = (
                        f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
                        f"?state=closed&sort=created&direction=desc"
                        f"&page={page}&per_page=100"
                    )
                    
                    response = requests.get(list_url, headers=HEADERS, timeout=10)
                    
                    if self._handle_rate_limit(response):
                        continue
                    
                    if response.status_code != 200:
                        logger.warning(f"Failed to fetch PR list page {page}")
                        break
                    
                    prs = response.json()
                    if not prs:
                        break
                    
                    for pr in prs:
                        if prs_collected >= self.max_prs_per_repo:
                            break
                        
                        metadata = self._get_pr_details(owner, repo, pr['number'])
                        
                        if metadata is None:
                            continue
                        
                        if include_security_only and not metadata.is_security_related:
                            continue
                        
                        # Write to JSONL
                        f.write(json.dumps(asdict(metadata)) + '\n')
                        f.flush()
                        
                        yield metadata
                        prs_collected += 1
                        
                        # Rate limiting
                        time.sleep(0.5)
                    
                    page += 1
                
                logger.info(
                    f"Completed {owner}/{repo}: "
                    f"Collected={self.collected_count}, Skipped={self.skipped_count}"
                )

    def get_statistics(self) -> dict:
        """Calculate statistics from collected PRs."""
        merge_times = []
        security_count = 0
        revert_count = 0
        
        with open(self.output_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                merge_times.append(data['merge_time_hours'])
                if data['is_security_related']:
                    security_count += 1
                if data['has_revert']:
                    revert_count += 1
        
        if not merge_times:
            return {}
        
        merge_times.sort()
        
        return {
            'total_prs': len(merge_times),
            'security_prs': security_count,
            'security_percentage': (security_count / len(merge_times)) * 100,
            'median_merge_hours': merge_times[len(merge_times) // 2],
            'mean_merge_hours': sum(merge_times) / len(merge_times),
            'min_merge_hours': min(merge_times),
            'max_merge_hours': max(merge_times),
            'revert_count': revert_count,
            'revert_rate': (revert_count / len(merge_times)) * 100,
        }


if __name__ == "__main__":
    import sys
    
    # Research targets: high-quality open source with security focus
    TARGET_REPOS = [
        "eslint/eslint",  # ESLint - meta-tool (code quality)
        "prettier/prettier",  # Prettier - meta-tool (formatting)
        "typescript-eslint/typescript-eslint",  # TypeScript linting
        "nodejs/node",  # Node.js - core infrastructure
    ]
    
    collector = GitHubCollector(
        repositories=TARGET_REPOS,
        output_file="data/raw_prs.jsonl",
        max_prs_per_repo=100,  # 400 PRs total for demo
        min_merge_time_hours=0.5
    )
    
    logger.info("Starting PR collection...")
    count = 0
    for pr in collector.collect_prs(include_security_only=True):
        count += 1
        if count % 10 == 0:
            logger.info(f"Collected {count} PRs...")
    
    stats = collector.get_statistics()
    logger.info(f"\n=== Collection Statistics ===")
    logger.info(json.dumps(stats, indent=2))
    logger.info(f"\nData saved to: {collector.output_file}")