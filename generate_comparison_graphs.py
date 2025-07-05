import os
import matplotlib.pyplot as plt

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
            elif "recall" in line:
                metrics["recall_time"] = float(line.split(":")[1].strip().replace("s", ""))
            elif "f1-score" in line:
                metrics["f1_score"] = float(line.split(":")[1].strip())
    return metrics

# Extract metrics for facial and fingerprint recognition
facial_metrics = extract_metrics(FACIAL_RESULTS_FILE)
fingerprint_metrics = extract_metrics(FINGERPRINT_RESULTS_FILE)

# Generate comparison graphs
def generate_comparison_graphs(facial_metrics, fingerprint_metrics):
    labels = ["Accuracy (%)", "Recall Time (s)", "F1 Score"]
    facial_values = [facial_metrics["accuracy"], facial_metrics["recall_time"], facial_metrics["f1_score"]]
    fingerprint_values = [fingerprint_metrics["accuracy"], fingerprint_metrics["recall_time"], fingerprint_metrics["f1_score"]]

    x = range(len(labels))
    plt.figure(figsize=(10, 6))
    plt.bar(x, facial_values, width=0.4, label="Facial Recognition", color="blue", align="center")
    plt.bar([i + 0.4 for i in x], fingerprint_values, width=0.4, label="Fingerprint Recognition", color="green", align="center")
    plt.xticks([i + 0.2 for i in x], labels)
    plt.title("Comparison of Facial and Fingerprint Recognition Metrics")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save the graph
    output_path = os.path.join(RESULTS_FOLDER, "comparison_graph.png")
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Comparison graph saved to: {output_path}")

# Generate the graph
generate_comparison_graphs(facial_metrics, fingerprint_metrics)