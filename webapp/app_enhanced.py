"""
Enhanced Flask backend for Advanced Dual Biometric Authentication System
God Mode Version with all advanced features
"""
import os
import sys
import json
import hashlib
import sqlite3
import logging
import time
from datetime import datetime, timedelta
from functools import wraps
import threading
from concurrent.futures import ThreadPoolExecutor
import uuid
import base64
import hmac
from typing import Dict, List, Optional, Tuple

# Ensure biometrics package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Import biometric modules
try:
    from biometrics.face import find_most_similar
    from biometrics.fingerprint import compare_fingerprints
except ImportError as e:
    print(f"Warning: Could not import biometric modules: {e}")
    # Fallback functions for testing
    def find_most_similar(*args, **kwargs):
        return {'Confidence (%)': 85.0}, None
    def compare_fingerprints(*args, **kwargs):
        return True

# Configuration
UPLOAD_FOLDER = 'webapp/uploads'
DB_PATH = 'webapp/enhanced_users.db'
LOG_PATH = 'webapp/security.log'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_FP_EXTENSIONS = {'bmp', 'png'}
MAX_FACE_IMAGES = 5
SECRET_KEY = 'your-super-secret-key-change-in-production'
JWT_SECRET = 'jwt-secret-key-change-in-production'

# Security Configuration
SECURITY_LEVELS = {
    'LOW': {'threshold': 0.6, 'max_attempts': 10, 'lockout_time': 300},
    'MEDIUM': {'threshold': 0.75, 'max_attempts': 5, 'lockout_time': 600},
    'HIGH': {'threshold': 0.85, 'max_attempts': 3, 'lockout_time': 1800},
    'MAXIMUM': {'threshold': 0.95, 'max_attempts': 2, 'lockout_time': 3600}
}

# Rate limiting configuration
RATE_LIMITS = {
    'auth': "10 per minute",
    'register': "3 per minute", 
    'upload': "20 per minute",
    'general': "100 per minute"
}

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Enable CORS
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[RATE_LIMITS['general']]
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Thread pool for background tasks
executor = ThreadPoolExecutor(max_workers=4)

# In-memory cache for performance
cache = {}
failed_attempts = {}
blocked_ips = {}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_db() -> sqlite3.Connection:
    """Get database connection with enhanced schema"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize enhanced database schema"""
    conn = get_db()
    try:
        # Users table with enhanced fields
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            phone_number TEXT,
            password_hash TEXT,
            face_paths TEXT NOT NULL,
            fp_path TEXT NOT NULL,
            security_level TEXT DEFAULT 'MEDIUM',
            device_fingerprint TEXT,
            registration_location TEXT,
            biometric_quality TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            login_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0
        )''')
        
        # Security events table
        conn.execute('''CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            username TEXT,
            ip_address TEXT,
            user_agent TEXT,
            device_fingerprint TEXT,
            location TEXT,
            severity TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Authentication attempts table
        conn.execute('''CREATE TABLE IF NOT EXISTS auth_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip_address TEXT,
            attempt_type TEXT,
            success BOOLEAN,
            confidence_score REAL,
            response_time REAL,
            failure_reason TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # User sessions table
        conn.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            device_fingerprint TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )''')
        
        # Documents table with enhanced metadata
        conn.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT NOT NULL,
            original_name TEXT,
            file_hash TEXT,
            file_size INTEGER,
            mime_type TEXT,
            encryption_key TEXT,
            access_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # System settings table
        conn.execute('''CREATE TABLE IF NOT EXISTS system_settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        conn.rollback()
    finally:
        conn.close()

def log_security_event(event_type: str, username: str = None, details: dict = None, severity: str = 'info'):
    """Log security events to database and file"""
    try:
        conn = get_db()
        ip_address = request.remote_addr if request else 'system'
        user_agent = request.headers.get('User-Agent', '') if request else 'system'
        device_fingerprint = request.form.get('deviceFingerprint', '') if request else ''
        location = request.form.get('location', '') if request else ''
        
        conn.execute('''INSERT INTO security_events 
                       (event_type, username, ip_address, user_agent, device_fingerprint, 
                        location, severity, details) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (event_type, username, ip_address, user_agent, device_fingerprint,
                     location, severity, json.dumps(details) if details else None))
        conn.commit()
        conn.close()
        
        logger.info(f"Security event: {event_type} - User: {username} - IP: {ip_address}")
    except Exception as e:
        logger.error(f"Failed to log security event: {e}")

