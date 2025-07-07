"""
biometrics/face.py
Face recognition processing logic, refactored for modularity and best practices.
"""
import os
import numpy as np
from deepface import DeepFace
from typing import Callable, Optional, List, Dict, Any
import time
import csv
import logging
from .config import FACIAL_DATASET_PATH, FACEOM_RESULTS_DIR, FACIAL_RESULTS_FILE, MIN_CLASS_SAMPLES
from .utils import setup_logging
from .parallel import parallel_map

setup_logging()


def _verify_pair(args):
    image_path, img_path = args
    try:
        result = DeepFace.verify(image_path, img_path)
        accuracy = (1 - result['distance']) * 100
        return img_path, accuracy, None
    except Exception as e:
        return img_path, None, str(e)

def find_most_similar(image_path: str, dataset_folder: Optional[str] = None, log_callback: Optional[Callable[[str], None]] = None, parallel: bool = True, max_workers: int = 4) -> (Optional[Dict[str, Any]], float):
    """Perform facial recognition and find the most similar face, optionally in parallel."""
    if dataset_folder is None:
        dataset_folder = FACIAL_DATASET_PATH
    results = []
    metrics_per_epoch = []
    start_time = time.time()
    os.makedirs(FACEOM_RESULTS_DIR, exist_ok=True)
    csv_file = os.path.join(FACEOM_RESULTS_DIR, "face_matching_results.csv")
    top_result_file = os.path.join(FACEOM_RESULTS_DIR, "top_result.txt")
    image_files = [f for f in os.listdir(dataset_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    tasks = [(image_path, os.path.join(dataset_folder, img_name)) for img_name in image_files]
    if parallel:
        results_raw = parallel_map(_verify_pair, tasks, max_workers=max_workers)
    else:
        results_raw = [_verify_pair(t) for t in tasks]
    epoch = 0
    for img_name, accuracy, error in [ (os.path.basename(t[1]), acc, err) for t, (p, acc, err) in zip(tasks, results_raw) ]:
        if error:
            logging.error(f"Error processing {img_name}: {error}")
            if log_callback:
                log_callback(f"Error processing {img_name}: {error}")
            continue
        if log_callback:
            log_callback(f"Compared {os.path.basename(image_path)} with {img_name}: {accuracy:.2f}% confidence")
        precision = accuracy / 100
        recall = 1
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        metrics_per_epoch.append({
            "epoch": epoch,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        })
        epoch += 1
        results.append({
            "Image": img_name,
            "Confidence (%)": round(accuracy, 2)
        })
    elapsed_time = time.time() - start_time
    if log_callback:
        log_callback(f"Time taken for scanning: {elapsed_time:.2f} seconds")
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Image", "Confidence (%)"])
        writer.writeheader()
        writer.writerows(results)
    best_match = max(results, key=lambda x: x["Confidence (%)"], default=None)
    accuracy = best_match["Confidence (%)"] if best_match else 0
    recall_time = elapsed_time
    precision = accuracy / 100
    f1_score = (2 * precision) / (precision + 1) if precision > 0 else 0
    with open(FACIAL_RESULTS_FILE, "w") as file:
        file.write(f"Accuracy: {accuracy:.2f}%\n")
        file.write(f"Recall Time: {recall_time:.2f}s\n")
        file.write(f"F1-Score: {f1_score:.2f}\n")
    metrics_csv = os.path.join(os.path.dirname(FACIAL_RESULTS_FILE), "facial_metrics_per_epoch.csv")
    with open(metrics_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["epoch", "accuracy", "precision", "recall", "f1_score"])
        writer.writeheader()
        writer.writerows(metrics_per_epoch)
    if best_match:
        with open(top_result_file, mode='w') as file:
            file.write(f"Best Match: {best_match['Image']}\n")
            file.write(f"Confidence: {best_match['Confidence (%)']}%\n")
            file.write(f"Time Taken: {elapsed_time:.2f} seconds\n")
        if log_callback:
            log_callback(f"Top result saved to {top_result_file}")
        return best_match, elapsed_time
    else:
        if log_callback:
            log_callback("No matching faces found.")
        return None, elapsed_time
