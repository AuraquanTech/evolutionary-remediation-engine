import pytest
from research.extractors.pattern_extractor import DiffFingerprinter

def test_diff_fingerprint():
    """Test diff fingerprinting."""
    added = ['const API_KEY = "abc123";']
    removed = ['const API_KEY = "hardcoded";']
    
    fingerprint1 = DiffFingerprinter.fingerprint(added, removed)
    assert len(fingerprint1) == 64  # SHA256
    
    # Same diff should give same fingerprint
    fingerprint2 = DiffFingerprinter.fingerprint(added, removed)
    assert fingerprint1 == fingerprint2

def test_diff_normalization():
    """Test line normalization."""
    line = '  const x = "value";  // comment'
    normalized = DiffFingerprinter._normalize_line(line, 'structural')
    assert '<STRING>' in normalized
    assert 'value' not in normalized
    assert 'comment' not in normalized
