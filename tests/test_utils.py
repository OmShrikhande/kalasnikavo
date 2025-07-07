"""
tests/test_utils.py
Unit tests for biometrics.utils
"""
import tempfile
from biometrics import utils

def test_extract_metrics_missing_file():
    metrics = utils.extract_metrics("not_a_real_file.txt")
    assert metrics["accuracy"] == 0
    assert metrics["recall_time"] == 0
    assert metrics["f1_score"] == 0

def test_extract_metrics_valid_file():
    with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as f:
        f.write("Accuracy: 99.9%\nRecall Time: 1.23s\nF1-Score: 0.98\n")
        f.flush()
        metrics = utils.extract_metrics(f.name)
        assert metrics["accuracy"] == 99.9
        assert metrics["recall_time"] == 1.23
        assert metrics["f1_score"] == 0.98
