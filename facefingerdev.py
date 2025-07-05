import os
import cv2
import pickle
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from skimage.feature import local_binary_pattern
from skimage.filters import gabor
from scipy.ndimage import gaussian_filter
import pandas as pd
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import sys
import threading
import subprocess
import tkinter as tk


class FaceProcessor:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.resnet = ResNet50(weights="imagenet", include_top=False, pooling='avg')
        self.face_model = Model(inputs=self.resnet.input, outputs=self.resnet.output)
        self.X = []
        self.y = []

    def extract_features(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            return None
        img = cv2.resize(img, (224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0) / 255.0
        features = self.face_model.predict(img, verbose=0)
        return features.flatten()

    def load_data(self):
        print("Extracting face features...")
        for class_name in os.listdir(self.dataset_path):
            class_dir = os.path.join(self.dataset_path, class_name)
            if not os.path.isdir(class_dir):
                continue
            for img_file in os.listdir(class_dir):
                if not img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    continue
                img_path = os.path.join(class_dir, img_file)
                features = self.extract_features(img_path)
                if features is not None:
                    self.X.append(features)
                    self.y.append(class_name)
        print(f"[OK] {len(self.X)} face samples collected.")

    def filter_classes(self, min_samples=2):
        counts = Counter(self.y)
        valid_labels = {label for label, count in counts.items() if count >= min_samples}
        self.X = [x for x, y in zip(self.X, self.y) if y in valid_labels]
        self.y = [y for y in self.y if y in valid_labels]
        if not self.y:
            raise ValueError("No classes in the face dataset have at least 2 samples. Please check your dataset.")


class FingerprintProcessor:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.X = []
        self.y = []

    def gabor_enhance(self, img):
        img = img / 255.0
        real, _ = gabor(img, frequency=0.6)
        return (real * 255).astype(np.uint8)

    def extract_lbp(self, img):
        lbp = local_binary_pattern(img, P=8, R=1, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 10), range=(0, 9))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-6)
        return hist

    def fake_minutiae_features(self, img):
        blurred = gaussian_filter(img, sigma=1)
        corners = cv2.goodFeaturesToTrack(blurred, maxCorners=10, qualityLevel=0.01, minDistance=5)
        return corners.shape[0] if corners is not None else 0

    def extract_features(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        img = cv2.resize(img, (100, 100))
        img = cv2.equalizeHist(img)
        enhanced = self.gabor_enhance(img)
        lbp = self.extract_lbp(enhanced)
        minutiae = self.fake_minutiae_features(enhanced)
        return np.append(lbp, minutiae)

    def load_data(self):
        print("Extracting fingerprint features...")

        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset path '{self.dataset_path}' does not exist.")

        has_subdirs = any(os.path.isdir(os.path.join(self.dataset_path, item)) for item in os.listdir(self.dataset_path))

        if has_subdirs:
            for class_name in os.listdir(self.dataset_path):
                class_dir = os.path.join(self.dataset_path, class_name)
                if not os.path.isdir(class_dir):
                    continue
                for img_file in os.listdir(class_dir):
                    if not img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        continue
                    img_path = os.path.join(class_dir, img_file)
                    features = self.extract_features(img_path)
                    if features is not None:
                        self.X.append(features)
                        self.y.append(class_name)
        else:
            for img_file in os.listdir(self.dataset_path):
                if not img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    continue
                label = os.path.splitext(img_file)[0].split('_')[0]
                img_path = os.path.join(self.dataset_path, img_file)
                features = self.extract_features(img_path)
                if features is not None:
                    self.X.append(features)
                    self.y.append(label)

        print(f"[OK] {len(self.X)} fingerprint samples collected from {self.dataset_path}.")

    def filter_classes(self, min_samples=2):
        counts = Counter(self.y)
        valid_labels = {label for label, count in counts.items() if count >= min_samples}
        self.X = [x for x, y in zip(self.X, self.y) if y in valid_labels]
        self.y = [y for y in self.y if y in valid_labels]
        if not self.y:
            raise ValueError("No classes in the fingerprint dataset have at least 2 samples. Please check your dataset.")


class ModelEvaluator:
    def __init__(self, X, y, model, name):
        self.X = X
        self.y = y
        self.model = model
        self.name = name

    def evaluate(self):
        class_counts = Counter(self.y)
        min_class_samples = min(class_counts.values())
        if min_class_samples < 2:
            raise ValueError(f"Each class in the {self.name} dataset must have at least 2 samples for StratifiedKFold.")
        n_splits = max(min(min_class_samples, 3), 2)
        skf = StratifiedKFold(n_splits=n_splits)
        scores = cross_val_score(self.model, self.X, self.y, cv=skf)
        print(f"{self.name} CV Scores: {scores}")
        return scores

    def save_model(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.model, f)

    @staticmethod
    def plot_results(face_scores, fp_scores, results_dir):
        results_df = pd.DataFrame({
            'Face KNN Accuracy': [np.mean(face_scores)],
            'Fingerprint SVM Accuracy': [np.mean(fp_scores)]
        })
        os.makedirs(results_dir, exist_ok=True)
        results_df.to_csv(os.path.join(results_dir, "model_accuracy.csv"), index=False)
        plt.figure(figsize=(8, 6))
        plt.bar(["Face KNN", "Fingerprint SVM"], [np.mean(face_scores), np.mean(fp_scores)], color=['blue', 'green'])
        plt.ylabel("Accuracy")
        plt.title("Model Accuracy")
        plt.ylim(0, 1)
        plt.savefig(os.path.join(results_dir, "model_accuracy_graph.png"))
        plt.show()
        print(f"[OK] Results and graphs saved to {results_dir}")


def compare_single_image_with_faces(input_image_path, faces_folder, face_model):
    input_filename = os.path.basename(input_image_path)
    input_prefix = os.path.splitext(input_filename)[0].split('_')[0]  # Get prefix before first underscore

    print(f"Comparing input image: {input_filename} with images in {faces_folder} having prefix '{input_prefix}'")
    input_features = face_model.extract_features(input_image_path)
    if input_features is None:
        print("[ERROR] Could not extract features from input image.")
        return

    best_score = -1
    best_match = None

    for face_file in os.listdir(faces_folder):
        if not face_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            continue
        # Only compare with files that have the same prefix
        if not face_file.startswith(input_prefix):
            continue
        face_path = os.path.join(faces_folder, face_file)
        print(f"Comparing with: {face_file}")
        features = face_model.extract_features(face_path)
        if features is None:
            continue

        similarity = cosine_similarity([input_features], [features])[0][0]
        if similarity > best_score:
            best_score = similarity
            best_match = face_file

    if best_match:
        print(f"[OK] Best match: {best_match} (Similarity: {best_score:.4f})")
    else:
        print("[ERROR] No valid face images found for comparison with the same prefix.")


def run_fingerprint_dev(self):
    """Run facefingerdev.py and show its output in the fingerprint log panel."""
    self.fingerprint_logs_text.delete(1.0, tk.END)
    self.log_fingerprint("Running facefingerdev.py ...")
    def run_script():
        try:
            args = [r".venv\Scripts\python.exe", "facefingerdev.py"]
            if self.selected_facial_image:
                args.append(self.selected_facial_image)
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                universal_newlines=True,
                bufsize=1
            )
            for line in process.stdout:
                self.log_fingerprint(line.rstrip())
            process.stdout.close()
            process.wait()
            self.log_fingerprint("facefingerdev.py finished.")
        except Exception as e:
            self.log_fingerprint(f"Error running facefingerdev.py: {e}")
    threading.Thread(target=run_script, daemon=True).start()


