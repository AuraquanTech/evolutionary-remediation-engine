import pytest
from research.collectors.github_collector import GitHubCollector

def test_github_collector_init():
    """Test collector initialization."""
    collector = GitHubCollector(
        repositories=["eslint/eslint"],
        max_prs_per_repo=10
    )
    assert collector.repositories == ["eslint/eslint"]
    assert collector.max_prs_per_repo == 10

def test_security_detection():
    """Test security-related PR detection."""
    pr = {
        'title': 'Security: Fix XSS vulnerability',
        'body': 'Fixes CVE-2024-1234',
        'labels': []
    }
    assert GitHubCollector([])._is_security_related(pr)

def test_non_security_detection():
    """Test non-security PR detection."""
    pr = {
        'title': 'Docs: Update README',
        'body': 'Add examples',
        'labels': []
    }
    assert not GitHubCollector([])._is_security_related(pr)
