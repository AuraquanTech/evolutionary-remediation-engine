#!/usr/bin/env python3
"""Pattern extractor: Analyzes PR diffs to identify remediation patterns."""

import json
import logging
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

@dataclass
class DiffAnalysis:
    """Analysis of a single diff."""
    pr_id: str
    repo: str
    title: str
    merge_time_hours: float
    discussion_density: float
    is_security: bool
    was_reverted: bool
    fingerprint: str

class PatternExtractor:
    """Extract patterns from collected PR data."""

    def __init__(self, input_file: str = "data/raw_prs.jsonl"):
        self.input_file = Path(input_file)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info(f"Initialized pattern extractor")

    def load_prs(self) -> List[Dict]:
        """Load collected PRs from JSONL file."""
        prs = []
        if not self.input_file.exists():
            logger.warning(f"Input file not found: {self.input_file}")
            return prs
            
        with open(self.input_file, 'r') as f:
            for line in f:
                if line.strip():
                    prs.append(json.loads(line))
        logger.info(f"Loaded {len(prs)} PRs")
        return prs

    def extract_patterns(self) -> List[Dict]:
        """Complete extraction pipeline."""
        prs = self.load_prs()
        if not prs:
            return []
        
        # Analyze
        diffs = []
        for pr in prs:
            diff = DiffAnalysis(
                pr_id=f"{pr['owner']}/{pr['repo']}#{pr['pr_number']}",
                repo=f"{pr['owner']}/{pr['repo']}",
                title=pr['title'],
                merge_time_hours=pr['merge_time_hours'],
                discussion_density=pr.get('review_comments', 0) / max(pr['additions'] + pr['deletions'], 1),
                is_security=pr['is_security_related'],
                was_reverted=pr['has_revert'],
                fingerprint=hashlib.sha256(pr['title'].encode()).hexdigest()[:16]
            )
            diffs.append(diff)
        
        # Cluster
        texts = [d.title for d in diffs]
        embeddings = self.embedder.encode(texts)
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(embeddings)
        
        clustering = DBSCAN(eps=0.5, min_samples=3, metric='cosine')
        labels = clustering.fit_predict(embeddings_scaled)
        
        # Extract patterns
        patterns = []
        clusters = defaultdict(list)
        for idx, label in enumerate(labels):
            if label != -1:
                clusters[label].append(idx)
        
        for cluster_id, indices in clusters.items():
            if len(indices) < 3:
                continue
            
            cluster_diffs = [diffs[i] for i in indices]
            merge_times = [d.merge_time_hours for d in cluster_diffs]
            revert_count = sum(1 for d in cluster_diffs if d.was_reverted)
            repos = set(d.repo for d in cluster_diffs)
            
            pattern = {
                'cluster_id': int(cluster_id),
                'size': len(cluster_diffs),
                'evidence': {
                    'occurrence_count': len(cluster_diffs),
                    'repo_count': len(repos),
                    'median_merge_hours': float(np.median(merge_times)),
                    'median_discussion_density': float(np.median([d.discussion_density for d in cluster_diffs])),
                    'revert_rate': revert_count / len(cluster_diffs),
                },
            }
            patterns.append(pattern)
        
        return patterns