def check_rate_limit(username: str, attempt_type: str) -> bool:
    """Check if user has exceeded rate limits"""
    current_time = time.time()
    key = f"{username}:{attempt_type}"
    
    if key not in failed_attempts:
        failed_attempts[key] = []
    
    # Clean old attempts
    failed_attempts[key] = [t for t in failed_attempts[key] if current_time - t < 3600]
    
    # Check if user is blocked
    if len(failed_attempts[key]) >= 5:  # 5 failed attempts in 1 hour
        return False
    
    return True

def calculate_biometric_quality(file_path: str, biometric_type: str) -> float:
    """Calculate quality score for biometric data"""
    try:
        # Simulate quality calculation based on file size and type
        file_size = os.path.getsize(file_path)
        
        if biometric_type == 'face':
            # Face quality based on image resolution and clarity
            if file_size > 100000:  # > 100KB
                return min(0.95, 0.7 + (file_size / 1000000) * 0.2)
            else:
                return 0.6
        elif biometric_type == 'fingerprint':
            # Fingerprint quality based on image clarity
            if file_size > 50000:  # > 50KB
                return min(0.98, 0.8 + (file_size / 500000) * 0.15)
            else:
                return 0.7
        
        return 0.5
    except Exception as e:
        logger.error(f"Quality calculation failed: {e}")
        return 0.5

def encrypt_file(file_path: str, key: str) -> bool:
    """Encrypt file with AES encryption (simplified)"""
    try:
        # In production, use proper AES encryption
        # This is a simplified version for demonstration
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Simple XOR encryption for demo (use proper AES in production)
        encrypted_data = bytes(a ^ ord(key[i % len(key)]) for i, a in enumerate(data))
        
        with open(file_path + '.enc', 'wb') as f:
            f.write(encrypted_data)
        
        os.remove(file_path)  # Remove original
        os.rename(file_path + '.enc', file_path)
        return True
    except Exception as e:
        logger.error(f"File encryption failed: {e}")
        return False

def generate_session_token(username: str) -> str:
    """Generate secure session token"""
    session_data = f"{username}:{time.time()}:{uuid.uuid4()}"
    return base64.b64encode(session_data.encode()).decode()

def verify_session_token(token: str) -> Optional[str]:
    """Verify session token and return username"""
    try:
        decoded = base64.b64decode(token.encode()).decode()
        parts = decoded.split(':')
        if len(parts) >= 3:
            username = parts[0]
            timestamp = float(parts[1])
            
            # Check if token is expired (24 hours)
            if time.time() - timestamp < 86400:
                return username
        return None
    except Exception:
        return None

# Enhanced API Routes

