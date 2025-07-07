"""
tests/test_face.py
Unit tests for biometrics.face
"""
import os
import pytest
from biometrics import face

def test_find_most_similar_returns_none_for_empty_dataset(tmp_path):
    # Create empty dataset folder
    dataset = tmp_path / "faces"
    dataset.mkdir()
    result, elapsed = face.find_most_similar("nonexistent.jpg", str(dataset))
    assert result is None
    assert isinstance(elapsed, float)

def test_find_most_similar_handles_invalid_image(tmp_path):
    dataset = tmp_path / "faces"
    dataset.mkdir()
    # Create a dummy file that is not an image
    dummy = dataset / "not_an_image.txt"
    dummy.write_text("not an image")
    result, elapsed = face.find_most_similar(str(dummy), str(dataset))
    assert result is None or isinstance(result, dict)
    assert isinstance(elapsed, float)
