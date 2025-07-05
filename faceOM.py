from deepface import DeepFace
import matplotlib.pyplot as plt
import os
import csv
import time

def find_most_similar(image_path, dataset_folder, log_callback=None):
    """Perform facial recognition and find the most similar face."""
    results = []
    metrics_per_epoch = []
    start_time = time.time()

    # Ensure results directory exists
    results_dir = os.path.join(os.getcwd(), "results/faceom")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # CSV file for appending results
    csv_file = os.path.join(results_dir, "face_matching_results.csv")
    top_result_file = os.path.join(results_dir, "top_result.txt")
    facial_results_file = os.path.join(os.getcwd(), "results", "facial_results.txt")

    epoch = 0
    # Iterate through all images in the dataset folder
    for img_name in os.listdir(dataset_folder):
        img_path = os.path.join(dataset_folder, img_name)
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # Skip non-image files
            continue

        try:
            if log_callback:
                log_callback(f"Comparing {os.path.basename(image_path)} with {img_name}...")
            result = DeepFace.verify(image_path, img_path)
            accuracy = (1 - result['distance']) * 100  # Convert distance to confidence percentage
            precision = accuracy / 100
            recall = 1  # For demo, assume recall is 1 (you can adjust if you have ground truth)
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

        except Exception as e:
            if log_callback:
                log_callback(f"Error processing {img_name}: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    if log_callback:
        log_callback(f"Time taken for scanning: {elapsed_time:.2f} seconds")

    # Append results to CSV
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Image", "Confidence (%)"])
        if os.stat(csv_file).st_size == 0:  # Write header only if file is empty
            writer.writeheader()
        writer.writerows(results)

    if log_callback:
        log_callback(f"Results saved to {csv_file}")

    # Sort results by confidence and get the top 10 matches
    top_results = sorted(results, key=lambda x: x["Confidence (%)"], reverse=True)[:10]

    # Calculate metrics
    accuracy = max([result["Confidence (%)"] for result in results]) if results else 0
    recall_time = elapsed_time
    precision = accuracy / 100  # Assuming accuracy is equivalent to precision
    f1_score = (2 * precision) / (precision + 1) if precision > 0 else 0  # Example F1 score calculation

    # Save metrics to facial_results.txt
    with open(facial_results_file, "w") as file:
        file.write(f"Accuracy: {accuracy:.2f}%\n")
        file.write(f"Recall Time: {recall_time:.2f}s\n")
        file.write(f"F1-Score: {f1_score:.2f}\n")

    # Save per-epoch metrics to CSV for plotting
    metrics_csv = os.path.join(os.getcwd(), "results", "facial_metrics_per_epoch.csv")
    with open(metrics_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["epoch", "accuracy", "precision", "recall", "f1_score"])
        writer.writeheader()
        writer.writerows(metrics_per_epoch)

    # Save the top result to a separate file
    if results:
        best_match = max(results, key=lambda x: x["Confidence (%)"])
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

