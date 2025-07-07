"""
biometrics/config.py
Centralized configuration for paths and parameters.
"""
import os

# Dataset paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACIAL_DATASET_PATH = os.path.join(BASE_DIR, "facialDataset", "Faces", "Faces")
FINGERPRINT_DATASET_PATH = os.path.join(BASE_DIR, "fingerprintDataset", "altered")
FINGERPRINT_REAL_PATH = os.path.join(BASE_DIR, "fingerprintDataset", "real")

# Results
RESULTS_DIR = os.path.join(BASE_DIR, "results")
FACEOM_RESULTS_DIR = os.path.join(RESULTS_DIR, "faceom")
FINGERPRINT_RESULTS_FILE = os.path.join(RESULTS_DIR, "fingerprint_results.txt")
FACIAL_RESULTS_FILE = os.path.join(RESULTS_DIR, "facial_results.txt")

# Model files
KNN_MODEL_PATH = os.path.join(RESULTS_DIR, "knn_model.pkl")
SVM_MODEL_PATH = os.path.join(RESULTS_DIR, "svm_fingerprint_model.pkl")

# Other parameters
MIN_CLASS_SAMPLES = 2
BATCH_SIZE = 16
N_JOBS = -1  # For parallelism

# Logging
LOGGING_LEVEL = "INFO"
