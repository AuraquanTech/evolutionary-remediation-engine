"""Pattern data structures."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PatternEvidence:
    """Statistical evidence for a pattern."""
    occurrence_count: int  # How many times seen
    repo_count: int  # How many repos
    median_merge_hours: float
    median_discussion_density: float
    revert_rate: float
    pr_examples: List[str] = field(default_factory=list)  # Links to examples


@dataclass
class FixTemplate:
    """Template for applying a fix."""
    id: str
    name: str
    confidence: float
    evidence: PatternEvidence
    before: str  # Code pattern (before)
    after: str  # Code pattern (after)
    language: str  # e.g., 'python', 'javascript'
    companion_changes: Dict[str, Any] = field(default_factory=dict)
    pr_title_template: str = ""
    pr_body_template: str = ""


@dataclass
class ClusteredPattern:
    """Pattern cluster with metadata."""
    cluster_id: int
    fingerprints: List[str]  # Structural patterns
    pr_indices: List[int]  # Original PR indices
    centroid_embedding: List[float]  # Semantic centroid
    score: float  # Quality score