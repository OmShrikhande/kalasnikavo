"""
biometrics/utils.py
Utility functions for logging, metrics, and file operations.
"""
import logging
import os
from typing import Dict, Any

# Logging setup

def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )


def extract_metrics(file_path: str) -> Dict[str, Any]:
    metrics = {"accuracy": 0, "recall_time": 0, "f1_score": 0}
    if not os.path.exists(file_path):
        logging.warning(f"File not found: {file_path}")
        return metrics
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().lower()
            if "accuracy" in line:
                metrics["accuracy"] = float(line.split(":")[1].strip().replace("%", ""))
            elif "recall" in line:
                metrics["recall_time"] = float(line.split(":")[1].strip().replace("s", ""))
            elif "f1-score" in line:
                metrics["f1_score"] = float(line.split(":")[1].strip())
    return metrics
