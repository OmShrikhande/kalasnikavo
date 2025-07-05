import os
import matplotlib.pyplot as plt
import numpy as np

# Define paths
RESULTS_FOLDER = os.path.join(os.getcwd(), "results")
FACIAL_RESULTS_FILE = os.path.join(RESULTS_FOLDER, "facial_results.txt")
FINGERPRINT_RESULTS_FILE = os.path.join(RESULTS_FOLDER, "fingerprint_results.txt")

# Function to extract metrics from results file
def extract_metrics(file_path):
    metrics = {"accuracy": 0, "recall_time": 0, "f1_score": 0}
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return metrics

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().lower()
            if "accuracy" in line:
                metrics["accuracy"] = float(line.split(":")[1].strip().replace("%", ""))
            elif "recall time" in line:
                metrics["recall_time"] = float(line.split(":")[1].strip().replace("s", ""))
            elif "f1-score" in line:
                metrics["f1_score"] = float(line.split(":")[1].strip())
    return metrics

# Extract metrics for facial and fingerprint recognition
facial_metrics = extract_metrics(FACIAL_RESULTS_FILE)
fingerprint_metrics = extract_metrics(FINGERPRINT_RESULTS_FILE)

# Simulate dataset growth
dataset_sizes = [200, 1000, 5000, 10000, 50000, 100000]

# Simulate how recall time scales with dataset size (assuming linear growth)
facial_recall_times = [facial_metrics["recall_time"] * (size / 200) for size in dataset_sizes]
fingerprint_recall_times = [fingerprint_metrics["recall_time"] * (size / 200) for size in dataset_sizes]

# Simulate how accuracy and F1 score might degrade slightly with larger datasets
facial_accuracies = [max(0, facial_metrics["accuracy"] - (0.01 * (size / 200))) for size in dataset_sizes]
fingerprint_accuracies = [max(0, fingerprint_metrics["accuracy"] - (0.01 * (size / 200))) for size in dataset_sizes]

facial_f1_scores = [max(0, facial_metrics["f1_score"] - (0.01 * (size / 200))) for size in dataset_sizes]
fingerprint_f1_scores = [max(0, fingerprint_metrics["f1_score"] - (0.01 * (size / 200))) for size in dataset_sizes]

# Generate combined bar graph
def generate_combined_bar_graph(dataset_sizes, facial_times, fingerprint_times, facial_accuracies, fingerprint_accuracies, facial_f1_scores, fingerprint_f1_scores, output_file):
    x = np.arange(len(dataset_sizes))  # X-axis positions for bars
    bar_width = 0.35  # Width of each bar

    plt.figure(figsize=(14, 10))

    # Plot recall times
    plt.subplot(3, 1, 1)
    plt.bar(x - bar_width / 2, facial_times, bar_width, label="Facial Recognition Recall Time", color="blue")
    plt.bar(x + bar_width / 2, fingerprint_times, bar_width, label="Fingerprint Recognition Recall Time", color="green")
    plt.title("Recall Time vs Dataset Size")
    plt.xlabel("Dataset Size")
    plt.ylabel("Recall Time (s)")
    plt.xticks(x, [str(size) for size in dataset_sizes])
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend()

    # Plot accuracies
    plt.subplot(3, 1, 2)
    plt.bar(x - bar_width / 2, facial_accuracies, bar_width, label="Facial Recognition Accuracy", color="blue")
    plt.bar(x + bar_width / 2, fingerprint_accuracies, bar_width, label="Fingerprint Recognition Accuracy", color="green")
    plt.title("Accuracy vs Dataset Size")
    plt.xlabel("Dataset Size")
    plt.ylabel("Accuracy (%)")
    plt.xticks(x, [str(size) for size in dataset_sizes])
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend()

    # Plot F1 scores
    plt.subplot(3, 1, 3)
    plt.bar(x - bar_width / 2, facial_f1_scores, bar_width, label="Facial Recognition F1 Score", color="blue")
    plt.bar(x + bar_width / 2, fingerprint_f1_scores, bar_width, label="Fingerprint Recognition F1 Score", color="green")
    plt.title("F1 Score vs Dataset Size")
    plt.xlabel("Dataset Size")
    plt.ylabel("F1 Score")
    plt.xticks(x, [str(size) for size in dataset_sizes])
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"✅ Combined scaling bar graph saved to: {output_file}")

# Generate the combined bar graph
generate_combined_bar_graph(
    dataset_sizes,
    facial_recall_times,
    fingerprint_recall_times,
    facial_accuracies,
    fingerprint_accuracies,
    facial_f1_scores,
    fingerprint_f1_scores,
    os.path.join(RESULTS_FOLDER, "combined_scaling_bar_graph.png")
)