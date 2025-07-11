"""
Enhanced Flask backend for Dual Biometric Authentication (Face + Fingerprint)
ULTIMATE VERSION - Multi-Algorithm Fusion for Maximum Security
"""
import os
import sys
import json
import hashlib
import sqlite3
import logging
import time
import numpy as np
from datetime import datetime, timedelta
import uuid
import base64
from typing import Dict, List, Tuple, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
from skimage.feature import local_binary_pattern, hog
from skimage.filters import gabor
from scipy.ndimage import gaussian_filter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tensorflow.keras.applications import ResNet50, VGG16, InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Ensure biometrics package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Try to import biometric modules
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("Warning: DeepFace not available")

# Configuration
UPLOAD_FOLDER = 'uploads'
DB_PATH = 'enhanced_ultimate_users.db'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
ALLOWED_FP_EXTENSIONS = {'bmp', 'png', 'jpg', 'jpeg'}
MAX_FACE_IMAGES = 5
SECRET_KEY = 'your-super-secret-key-change-in-production'

# Enhanced Security Configuration with Multi-Algorithm Fusion
SECURITY_LEVELS = {
    'LOW': {
        'face_threshold': 0.7, 'fp_threshold': 0.7, 'fusion_threshold': 0.75,
        'algorithms': ['deepface', 'resnet'], 'max_attempts': 10, 'lockout_time': 300
    },
    'MEDIUM': {
        'face_threshold': 0.8, 'fp_threshold': 0.8, 'fusion_threshold': 0.85,
        'algorithms': ['deepface', 'resnet', 'vgg16'], 'max_attempts': 5, 'lockout_time': 600
    },
    'HIGH': {
        'face_threshold': 0.9, 'fp_threshold': 0.9, 'fusion_threshold': 0.95,
        'algorithms': ['deepface', 'resnet', 'vgg16', 'inception'], 'max_attempts': 3, 'lockout_time': 1800
    },
    'MAXIMUM': {
        'face_threshold': 0.95, 'fp_threshold': 0.95, 'fusion_threshold': 0.98,
        'algorithms': ['deepface', 'resnet', 'vgg16', 'inception', 'ensemble'], 'max_attempts': 2, 'lockout_time': 3600
    }
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Enable CORS
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global models for reuse
face_models = {}
fp_models = {}
scalers = {}

def initialize_models():
    """Initialize all AI models for face and fingerprint recognition"""
    global face_models, fp_models, scalers
    
    logger.info("Initializing AI models...")
    
    # Face recognition models
    try:
        face_models['resnet50'] = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        face_models['vgg16'] = VGG16(weights='imagenet', include_top=False, pooling='avg')
        face_models['inception'] = InceptionV3(weights='imagenet', include_top=False, pooling='avg')
        
        # Feature scalers
        scalers['face'] = StandardScaler()
        scalers['fp'] = StandardScaler()
        
        logger.info("✅ All AI models initialized successfully")
    except Exception as e:
        logger.error(f"❌ Model initialization failed: {e}")

class EnhancedFaceRecognition:
    """Enhanced face recognition with multiple algorithms"""
    
    def __init__(self):
        self.models = face_models
        self.confidence_weights = {
            'deepface': 0.3,
            'resnet50': 0.25,
            'vgg16': 0.2,
            'inception': 0.15,
            'ensemble': 0.1
        }
    
    def extract_resnet_features(self, img_path: str) -> np.ndarray:
        """Extract features using ResNet50"""
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            features = self.models['resnet50'].predict(img_array, verbose=0)
            return features.flatten()
        except Exception as e:
            logger.error(f"ResNet feature extraction failed: {e}")
            return None
    
    def extract_vgg_features(self, img_path: str) -> np.ndarray:
        """Extract features using VGG16"""
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            features = self.models['vgg16'].predict(img_array, verbose=0)
            return features.flatten()
        except Exception as e:
            logger.error(f"VGG feature extraction failed: {e}")
            return None
    
    def extract_inception_features(self, img_path: str) -> np.ndarray:
        """Extract features using InceptionV3"""
        try:
            img = image.load_img(img_path, target_size=(299, 299))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            features = self.models['inception'].predict(img_array, verbose=0)
            return features.flatten()
        except Exception as e:
            logger.error(f"Inception feature extraction failed: {e}")
            return None
    
    def deepface_similarity(self, img1_path: str, img2_path: str) -> float:
        """Calculate similarity using DeepFace"""
        if not DEEPFACE_AVAILABLE:
            return 0.0
        
        try:
            result = DeepFace.verify(img1_path, img2_path, 
                                   model_name='VGG-Face', 
                                   distance_metric='cosine',
                                   enforce_detection=False)
            return (1 - result['distance']) if result['verified'] else 0.0
        except Exception as e:
            logger.error(f"DeepFace similarity failed: {e}")
            return 0.0
    
    def multi_algorithm_face_match(self, test_img_path: str, stored_img_paths: List[str], 
                                 security_level: str) -> Dict[str, Any]:
        """
        Perform face matching using multiple algorithms and fusion
        """
        algorithms = SECURITY_LEVELS[security_level]['algorithms']
        results = {}
        
        # Extract features from test image
        test_features = {}
        if 'resnet' in algorithms:
            test_features['resnet'] = self.extract_resnet_features(test_img_path)
        if 'vgg16' in algorithms:
            test_features['vgg16'] = self.extract_vgg_features(test_img_path)
        if 'inception' in algorithms:
            test_features['inception'] = self.extract_inception_features(test_img_path)
        
        best_overall_score = 0.0
        algorithm_scores = {}
        
        for stored_img_path in stored_img_paths:
            if not os.path.exists(stored_img_path):
                continue
            
            scores = {}
            
            # DeepFace similarity
            if 'deepface' in algorithms:
                scores['deepface'] = self.deepface_similarity(test_img_path, stored_img_path)
            
            # ResNet50 similarity
            if 'resnet' in algorithms and test_features.get('resnet') is not None:
                stored_features = self.extract_resnet_features(stored_img_path)
                if stored_features is not None:
                    similarity = cosine_similarity([test_features['resnet']], [stored_features])[0][0]
                    scores['resnet'] = max(0, similarity)
            
            # VGG16 similarity
            if 'vgg16' in algorithms and test_features.get('vgg16') is not None:
                stored_features = self.extract_vgg_features(stored_img_path)
                if stored_features is not None:
                    similarity = cosine_similarity([test_features['vgg16']], [stored_features])[0][0]
                    scores['vgg16'] = max(0, similarity)
            
            # InceptionV3 similarity
            if 'inception' in algorithms and test_features.get('inception') is not None:
                stored_features = self.extract_inception_features(stored_img_path)
                if stored_features is not None:
                    similarity = cosine_similarity([test_features['inception']], [stored_features])[0][0]
                    scores['inception'] = max(0, similarity)
            
            # Ensemble/Fusion score
            if 'ensemble' in algorithms and len(scores) > 1:
                weighted_score = sum(scores.get(alg, 0) * self.confidence_weights.get(alg, 0.1) 
                                   for alg in scores.keys())
                scores['ensemble'] = weighted_score
            
            # Calculate overall score for this stored image
            overall_score = np.mean(list(scores.values())) if scores else 0.0
            
            if overall_score > best_overall_score:
                best_overall_score = overall_score
                algorithm_scores = scores.copy()
        
        return {
            'overall_confidence': best_overall_score * 100,
            'algorithm_scores': algorithm_scores,
            'passed_threshold': best_overall_score >= SECURITY_LEVELS[security_level]['face_threshold']
        }

class EnhancedFingerprintRecognition:
    """Enhanced fingerprint recognition with multiple algorithms"""
    
    def __init__(self):
        self.confidence_weights = {
            'hog': 0.3,
            'lbp': 0.25,
            'gabor': 0.2,
            'minutiae': 0.15,
            'ensemble': 0.1
        }
    
    def extract_hog_features(self, img_path: str) -> np.ndarray:
        """Extract HOG features"""
        try:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return None
            
            img = cv2.resize(img, (128, 128))
            img = cv2.equalizeHist(img)
            
            features = hog(img, orientations=9, pixels_per_cell=(8, 8),
                          cells_per_block=(2, 2), feature_vector=True)
            return features
        except Exception as e:
            logger.error(f"HOG feature extraction failed: {e}")
            return None
    
    def extract_lbp_features(self, img_path: str) -> np.ndarray:
        """Extract Local Binary Pattern features"""
        try:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return None
            
            img = cv2.resize(img, (128, 128))
            img = cv2.equalizeHist(img)
            
            lbp = local_binary_pattern(img, P=8, R=1, method='uniform')
            hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 11), range=(0, 10))
            hist = hist.astype("float")
            hist /= (hist.sum() + 1e-6)
            return hist
        except Exception as e:
            logger.error(f"LBP feature extraction failed: {e}")
            return None
    
    def extract_gabor_features(self, img_path: str) -> np.ndarray:
        """Extract Gabor filter features"""
        try:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return None
            
            img = cv2.resize(img, (128, 128))
            img = cv2.equalizeHist(img)
            img = img / 255.0
            
            # Apply Gabor filters with different orientations
            features = []
            for angle in [0, 45, 90, 135]:
                real, _ = gabor(img, frequency=0.6, theta=np.radians(angle))
                features.extend(real.flatten())
            
            return np.array(features)
        except Exception as e:
            logger.error(f"Gabor feature extraction failed: {e}")
            return None
    
    def extract_minutiae_features(self, img_path: str) -> np.ndarray:
        """Extract minutiae-like features"""
        try:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return None
            
            img = cv2.resize(img, (128, 128))
            img = cv2.equalizeHist(img)
            
            # Apply Gaussian filter
            blurred = gaussian_filter(img, sigma=1)
            
            # Extract corner points as minutiae approximation
            corners = cv2.goodFeaturesToTrack(blurred, maxCorners=100, 
                                            qualityLevel=0.01, minDistance=5)
            
            if corners is not None:
                # Create feature vector from corner positions
                features = corners.flatten()
                # Pad or truncate to fixed size
                if len(features) < 200:
                    features = np.pad(features, (0, 200 - len(features)), 'constant')
                else:
                    features = features[:200]
                return features
            else:
                return np.zeros(200)
        except Exception as e:
            logger.error(f"Minutiae feature extraction failed: {e}")
            return None
    
    def multi_algorithm_fingerprint_match(self, test_fp_path: str, stored_fp_path: str, 
                                        security_level: str) -> Dict[str, Any]:
        """
        Perform fingerprint matching using multiple algorithms and fusion
        """
        algorithms = SECURITY_LEVELS[security_level]['algorithms']
        scores = {}
        
        # Extract features using different algorithms
        test_hog = self.extract_hog_features(test_fp_path)
        stored_hog = self.extract_hog_features(stored_fp_path)
        
        test_lbp = self.extract_lbp_features(test_fp_path)
        stored_lbp = self.extract_lbp_features(stored_fp_path)
        
        test_gabor = self.extract_gabor_features(test_fp_path)
        stored_gabor = self.extract_gabor_features(stored_fp_path)
        
        test_minutiae = self.extract_minutiae_features(test_fp_path)
        stored_minutiae = self.extract_minutiae_features(stored_fp_path)
        
        # Calculate similarities
        if test_hog is not None and stored_hog is not None:
            similarity = cosine_similarity([test_hog], [stored_hog])[0][0]
            scores['hog'] = max(0, similarity)
        
        if test_lbp is not None and stored_lbp is not None:
            similarity = cosine_similarity([test_lbp], [stored_lbp])[0][0]
            scores['lbp'] = max(0, similarity)
        
        if test_gabor is not None and stored_gabor is not None:
            similarity = cosine_similarity([test_gabor], [stored_gabor])[0][0]
            scores['gabor'] = max(0, similarity)
        
        if test_minutiae is not None and stored_minutiae is not None:
            similarity = cosine_similarity([test_minutiae], [stored_minutiae])[0][0]
            scores['minutiae'] = max(0, similarity)
        
        # Ensemble score
        if len(scores) > 1:
            weighted_score = sum(scores.get(alg, 0) * self.confidence_weights.get(alg, 0.1) 
                               for alg in scores.keys())
            scores['ensemble'] = weighted_score
        
        # Calculate overall score
        overall_score = np.mean(list(scores.values())) if scores else 0.0
        
        return {
            'overall_confidence': overall_score * 100,
            'algorithm_scores': scores,
            'passed_threshold': overall_score >= SECURITY_LEVELS[security_level]['fp_threshold']
        }