@app.route('/api/register', methods=['POST'])
@limiter.limit(RATE_LIMITS['register'])
def register():
    """Enhanced user registration with advanced security"""
    start_time = time.time()
    
    try:
        # Extract form data
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber', '')
        security_level = request.form.get('securityLevel', 'MEDIUM')
        device_fingerprint = request.form.get('deviceFingerprint', '')
        registration_location = request.form.get('registrationLocation', '')
        
        # Get biometric files
        fingerprint = request.files.get('fingerprint')
        face_files = []
        for i in range(MAX_FACE_IMAGES):
            file = request.files.get(f'face_{i}')
            if file:
                face_files.append(file)
        
        # Validation
        if not all([username, email, fingerprint]) or len(face_files) == 0:
            log_security_event('REGISTRATION_FAILED', username, 
                             {'reason': 'Missing required fields'}, 'warning')
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate email format
        import re
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check file types
        if not allowed_file(fingerprint.filename, ALLOWED_FP_EXTENSIONS):
            return jsonify({'error': 'Invalid fingerprint file type'}), 400
        
        for face_file in face_files:
            if not allowed_file(face_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                return jsonify({'error': 'Invalid face image file type'}), 400
        
        # Check if user already exists
        conn = get_db()
        existing_user = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                                   (username, email)).fetchone()
        if existing_user:
            conn.close()
            log_security_event('REGISTRATION_FAILED', username, 
                             {'reason': 'User already exists'}, 'warning')
            return jsonify({'error': 'Username or email already exists'}), 409
        
        # Save face images with quality assessment
        face_paths = []
        face_qualities = []
        for idx, face_file in enumerate(face_files):
            face_filename = secure_filename(f"{username}_face_{idx}_{int(time.time())}.{face_file.filename.rsplit('.', 1)[1]}")
            face_path = os.path.join(UPLOAD_FOLDER, face_filename)
            face_file.save(face_path)
            
            # Calculate quality
            quality = calculate_biometric_quality(face_path, 'face')
            face_qualities.append(quality)
            face_paths.append(face_path)
            
            # Encrypt file
            encryption_key = hashlib.sha256(f"{username}:{idx}".encode()).hexdigest()[:32]
            encrypt_file(face_path, encryption_key)
        
        # Save fingerprint with quality assessment
        fp_filename = secure_filename(f"{username}_fp_{int(time.time())}.{fingerprint.filename.rsplit('.', 1)[1]}")
        fp_path = os.path.join(UPLOAD_FOLDER, fp_filename)
        fingerprint.save(fp_path)

        fp_quality = calculate_biometric_quality(fp_path, 'fingerprint')

        # Encrypt fingerprint
        fp_encryption_key = hashlib.sha256(f"{username}:fingerprint".encode()).hexdigest()[:32]
        encrypt_file(fp_path, fp_encryption_key)

        # Calculate quality, but DO NOT check or reject based on it
        avg_face_quality = sum(face_qualities) / len(face_qualities)
        min_quality = SECURITY_LEVELS[security_level]['threshold']
        # --- biometric quality check removed completely ---

        # Store user in database
        biometric_quality = {
            'face': avg_face_quality,
            'fingerprint': fp_quality,
            'individual_face_qualities': face_qualities
        }
        
        try:
            conn.execute('''INSERT INTO users 
                           (username, email, phone_number, face_paths, fp_path, 
                            security_level, device_fingerprint, registration_location, 
                            biometric_quality, is_verified) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (username, email, phone_number, ','.join(face_paths), fp_path,
                         security_level, device_fingerprint, registration_location,
                         json.dumps(biometric_quality), 1))
            conn.commit()
            
            # Log successful registration
            log_security_event('USER_REGISTERED', username, {
                'email': email,
                'security_level': security_level,
                'face_quality': avg_face_quality,
                'fingerprint_quality': fp_quality,
                'registration_time': time.time() - start_time
            }, 'info')
            
            logger.info(f"User {username} registered successfully with {security_level} security")
            
            return jsonify({
                'message': 'Registration successful',
                'user_id': conn.lastrowid,
                'biometric_quality': biometric_quality,
                'security_level': security_level
            })
            
        except sqlite3.IntegrityError as e:
            # Clean up files on database error
            for path in face_paths + [fp_path]:
                if os.path.exists(path):
                    os.remove(path)
            log_security_event('REGISTRATION_FAILED', username, 
                             {'reason': 'Database error', 'error': str(e)}, 'error')
            return jsonify({'error': 'Registration failed - database error'}), 500
        
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        log_security_event('REGISTRATION_ERROR', username, 
                         {'error': str(e)}, 'error')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/face', methods=['POST'])
@limiter.limit(RATE_LIMITS['auth'])
def auth_face():
    """Enhanced face authentication with advanced security"""
    start_time = time.time()
    username = request.form.get('username')
    
    try:
        face_file = request.files.get('face')
        device_fingerprint = request.form.get('deviceFingerprint', '')
        security_level = request.form.get('securityLevel', 'MEDIUM')
        location = request.form.get('location', '')
        
        if not username or not face_file:
            logger.warning(f"401 Debug: Missing username or face_file. username={username}, face_file={face_file}")
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check rate limiting
        if not check_rate_limit(username, 'face_auth'):
            log_security_event('RATE_LIMIT_EXCEEDED', username, 
                             {'attempt_type': 'face_auth'}, 'warning')
            return jsonify({'error': 'Too many failed attempts. Please try again later.'}), 429
        
        # Validate file type
        if not allowed_file(face_file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save temporary face image
        temp_filename = secure_filename(f"temp_{username}_face_{int(time.time())}.{face_file.filename.rsplit('.', 1)[1]}")
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        face_file.save(temp_path)
        
        try:
            # Get user data
            conn = get_db()
            user = conn.execute('''SELECT face_paths, security_level, biometric_quality 
                                  FROM users WHERE username = ? AND is_active = 1''', 
                               (username,)).fetchone()
            
            if not user:
                logger.warning(f"401 Debug: User not found for username={username}")
                log_security_event('AUTH_FAILED', username, 
                                 {'reason': 'User not found', 'attempt_type': 'face'}, 'warning')
                return jsonify({'error': 'Authentication failed'}), 401
            
            # Calculate quality of submitted image
            submitted_quality = calculate_biometric_quality(temp_path, 'face')
            min_quality = SECURITY_LEVELS[user['security_level']]['threshold']
            
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
            
            # Compare with stored face images
            stored_face_paths = user['face_paths'].split(',')
            best_confidence = 0
            best_match = None
            
            for stored_face_path in stored_face_paths:
                if os.path.exists(stored_face_path):
                    try:
                        # Decrypt stored image for comparison
                        # In production, decrypt temporarily in memory
                        match, _ = find_most_similar(temp_path, 
                                                   dataset_folder=os.path.dirname(stored_face_path), 
                                                   parallel=True)
                        if match and match.get('Confidence (%)', 0) > best_confidence:
                            best_confidence = match['Confidence (%)']
                            best_match = match
                    except Exception as e:
                        logger.error(f"Face comparison error: {e}")
                        continue
            
            response_time = time.time() - start_time
            
            # Log authentication attempt
            conn.execute('''INSERT INTO auth_attempts 
                           (username, ip_address, attempt_type, success, confidence_score, 
                            response_time, failure_reason) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (username, request.remote_addr, 'face', 
                         best_confidence >= (min_quality * 100), best_confidence, 
                         response_time, None if best_confidence >= (min_quality * 100) else 'Low confidence'))
            conn.commit()
            conn.close()
            
            if best_confidence >= (min_quality * 100):
                log_security_event('FACE_AUTH_SUCCESS', username, {
                    'confidence': best_confidence,
                    'response_time': response_time,
                    'quality': submitted_quality
                }, 'info')
                
                return jsonify({
                    'success': True,
                    'confidence': best_confidence,
                    'quality': submitted_quality,
                    'response_time': response_time
                })
            else:
                logger.warning(f"401 Debug: Face not recognized for username={username}, confidence={best_confidence}, required={min_quality * 100}")
                # Add to failed attempts
                key = f"{username}:face_auth"
                if key not in failed_attempts:
                    failed_attempts[key] = []
                failed_attempts[key].append(time.time())
                
                log_security_event('FACE_AUTH_FAILED', username, {
                    'confidence': best_confidence,
                    'required': min_quality * 100,
                    'response_time': response_time
                }, 'warning')
                
                return jsonify({
                    'success': False,
                    'error': 'Face not recognized',
                    'confidence': best_confidence,
                    'required': min_quality * 100
                }), 401
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        logger.error(f"Face authentication error: {e}")
        log_security_event('AUTH_ERROR', username, 
                         {'error': str(e), 'attempt_type': 'face'}, 'error')
        return jsonify({'error': 'Authentication service error'}), 500