if __name__ == "__main__":
    # === Paths ===
    FACIAL_FOLDER_1 = os.path.join(os.getcwd(), "archive", "Original Images")
    FACIAL_FOLDER_2 = os.path.join(os.getcwd(), "archive", "Faces")
    FINGERPRINT_DATASET = os.path.join(os.getcwd(), "fingerprtintDataset", "real")

    # === Face: Original Images ===
    face_proc1 = FaceProcessor(FACIAL_FOLDER_1)
    face_proc1.load_data()

    # === Face: Flat Folder (Faces) ===
    face_proc2 = FaceProcessor(FACIAL_FOLDER_2)
    face_proc2.load_data()

    # Combine face data
    face_proc1.X.extend(face_proc2.X)
    face_proc1.y.extend(face_proc2.y)
    face_proc1.filter_classes()

    # === Fingerprint ===
    fp_proc = FingerprintProcessor(FINGERPRINT_DATASET)
    fp_proc.load_data()
    fp_proc.filter_classes()

    # === Models ===
    knn_model = KNeighborsClassifier(n_neighbors=3)
    svm_model = SVC(kernel='linear', probability=True)

    # === Evaluation ===
    face_eval = ModelEvaluator(face_proc1.X, face_proc1.y, knn_model, "face")
    fp_eval = ModelEvaluator(fp_proc.X, fp_proc.y, svm_model, "fingerprint")

    face_scores = face_eval.evaluate()
    fp_scores = fp_eval.evaluate()

    face_eval.save_model("knn_model.pkl")
    fp_eval.save_model("svm_fingerprint_model.pkl")

    results_dir = os.path.join(os.getcwd(), "results", "devop")
    ModelEvaluator.plot_results(face_scores, fp_scores, results_dir)

    # === Face Comparison ===
    # Get input image path from command-line argument if provided
    if len(sys.argv) > 1:
        input_img_path = sys.argv[1]
        print(f"Comparing with user-selected image: {input_img_path}")
        compare_single_image_with_faces(input_img_path, FACIAL_FOLDER_2, face_proc1)
    else:
        print("No input image provided for comparison.")
