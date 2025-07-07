"""
tests/test_fingerprint.py
Unit tests for biometrics.fingerprint
"""
import os
import pytest
from biometrics import fingerprint

def test_extract_features_invalid_path():
    with pytest.raises(ValueError):
        fingerprint.extract_features("nonexistent.bmp")

def test_compare_fingerprints_empty_dataset(tmp_path):
    # Create empty dataset folder
    dataset = tmp_path / "prints"
    dataset.mkdir()
    # Should not raise, but return None
    result = fingerprint.compare_fingerprints("nonexistent.bmp", str(dataset), None)
    assert result is None or result is None