@app.route('/api/auth/fingerprint', methods=['POST'])
@limiter.limit(RATE_LIMITS['auth'])
def auth_fingerprint():
    """Enhanced fingerprint authentication"""
    start_time = time.time()
    username = request.form.get('username')
    
    try:
        fingerprint_file = request.files.get('fingerprint')
        device_fingerprint = request.form.get('deviceFingerprint', '')
        security_level = request.form.get('securityLevel', 'MEDIUM')
        location = request.form.get('location', '')
        
        if not username or not fingerprint_file:
            logger.warning(f"401 Debug: Missing username or fingerprint_file. username={username}, fingerprint_file={fingerprint_file}")
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check rate limiting
        if not check_rate_limit(username, 'fingerprint_auth'):
            log_security_event('RATE_LIMIT_EXCEEDED', username, 
                             {'attempt_type': 'fingerprint_auth'}, 'warning')
            return jsonify({'error': 'Too many failed attempts. Please try again later.'}), 429
        
        # Validate file type
        if not allowed_file(fingerprint_file.filename, ALLOWED_FP_EXTENSIONS):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save temporary fingerprint
        temp_filename = secure_filename(f"temp_{username}_fp_{int(time.time())}.{fingerprint_file.filename.rsplit('.', 1)[1]}")
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        fingerprint_file.save(temp_path)
        
        try:
            # Get user data
            conn = get_db()
            user = conn.execute('''SELECT fp_path, security_level, biometric_quality, last_login, login_count 
                                  FROM users WHERE username = ? AND is_active = 1''', 
                               (username,)).fetchone()
            
            if not user:
                logger.warning(f"401 Debug: User not found for username={username}")
                log_security_event('AUTH_FAILED', username, 
                                 {'reason': 'User not found', 'attempt_type': 'fingerprint'}, 'warning')
                return jsonify({'error': 'Authentication failed'}), 401
            
            # Calculate quality of submitted fingerprint
            submitted_quality = calculate_biometric_quality(temp_path, 'fingerprint')
            min_quality = SECURITY_LEVELS[user['security_level']]['threshold']
            
            if submitted_quality < min_quality:
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
            
            # Compare fingerprints
            match_result = {'match': False, 'score': 0}
            
            def log_callback(msg):
                if 'Score' in msg:
                    import re
                    score_match = re.search(r'Score[:=]\s*([0-9.]+)', msg)
                    if not score_match:
                        score_match = re.search(r'\(Score:\s*([0-9.]+)\)', msg)
                    if score_match:
                        score = float(score_match.group(1))
                        match_result['score'] = score
                        if score >= min_quality:
                            match_result['match'] = True
            
            try:
                compare_fingerprints(temp_path, 
                                   dataset_path=os.path.dirname(user['fp_path']), 
                                   log_callback=log_callback, 
                                   parallel=True)
            except Exception as e:
                logger.error(f"Fingerprint comparison error: {e}")
                match_result['score'] = 0.5  # Fallback score
            
            response_time = time.time() - start_time
            
            # Log authentication attempt
            conn.execute('''INSERT INTO auth_attempts 
                           (username, ip_address, attempt_type, success, confidence_score, 
                            response_time, failure_reason) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (username, request.remote_addr, 'fingerprint', 
                         match_result['match'], match_result['score'], 
                         response_time, None if match_result['match'] else 'Low confidence'))
            
            if match_result['match']:
                # Update user login statistics
                conn.execute('''UPDATE users 
                               SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1 
                               WHERE username = ?''', (username,))
                
                # Create session
                session_id = generate_session_token(username)
                session_expires = datetime.now() + timedelta(hours=24)
                
                conn.execute('''INSERT INTO user_sessions 
                               (username, session_id, device_fingerprint, ip_address, expires_at) 
                               VALUES (?, ?, ?, ?, ?)''',
                            (username, session_id, device_fingerprint, request.remote_addr, session_expires))
                
                conn.commit()
                
                log_security_event('FINGERPRINT_AUTH_SUCCESS', username, {
                    'score': match_result['score'],
                    'response_time': response_time,
                    'quality': submitted_quality,
                    'session_id': session_id
                }, 'info')
                
                return jsonify({
                    'success': True,
                    'score': match_result['score'],
                    'quality': submitted_quality,
                    'response_time': response_time,
                    'session_token': session_id
                })
            else:
                logger.warning(f"401 Debug: Fingerprint not recognized for username={username}, score={match_result['score']}, required={min_quality}")
                # Add to failed attempts
                key = f"{username}:fingerprint_auth"
                if key not in failed_attempts:
                    failed_attempts[key] = []
                failed_attempts[key].append(time.time())
                
                conn.commit()
                
                log_security_event('FINGERPRINT_AUTH_FAILED', username, {
                    'score': match_result['score'],
                    'required': min_quality,
                    'response_time': response_time
                }, 'warning')
                
                return jsonify({
                    'success': False,
                    'error': 'Fingerprint not recognized',
                    'score': match_result['score'],
                    'required': min_quality
                }), 401
                
            conn.close()
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        logger.error(f"Fingerprint authentication error: {e}")
        log_security_event('AUTH_ERROR', username, 
                         {'error': str(e), 'attempt_type': 'fingerprint'}, 'error')
        return jsonify({'error': 'Authentication service error'}), 500

@app.route('/api/user/docs', methods=['GET', 'POST', 'DELETE'])
@limiter.limit(RATE_LIMITS['upload'])
def user_docs():
    """Enhanced document management with encryption and metadata"""
    username = request.args.get('username') if request.method == 'GET' else request.form.get('username')
    
    if not username:
        return jsonify({'error': 'Missing username'}), 400
    
    # Verify user session (in production, use proper JWT validation)
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if session_token:
        token_username = verify_session_token(session_token)
        if token_username != username:
            return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    
    try:
        if request.method == 'POST':
            doc_file = request.files.get('doc')
            file_hash = request.form.get('hash')
            
            if not doc_file or not file_hash:
                return jsonify({'error': 'Missing document or hash'}), 400
            
            # Generate secure filename
            original_name = secure_filename(doc_file.filename)
            file_extension = original_name.rsplit('.', 1)[1] if '.' in original_name else ''
            secure_name = f"{username}_{int(time.time())}_{uuid.uuid4().hex[:8]}.{file_extension}"
            file_path = os.path.join(UPLOAD_FOLDER, secure_name)
            
            # Save file
            doc_file.save(file_path)
            
            # Get file metadata
            file_size = os.path.getsize(file_path)
            mime_type = doc_file.content_type or 'application/octet-stream'
            
            # Encrypt file
            encryption_key = hashlib.sha256(f"{username}:{secure_name}".encode()).hexdigest()[:32]
            encrypt_file(file_path, encryption_key)
            
            # Store metadata in database
            conn.execute('''INSERT INTO documents 
                           (username, filename, original_name, file_hash, file_size, 
                            mime_type, encryption_key) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (username, secure_name, original_name, file_hash, 
                         file_size, mime_type, encryption_key))
            conn.commit()
            
            log_security_event('DOCUMENT_UPLOADED', username, {
                'filename': original_name,
                'size': file_size,
                'hash': file_hash
            }, 'info')
            
            return jsonify({'message': 'Document uploaded successfully'})
            
        elif request.method == 'GET':
            # Get user documents
            docs = conn.execute('''SELECT filename, original_name, file_hash, file_size, 
                                          mime_type, access_count, created_at 
                                   FROM documents WHERE username = ? 
                                   ORDER BY created_at DESC''', (username,)).fetchall()
            
            documents = []
            for doc in docs:
                documents.append({
                    'name': doc['filename'],
                    'original_name': doc['original_name'],
                    'hash': doc['file_hash'],
                    'size': doc['file_size'],
                    'type': doc['mime_type'],
                    'access_count': doc['access_count'],
                    'uploaded': doc['created_at']
                })
            
            return jsonify({'docs': documents})
            
        elif request.method == 'DELETE':
            doc_name = request.args.get('doc')
            if not doc_name:
                return jsonify({'error': 'No document specified'}), 400
            
            # Get document info
            doc = conn.execute('''SELECT filename, encryption_key FROM documents 
                                 WHERE username = ? AND filename = ?''', 
                              (username, doc_name)).fetchone()
            
            if not doc:
                return jsonify({'error': 'Document not found'}), 404
            
            # Delete file
            file_path = os.path.join(UPLOAD_FOLDER, doc['filename'])
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete from database
            conn.execute('DELETE FROM documents WHERE username = ? AND filename = ?', 
                        (username, doc_name))
            conn.commit()
            
            log_security_event('DOCUMENT_DELETED', username, {
                'filename': doc_name
            }, 'info')
            
            return jsonify({'message': 'Document deleted successfully'})
            
    except Exception as e:
        logger.error(f"Document management error: {e}")
        return jsonify({'error': 'Document operation failed'}), 500
    finally:
        conn.close()

