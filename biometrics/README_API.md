"""
biometrics/README_API.md
API Documentation for biometrics package
"""
# Biometrics Python API Documentation

## biometrics.face

### find_most_similar(image_path: str, dataset_folder: Optional[str] = None, log_callback: Optional[Callable[[str], None]] = None) -> (Optional[Dict[str, Any]], float)
- Performs facial recognition and finds the most similar face in the dataset.
- **Args:**
    - `image_path`: Path to the input image.
    - `dataset_folder`: Path to the dataset folder. If None, uses default from config.
    - `log_callback`: Optional function for logging progress.
- **Returns:**
    - Tuple of (best_match_dict or None, elapsed_time in seconds)

## biometrics.fingerprint

### extract_features(image_path: str) -> np.ndarray
- Extracts HOG features from a fingerprint image.
- **Args:**
    - `image_path`: Path to the fingerprint image.
- **Returns:**
    - Numpy array of features.

### compare_fingerprints(fingerprint_path: str, dataset_path: Optional[str], log_callback: Optional[Callable[[str], None]], progress_bar=None)
- Compares a fingerprint against a dataset and logs results.
- **Args:**
    - `fingerprint_path`: Path to the input fingerprint image.
    - `dataset_path`: Path to the dataset folder. If None, uses default from config.
    - `log_callback`: Optional function for logging progress.
    - `progress_bar`: Optional progress bar widget.
- **Returns:**
    - None

## biometrics.utils

### setup_logging(level: str = "INFO")
- Configures logging for the application.

### extract_metrics(file_path: str) -> Dict[str, Any]
- Extracts accuracy, recall time, and F1 score from a results file.

---

For more details, see inline docstrings in each module.
