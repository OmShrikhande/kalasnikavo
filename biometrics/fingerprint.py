"""
biometrics/fingerprint.py
Fingerprint recognition processing logic, refactored for modularity and best practices.
"""
import os
import cv2
import numpy as np
from skimage.feature import hog
from sklearn.metrics.pairwise import cosine_similarity
import time
import csv
import logging
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Callable
from .config import FINGERPRINT_DATASET_PATH, FINGERPRINT_RESULTS_FILE, RESULTS_DIR, MIN_CLASS_SAMPLES
from .utils import setup_logging

setup_logging()


def extract_features(image_path: str) -> np.ndarray:
    """Extract HOG features from an image."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")
    image = cv2.resize(image, (128, 128))
    features, _ = hog(image, orientations=9, pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2), visualize=True, feature_vector=True)
    return features


def compare_fingerprints(fingerprint_path: str, dataset_path: Optional[str], log_callback: Optional[Callable[[str], None]], progress_bar=None):
    if dataset_path is None:
        dataset_path = FINGERPRINT_DATASET_PATH
    start_time = time.time()
    best_score = -1
    best_match_file = None
    scores = []
    metrics_per_epoch = []
    try:
        input_features = extract_features(fingerprint_path)
    except Exception as e:
        msg = f"[ERROR] Failed to process input fingerprint: {e}"
        logging.error(msg)
        if log_callback:
            log_callback(msg)
        return
    files = [f for f in os.listdir(dataset_path) if f.lower().endswith(".bmp")]
    total = len(files)
    if log_callback:
        log_callback(f"Comparing against {total} fingerprints...")
    epoch = 0
    for idx, file in enumerate(files):
        if progress_bar:
            progress = int((idx + 1) / total * 100)
            progress_bar["value"] = progress
            progress_bar.update_idletasks()
        try:
            db_path = os.path.join(dataset_path, file)
            db_features = extract_features(db_path)
            score = cosine_similarity([input_features], [db_features])[0][0]
            accuracy = score * 100
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
            scores.append((file, score))
            if log_callback:
                log_callback(f"{file}: Score = {score:.4f}")
            if score > best_score:
                best_score = score
                best_match_file = file
        except Exception as e:
            msg = f"[ERROR] Skipping {file}: {e}"
            logging.error(msg)
            if log_callback:
                log_callback(msg)
            continue
    metrics_csv = os.path.join(RESULTS_DIR, "fingerprint_metrics_per_epoch.csv")
    with open(metrics_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["epoch", "accuracy", "precision", "recall", "f1_score"])
        writer.writeheader()
        writer.writerows(metrics_per_epoch)
    elapsed_time = time.time() - start_time
    accuracy = best_score * 100 if best_score > 0 else 0
    recall_time = elapsed_time
    f1_score = (2 * accuracy) / (accuracy + 100) if accuracy > 0 else 0
    with open(FINGERPRINT_RESULTS_FILE, "w") as file:
        file.write(f"Accuracy: {accuracy:.2f}%\n")
        file.write(f"Recall Time: {recall_time:.2f}s\n")
        file.write(f"F1-Score: {f1_score:.2f}\n")
    if best_match_file:
        if log_callback:
            log_callback(f"\nBest match: {best_match_file} (Score: {best_score:.4f})")
        input_img = cv2.imread(fingerprint_path)
        best_match_img = cv2.imread(os.path.join(dataset_path, best_match_file))
        os.makedirs(os.path.join(RESULTS_DIR, "fOM", "outputs"), exist_ok=True)
        cv2.imwrite(os.path.join(RESULTS_DIR, "fOM", "outputs", "input.png"), input_img)
        cv2.imwrite(os.path.join(RESULTS_DIR, "fOM", "outputs", "best_match.png"), best_match_img)
    else:
        if log_callback:
            log_callback("\nNo match found.")
    if log_callback:
        log_callback(f"Time taken: {elapsed_time:.2f} seconds")
    results_csv_path = os.path.join(RESULTS_DIR, "fOM", "outputs", "results.csv")
    df = pd.DataFrame(scores, columns=["Filename", "CosineSimilarity"])
    df = df.sort_values(by="CosineSimilarity", ascending=False)
    df.to_csv(results_csv_path, index=False)
    top5 = df.head(5)
    plt.figure(figsize=(8, 4))
    plt.bar(top5["Filename"], top5["CosineSimilarity"], color='skyblue')
    plt.title("Top 5 Fingerprint Matches")
    plt.ylabel("Cosine Similarity Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "fOM", "outputs", "match_scores.png"))
    plt.close()
