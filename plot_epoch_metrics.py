import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_metric(csv_file, metric, algo_name, color, out_folder):
    df = pd.read_csv(csv_file)
    df = df.head(10)  # Only first 10 epochs
    plt.figure(figsize=(8, 5))
    plt.bar(df["epoch"], df[metric], color=color)
    plt.xlabel("Epoch")
    plt.ylabel(metric.capitalize())
    plt.title(f"{metric.capitalize()} vs Epoch ({algo_name})")
    plt.xticks(df["epoch"])
    plt.tight_layout()
    plt.savefig(os.path.join(out_folder, f"{algo_name.lower().replace(' ', '_')}_{metric}_vs_epoch.png"))
    plt.close()

RESULTS_FOLDER = os.path.join(os.getcwd(), "results")
facial_csv = os.path.join(RESULTS_FOLDER, "facial_metrics_per_epoch.csv")
fingerprint_csv = os.path.join(RESULTS_FOLDER, "fingerprint_metrics_per_epoch.csv")

# Define colors for each metric
colors = {
    "accuracy": "#1f77b4",   # blue
    "precision": "#ff7f0e",  # orange
    "recall": "#2ca02c",     # green
    "f1_score": "#d62728"    # red
}

# Plot for Facial Recognition
for metric in colors:
    plot_metric(facial_csv, metric, "Facial Recognition", colors[metric], RESULTS_FOLDER)

# Plot for Fingerprint Recognition
for metric in colors:
    plot_metric(fingerprint_csv, metric, "Fingerprint Recognition", colors[metric], RESULTS_FOLDER)

print("✅ All graphs for first 10 epochs saved in the results folder.")