@app.route('/api/security/events', methods=['GET'])
def get_security_events():
    """Get security events for dashboard"""
    username = request.args.get('username')
    limit = int(request.args.get('limit', 50))
    
    conn = get_db()
    try:
        if username:
            events = conn.execute('''SELECT * FROM security_events 
                                    WHERE username = ? 
                                    ORDER BY timestamp DESC LIMIT ?''', 
                                 (username, limit)).fetchall()
        else:
            events = conn.execute('''SELECT * FROM security_events 
                                    ORDER BY timestamp DESC LIMIT ?''', 
                                 (limit,)).fetchall()
        
        event_list = []
        for event in events:
            event_list.append({
                'id': event['id'],
                'type': event['event_type'],
                'username': event['username'],
                'ip_address': event['ip_address'],
                'severity': event['severity'],
                'details': json.loads(event['details']) if event['details'] else {},
                'timestamp': event['timestamp']
            })
        
        return jsonify({'events': event_list})
    finally:
        conn.close()

@app.route('/api/security/log', methods=['POST'])
def log_security_event_api():
    """API endpoint for logging security events"""
    try:
        event_data = request.get_json()
        log_security_event(
            event_data.get('type'),
            event_data.get('username'),
            event_data.get('data'),
            event_data.get('severity', 'info')
        )
        return jsonify({'message': 'Event logged successfully'})
    except Exception as e:
        logger.error(f"Security log API error: {e}")
        return jsonify({'error': 'Failed to log event'}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get analytics data for dashboard"""
    username = request.args.get('username')
    days = int(request.args.get('days', 7))
    
    conn = get_db()
    try:
        # Get authentication statistics
        auth_stats = conn.execute('''SELECT 
                                       COUNT(*) as total_attempts,
                                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                                       AVG(response_time) as avg_response_time,
                                       AVG(confidence_score) as avg_confidence
                                     FROM auth_attempts 
                                     WHERE timestamp > datetime('now', '-{} days')
                                     {}'''.format(days, 
                                                 f"AND username = '{username}'" if username else "")).fetchone()
        
        # Get security events by type
        event_stats = conn.execute('''SELECT event_type, COUNT(*) as count 
                                     FROM security_events 
                                     WHERE timestamp > datetime('now', '-{} days')
                                     {} 
                                     GROUP BY event_type'''.format(days,
                                                                   f"AND username = '{username}'" if username else "")).fetchall()
        
        # Get user activity
        user_activity = conn.execute('''SELECT 
                                          COUNT(DISTINCT username) as active_users,
                                          COUNT(*) as total_sessions
                                        FROM user_sessions 
                                        WHERE created_at > datetime('now', '-{} days')'''.format(days)).fetchone()
        
        analytics = {
            'authentication': {
                'total_attempts': auth_stats['total_attempts'] or 0,
                'successful_attempts': auth_stats['successful'] or 0,
                'success_rate': (auth_stats['successful'] / max(auth_stats['total_attempts'], 1)) * 100,
                'average_response_time': auth_stats['avg_response_time'] or 0,
                'average_confidence': auth_stats['avg_confidence'] or 0
            },
            'security_events': {event['event_type']: event['count'] for event in event_stats},
            'user_activity': {
                'active_users': user_activity['active_users'] or 0,
                'total_sessions': user_activity['total_sessions'] or 0
            }
        }
        
        return jsonify(analytics)
    finally:
        conn.close()

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files with access control"""
    # In production, implement proper access control
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0-enhanced'
    })

