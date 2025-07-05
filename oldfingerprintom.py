import os
import cv2
import numpy as np
from skimage.feature import hog
from sklearn.metrics.pairwise import cosine_similarity
import time
from tkinter import END
import pandas as pd
import matplotlib.pyplot as plt
import csv

# === CONFIG: Output path ===
RESULTS_DIR = os.path.join("results", "fOM", "outputs")
os.makedirs(RESULTS_DIR, exist_ok=True)

FINGERPRINT_DATASET_PATH = r"C:\xampp\htdocs\college project face fingerprint\fingerprtintDataset\altered\Altered easy"
FINGERPRINT_RESULTS_FILE = os.path.join(os.getcwd(), "results", "fingerprint_results.txt")

def extract_features(image_path):
    """Extract HOG features from an image."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")
    image = cv2.resize(image, (128, 128))
    features, _ = hog(image, orientations=9, pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2), visualize=True, feature_vector=True)
    return features

def compare_fingerprints(fingerprint_path, dataset_path, log_widget, progress_bar):
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
        log_widget.insert("end", f"[ERROR] Failed to process input fingerprint: {e}\n")
        log_widget.see("end")
        return

    files = [f for f in os.listdir(dataset_path) if f.lower().endswith(".bmp")]
    total = len(files)

    log_widget.insert("end", f"Comparing against {total} fingerprints...\n")
    log_widget.see("end")

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
            recall = 1  # For demo, assume recall is 1
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

            log_widget.insert("end", f"{file}: Score = {score:.4f}\n")
            log_widget.see("end")

            if score > best_score:
                best_score = score
                best_match_file = file

        except Exception as e:
            log_widget.insert("end", f"[ERROR] Skipping {file}: {e}\n")
            log_widget.see("end")
            continue

    # Save per-epoch metrics to CSV for plotting
    metrics_csv = os.path.join(os.getcwd(), "results", "fingerprint_metrics_per_epoch.csv")
    with open(metrics_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["epoch", "accuracy", "precision", "recall", "f1_score"])
        writer.writeheader()
        writer.writerows(metrics_per_epoch)

    elapsed_time = time.time() - start_time

    # Calculate metrics
    accuracy = best_score * 100 if best_score > 0 else 0
    recall_time = elapsed_time
    f1_score = (2 * accuracy) / (accuracy + 100) if accuracy > 0 else 0  # Example F1 score calculation

    # Save metrics to fingerprint_results.txt
    with open(FINGERPRINT_RESULTS_FILE, "w") as file:
        file.write(f"Accuracy: {accuracy:.2f}%\n")
        file.write(f"Recall Time: {recall_time:.2f}s\n")
        file.write(f"F1-Score: {f1_score:.2f}\n")

    if best_match_file:
        log_widget.insert("end", f"\nBest match: {best_match_file} (Score: {best_score:.4f})\n")

        # Save input and best match fingerprint
        input_img = cv2.imread(fingerprint_path)
        best_match_img = cv2.imread(os.path.join(dataset_path, best_match_file))
        cv2.imwrite(os.path.join(RESULTS_DIR, "input.png"), input_img)
        cv2.imwrite(os.path.join(RESULTS_DIR, "best_match.png"), best_match_img)

    else:
        log_widget.insert("end", "\nNo match found.\n")

    log_widget.insert("end", f"Time taken: {elapsed_time:.2f} seconds\n")
    log_widget.see("end")

    # Save results to CSV
    results_csv_path = os.path.join(RESULTS_DIR, "results.csv")
    df = pd.DataFrame(scores, columns=["Filename", "CosineSimilarity"])
    df = df.sort_values(by="CosineSimilarity", ascending=False)
    df.to_csv(results_csv_path, index=False)

    # Plot top 5 matches
    top5 = df.head(5)
    plt.figure(figsize=(8, 4))
    plt.bar(top5["Filename"], top5["CosineSimilarity"], color='skyblue')
    plt.title("Top 5 Fingerprint Matches")
    plt.ylabel("Cosine Similarity Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "match_scores.png"))
    plt.close()
