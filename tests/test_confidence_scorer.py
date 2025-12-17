import pytest
from research.scoring.confidence_scorer import ConfidenceScorer

def test_merge_velocity_score():
    """Test merge velocity scoring."""
    scorer = ConfidenceScorer()
    
    # Fast merge = high score
    assert scorer._merge_velocity_score(0.5) == 1.0
    assert scorer._merge_velocity_score(1.0) == 1.0
    
    # Slow merge = low score
    assert scorer._merge_velocity_score(72) == 0.1

def test_stability_score():
    """Test stability scoring."""
    scorer = ConfidenceScorer()
    
    # No reverts = high score
    assert scorer._stability_score(0.0) == 1.0
    
    # High revert rate = low score
    assert scorer._stability_score(0.1) < 0.5

def test_discussion_score():
    """Test discussion scoring."""
    scorer = ConfidenceScorer()
    
    # No discussion = high score
    assert scorer._discussion_score(0.0) == 1.0
    
    # High discussion = lower score
    assert scorer._discussion_score(1.0) < 0.5
