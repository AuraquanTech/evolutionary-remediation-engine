#!/usr/bin/env python3
"""Confidence scoring: Non-AI statistical model."""

import json
import logging
from pathlib import Path
from typing import Dict, List
import numpy as np

logger = logging.getLogger(__name__)

class ConfidenceScorer:
    """Formula-based confidence scoring."""

    WEIGHTS = {
        'merge_velocity': 0.40,
        'stability': 0.30,
        'discussion': 0.15,
        'frequency': 0.10,
        'diversity': 0.05,
    }

    @staticmethod
    def score_pattern(pattern: Dict) -> float:
        """Calculate confidence score for a pattern."""
        evidence = pattern['evidence']
        
        # Merge velocity score
        merge_velocity = min(1.0, max(0.0, 1.0 - (evidence['median_merge_hours'] / 24.0)))
        
        # Stability score
        stability = max(0.1, 1.0 - (evidence['revert_rate'] * 10.0))
        
        # Discussion score
        discussion = max(0.1, 1.0 - (evidence['median_discussion_density'] * 2.0))
        
        # Frequency score
        frequency = min(1.0, np.log10(evidence['occurrence_count'] + 1) / 3.0)
        
        # Diversity score
        diversity_ratio = evidence['repo_count'] / max(evidence['occurrence_count'], 1)
        diversity = min(0.95, diversity_ratio * 0.5)
        
        # Weighted sum
        score = (
            ConfidenceScorer.WEIGHTS['merge_velocity'] * merge_velocity +
            ConfidenceScorer.WEIGHTS['stability'] * stability +
            ConfidenceScorer.WEIGHTS['discussion'] * discussion +
            ConfidenceScorer.WEIGHTS['frequency'] * frequency +
            ConfidenceScorer.WEIGHTS['diversity'] * diversity
        )
        
        return max(0.0, min(1.0, score))