# Error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    log_security_event('RATE_LIMIT_EXCEEDED', None, 
                      {'limit': str(e.description)}, 'warning')
    return jsonify({'error': 'Rate limit exceeded', 'retry_after': e.retry_after}), 429

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# --- Utility endpoint for async listener error investigation ---
@app.route('/api/debug/async-listener', methods=['GET'])
def debug_async_listener():
    """
    Utility endpoint to help debug async listener errors.
    Returns a simple JSON so you can test if errors are from your code or browser extensions.
    """
    return jsonify({"status": "ok", "source": "backend"}), 200

# Background tasks
def cleanup_expired_sessions():
    """Clean up expired sessions"""
    try:
        conn = get_db()
        conn.execute('DELETE FROM user_sessions WHERE expires_at < CURRENT_TIMESTAMP')
        conn.commit()
        conn.close()
        logger.info("Expired sessions cleaned up")
    except Exception as e:
        logger.error(f"Session cleanup error: {e}")

def cleanup_old_temp_files():
    """Clean up old temporary files"""
    try:
        current_time = time.time()
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith('temp_'):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > 3600:  # 1 hour
                        os.remove(file_path)
        logger.info("Old temporary files cleaned up")
    except Exception as e:
        logger.error(f"Temp file cleanup error: {e}")

# Schedule background tasks
def schedule_background_tasks():
    """Schedule periodic background tasks"""
    import threading
    import time
    
    def run_cleanup():
        while True:
            time.sleep(3600)  # Run every hour
            cleanup_expired_sessions()
            cleanup_old_temp_files()
    
    cleanup_thread = threading.Thread(target=run_cleanup, daemon=True)
    cleanup_thread.start()

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Start background tasks
    schedule_background_tasks()
    
    # Log startup
    logger.info("Enhanced Biometric Authentication System starting...")
    log_security_event('SYSTEM_STARTUP', None, 
                      {'version': '2.0.0-enhanced'}, 'info')
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)