# Initialize global recognizers
face_recognizer = None
fingerprint_recognizer = None

def init_recognizers():
    """Initialize recognition systems"""
    global face_recognizer, fingerprint_recognizer
    face_recognizer = EnhancedFaceRecognition()
    fingerprint_recognizer = EnhancedFingerprintRecognition()

def allowed_file(filename, allowed):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize enhanced database"""
    conn = get_db()
    
    # Enhanced users table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT,
        face_paths TEXT NOT NULL,
        fp_path TEXT NOT NULL,
        security_level TEXT DEFAULT 'MEDIUM',
        biometric_quality TEXT,
        face_algorithms TEXT,
        fp_algorithms TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        login_count INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        is_verified BOOLEAN DEFAULT 0
    )''')
    
    # Enhanced authentication attempts table
    conn.execute('''CREATE TABLE IF NOT EXISTS auth_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        ip_address TEXT,
        attempt_type TEXT,
        success BOOLEAN,
        algorithm_scores TEXT,
        overall_confidence REAL,
        response_time REAL,
        failure_reason TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Security events table
    conn.execute('''CREATE TABLE IF NOT EXISTS security_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        username TEXT,
        ip_address TEXT,
        user_agent TEXT,
        severity TEXT,
        details TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def log_security_event(event_type, username=None, details=None, severity='info'):
    """Log security events to database"""
    try:
        conn = get_db()
        ip_address = request.remote_addr if request else 'system'
        user_agent = request.headers.get('User-Agent', '') if request else 'system'
        
        conn.execute('''INSERT INTO security_events 
                       (event_type, username, ip_address, user_agent, severity, details) 
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (event_type, username, ip_address, user_agent, severity, 
                     json.dumps(details) if details else None))
        conn.commit()
        conn.close()
        logger.info(f"Security event: {event_type} - User: {username} - IP: {ip_address}")
    except Exception as e:
        logger.error(f"Failed to log security event: {e}")

def calculate_biometric_quality(file_path, biometric_type):
    """Calculate quality score for biometric data"""
    try:
        file_size = os.path.getsize(file_path)
        
        if biometric_type == 'face':
            # Check image quality
            img = cv2.imread(file_path)
            if img is None:
                return 0.3
            
            # Calculate sharpness using Laplacian variance
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize and combine with file size
            quality = min(0.95, 0.6 + (laplacian_var / 1000) * 0.3 + (file_size / 1000000) * 0.1)
            return quality
            
        elif biometric_type == 'fingerprint':
            # Check fingerprint quality
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return 0.3
            
            # Calculate contrast and sharpness
            contrast = img.std()
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            
            # Normalize and combine metrics
            quality = min(0.98, 0.7 + (contrast / 100) * 0.2 + (laplacian_var / 1000) * 0.1)
            return quality
            
        return 0.5
    except Exception as e:
        logger.error(f"Quality calculation failed: {e}")
        return 0.5

@app.route('/api/register', methods=['POST'])
def register():
    """Enhanced registration with multi-algorithm support"""
    start_time = time.time()
    username = request.form.get('username')
    email = request.form.get('email', '')
    security_level = request.form.get('securityLevel', 'MEDIUM')
    fingerprint = request.files.get('fingerprint')
    
    face_files = []
    for i in range(MAX_FACE_IMAGES):
        file = request.files.get(f'face_{i}')
        if file:
            face_files.append(file)
    
    if not username or not fingerprint or len(face_files) == 0:
        log_security_event('REGISTRATION_FAILED', username, {'reason': 'Missing required fields'}, 'warning')
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not allowed_file(fingerprint.filename, ALLOWED_FP_EXTENSIONS):
        return jsonify({'error': 'Invalid fingerprint file type'}), 400
    
    for f in face_files:
        if not allowed_file(f.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({'error': 'Invalid face file type'}), 400

    # Check if user exists
    conn = get_db()
    existing_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    if existing_user:
        conn.close()
        log_security_event('REGISTRATION_FAILED', username, {'reason': 'User already exists'}, 'warning')
        return jsonify({'error': 'Username already exists'}), 409

    # Save face images with enhanced quality assessment
    face_paths = []
    face_qualities = []
    for idx, face in enumerate(face_files):
        face_filename = secure_filename(f"{username}_face_{idx}_{int(time.time())}.{face.filename.rsplit('.', 1)[1]}")
        face_path = os.path.join(UPLOAD_FOLDER, face_filename)
        face.save(face_path)
        
        quality = calculate_biometric_quality(face_path, 'face')
        face_qualities.append(quality)
        face_paths.append(face_path)

    # Save fingerprint with enhanced quality assessment
    fp_filename = secure_filename(f"{username}_fp_{int(time.time())}.{fingerprint.filename.rsplit('.', 1)[1]}")
    fp_path = os.path.join(UPLOAD_FOLDER, fp_filename)
    fingerprint.save(fp_path)
    
    fp_quality = calculate_biometric_quality(fp_path, 'fingerprint')
    
    # Check quality against security level threshold
    avg_face_quality = sum(face_qualities) / len(face_qualities)
    min_quality = SECURITY_LEVELS[security_level]['face_threshold']
    
    if avg_face_quality < min_quality or fp_quality < min_quality:
        # Clean up files
        for path in face_paths + [fp_path]:
            if os.path.exists(path):
                os.remove(path)
        conn.close()
        return jsonify({
            'error': f'Biometric quality too low for {security_level} security level',
            'required_quality': min_quality,
            'face_quality': avg_face_quality,
            'fingerprint_quality': fp_quality
        }), 400

    # Store user in database with algorithm information
    biometric_quality = {
        'face': avg_face_quality,
        'fingerprint': fp_quality,
        'individual_face_qualities': face_qualities
    }
    
    algorithms_used = {
        'face': SECURITY_LEVELS[security_level]['algorithms'],
        'fingerprint': SECURITY_LEVELS[security_level]['algorithms']
    }
    
    try:
        conn.execute('''INSERT INTO users 
                       (username, email, face_paths, fp_path, security_level, biometric_quality, 
                        face_algorithms, fp_algorithms, is_verified) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (username, email, ','.join(face_paths), fp_path, security_level,
                     json.dumps(biometric_quality), json.dumps(algorithms_used['face']),
                     json.dumps(algorithms_used['fingerprint']), 1))
        conn.commit()
        
        log_security_event('USER_REGISTERED', username, {
            'email': email,
            'security_level': security_level,
            'face_quality': avg_face_quality,
            'fingerprint_quality': fp_quality,
            'algorithms': algorithms_used,
            'registration_time': time.time() - start_time
        }, 'info')
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': conn.lastrowid,
            'biometric_quality': biometric_quality,
            'security_level': security_level,
            'algorithms_used': algorithms_used
        })
        
    except sqlite3.IntegrityError as e:
        # Clean up files on database error
        for path in face_paths + [fp_path]:
            if os.path.exists(path):
                os.remove(path)
        log_security_event('REGISTRATION_FAILED', username, {'reason': 'Database error', 'error': str(e)}, 'error')
        return jsonify({'error': 'Registration failed - database error'}), 500
    finally:
        conn.close()

@app.route('/api/auth/face', methods=['POST'])
def auth_face():
    """Enhanced face authentication with multi-algorithm fusion"""
    start_time = time.time()
    username = request.form.get('username')
    face = request.files.get('face')
    
    if not username or not face:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not allowed_file(face.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save temporary face image
    temp_filename = secure_filename(f"temp_{username}_face_{int(time.time())}.{face.filename.rsplit('.', 1)[1]}")
    temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
    face.save(temp_path)
    
    try:
        # Get user data
        conn = get_db()
        user = conn.execute('''SELECT face_paths, security_level, biometric_quality 
                              FROM users WHERE username = ? AND is_active = 1''', 
                           (username,)).fetchone()
        conn.close()
        
        if not user:
            log_security_event('AUTH_FAILED', username, {'reason': 'User not found', 'attempt_type': 'face'}, 'warning')
            return jsonify({'error': 'Authentication failed'}), 401
        
        # Calculate quality of submitted image
        submitted_quality = calculate_biometric_quality(temp_path, 'face')
        min_quality = SECURITY_LEVELS[user['security_level']]['face_threshold']
        
        if submitted_quality < min_quality:
            log_security_event('AUTH_FAILED', username, {
                'reason': 'Poor image quality',
                'quality': submitted_quality,
                'required': min_quality
            }, 'warning')
            return jsonify({
                'error': 'Image quality too low',
                'quality': submitted_quality,
                'required': min_quality
            }), 400
        
        # Perform multi-algorithm face matching
        stored_face_paths = user['face_paths'].split(',')
        
        result = face_recognizer.multi_algorithm_face_match(
            temp_path, stored_face_paths, user['security_level']
        )
        
        response_time = time.time() - start_time
        
        # Log authentication attempt
        conn = get_db()
        conn.execute('''INSERT INTO auth_attempts 
                       (username, ip_address, attempt_type, success, algorithm_scores, 
                        overall_confidence, response_time) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (username, request.remote_addr, 'face', result['passed_threshold'],
                     json.dumps(result['algorithm_scores']), result['overall_confidence'], response_time))
        conn.commit()
        conn.close()
        
        if result['passed_threshold']:
            log_security_event('FACE_AUTH_SUCCESS', username, {
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'response_time': response_time,
                'quality': submitted_quality
            }, 'info')
            
            return jsonify({
                'success': True,
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'quality': submitted_quality,
                'response_time': response_time
            })
        else:
            log_security_event('FACE_AUTH_FAILED', username, {
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'required': min_quality * 100,
                'response_time': response_time
            }, 'warning')
            
            return jsonify({
                'success': False,
                'error': 'Face not recognized',
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'required': min_quality * 100
            }), 401
            
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/api/auth/fingerprint', methods=['POST'])
def auth_fingerprint():
    """Enhanced fingerprint authentication with multi-algorithm fusion"""
    start_time = time.time()
    username = request.form.get('username')
    fingerprint = request.files.get('fingerprint')
    
    if not username or not fingerprint:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not allowed_file(fingerprint.filename, ALLOWED_FP_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save temporary fingerprint
    temp_filename = secure_filename(f"temp_{username}_fp_{int(time.time())}.{fingerprint.filename.rsplit('.', 1)[1]}")
    temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
    fingerprint.save(temp_path)
    
    try:
        # Get user data
        conn = get_db()
        user = conn.execute('''SELECT fp_path, security_level, biometric_quality, last_login, login_count 
                              FROM users WHERE username = ? AND is_active = 1''', 
                           (username,)).fetchone()
        
        if not user:
            conn.close()
            log_security_event('AUTH_FAILED', username, {'reason': 'User not found', 'attempt_type': 'fingerprint'}, 'warning')
            return jsonify({'error': 'Authentication failed'}), 401
        
        # Calculate quality of submitted fingerprint
        submitted_quality = calculate_biometric_quality(temp_path, 'fingerprint')
        min_quality = SECURITY_LEVELS[user['security_level']]['fp_threshold']
        
        if submitted_quality < min_quality:
            conn.close()
            log_security_event('AUTH_FAILED', username, {
                'reason': 'Poor fingerprint quality',
                'quality': submitted_quality,
                'required': min_quality
            }, 'warning')
            return jsonify({
                'error': 'Fingerprint quality too low',
                'quality': submitted_quality,
                'required': min_quality
            }), 400
        
        # Perform multi-algorithm fingerprint matching
        result = fingerprint_recognizer.multi_algorithm_fingerprint_match(
            temp_path, user['fp_path'], user['security_level']
        )
        
        response_time = time.time() - start_time
        
        # Log authentication attempt
        conn.execute('''INSERT INTO auth_attempts 
                       (username, ip_address, attempt_type, success, algorithm_scores, 
                        overall_confidence, response_time) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (username, request.remote_addr, 'fingerprint', result['passed_threshold'],
                     json.dumps(result['algorithm_scores']), result['overall_confidence'], response_time))
        
        if result['passed_threshold']:
            # Update user login info
            conn.execute('''UPDATE users 
                           SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1 
                           WHERE username = ?''', (username,))
            conn.commit()
            conn.close()
            
            log_security_event('FINGERPRINT_AUTH_SUCCESS', username, {
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'response_time': response_time,
                'quality': submitted_quality
            }, 'info')
            
            return jsonify({
                'success': True,
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'quality': submitted_quality,
                'response_time': response_time,
                'message': 'Access granted! Welcome to your secure dashboard.'
            })
        else:
            conn.commit()
            conn.close()
            
            log_security_event('FINGERPRINT_AUTH_FAILED', username, {
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'required': min_quality * 100,
                'response_time': response_time
            }, 'warning')
            
            return jsonify({
                'success': False,
                'error': 'Fingerprint not recognized',
                'confidence': result['overall_confidence'],
                'algorithm_scores': result['algorithm_scores'],
                'required': min_quality * 100
            }), 401
            
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/api/auth/dual', methods=['POST'])
def auth_dual():
    """Dual biometric authentication (face + fingerprint) with fusion"""
    start_time = time.time()
    username = request.form.get('username')
    face = request.files.get('face')
    fingerprint = request.files.get('fingerprint')
    
    if not username or not face or not fingerprint:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Save temporary files
    temp_face_filename = secure_filename(f"temp_{username}_face_{int(time.time())}.{face.filename.rsplit('.', 1)[1]}")
    temp_face_path = os.path.join(UPLOAD_FOLDER, temp_face_filename)
    face.save(temp_face_path)
    
    temp_fp_filename = secure_filename(f"temp_{username}_fp_{int(time.time())}.{fingerprint.filename.rsplit('.', 1)[1]}")
    temp_fp_path = os.path.join(UPLOAD_FOLDER, temp_fp_filename)
    fingerprint.save(temp_fp_path)
    
    try:
        # Get user data
        conn = get_db()
        user = conn.execute('''SELECT face_paths, fp_path, security_level, biometric_quality 
                              FROM users WHERE username = ? AND is_active = 1''', 
                           (username,)).fetchone()
        
        if not user:
            conn.close()
            log_security_event('AUTH_FAILED', username, {'reason': 'User not found', 'attempt_type': 'dual'}, 'warning')
            return jsonify({'error': 'Authentication failed'}), 401
        
        # Perform face authentication
        stored_face_paths = user['face_paths'].split(',')
        face_result = face_recognizer.multi_algorithm_face_match(
            temp_face_path, stored_face_paths, user['security_level']
        )
        
        # Perform fingerprint authentication
        fp_result = fingerprint_recognizer.multi_algorithm_fingerprint_match(
            temp_fp_path, user['fp_path'], user['security_level']
        )
        
        # Fusion decision
        fusion_threshold = SECURITY_LEVELS[user['security_level']]['fusion_threshold']
        fusion_score = (face_result['overall_confidence'] + fp_result['overall_confidence']) / 2
        
        success = (face_result['passed_threshold'] and fp_result['passed_threshold'] and 
                  fusion_score >= fusion_threshold * 100)
        
        response_time = time.time() - start_time
        
        # Log authentication attempt
        conn.execute('''INSERT INTO auth_attempts 
                       (username, ip_address, attempt_type, success, algorithm_scores, 
                        overall_confidence, response_time) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (username, request.remote_addr, 'dual', success,
                     json.dumps({
                         'face': face_result['algorithm_scores'],
                         'fingerprint': fp_result['algorithm_scores'],
                         'fusion_score': fusion_score
                     }), fusion_score, response_time))
        
        if success:
            # Update user login info
            conn.execute('''UPDATE users 
                           SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1 
                           WHERE username = ?''', (username,))
            conn.commit()
            conn.close()
            
            log_security_event('DUAL_AUTH_SUCCESS', username, {
                'face_confidence': face_result['overall_confidence'],
                'fp_confidence': fp_result['overall_confidence'],
                'fusion_score': fusion_score,
                'response_time': response_time
            }, 'info')
            
            return jsonify({
                'success': True,
                'face_result': face_result,
                'fingerprint_result': fp_result,
                'fusion_score': fusion_score,
                'response_time': response_time,
                'message': 'Dual biometric authentication successful!'
            })
        else:
            conn.commit()
            conn.close()
            
            log_security_event('DUAL_AUTH_FAILED', username, {
                'face_confidence': face_result['overall_confidence'],
                'fp_confidence': fp_result['overall_confidence'],
                'fusion_score': fusion_score,
                'required': fusion_threshold * 100,
                'response_time': response_time
            }, 'warning')
            
            return jsonify({
                'success': False,
                'error': 'Dual biometric authentication failed',
                'face_result': face_result,
                'fingerprint_result': fp_result,
                'fusion_score': fusion_score,
                'required': fusion_threshold * 100
            }), 401
            
    finally:
        # Clean up temporary files
        for temp_path in [temp_face_path, temp_fp_path]:
            if os.path.exists(temp_path):
                os.remove(temp_path)

@app.route('/api/system/status', methods=['GET'])
def system_status():
    """Get system status and performance metrics"""
    try:
        conn = get_db()
        
        # Get user count
        user_count = conn.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1').fetchone()['count']
        
        # Get recent authentication attempts
        recent_auths = conn.execute('''SELECT attempt_type, success, AVG(overall_confidence) as avg_confidence,
                                      AVG(response_time) as avg_response_time, COUNT(*) as count
                                      FROM auth_attempts 
                                      WHERE timestamp > datetime('now', '-24 hours')
                                      GROUP BY attempt_type, success''').fetchall()
        
        # Get security events
        security_events = conn.execute('''SELECT severity, COUNT(*) as count
                                         FROM security_events 
                                         WHERE timestamp > datetime('now', '-24 hours')
                                         GROUP BY severity''').fetchall()
        
        conn.close()
        
        return jsonify({
            'status': 'online',
            'user_count': user_count,
            'recent_authentications': [dict(row) for row in recent_auths],
            'security_events': [dict(row) for row in security_events],
            'algorithms_available': {
                'face': ['deepface', 'resnet50', 'vgg16', 'inception', 'ensemble'],
                'fingerprint': ['hog', 'lbp', 'gabor', 'minutiae', 'ensemble']
            },
            'deepface_available': DEEPFACE_AVAILABLE,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("🚀 Starting Enhanced Ultimate Biometric Authentication System...")
    
    # Initialize database
    init_database()
    
    # Initialize AI models
    initialize_models()
    
    # Initialize recognizers
    init_recognizers()
    
    print("✅ System initialized successfully!")
    print("🔐 Security Levels Available:")
    for level, config in SECURITY_LEVELS.items():
        print(f"   {level}: Threshold {config['face_threshold']}, Algorithms: {config['algorithms']}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)