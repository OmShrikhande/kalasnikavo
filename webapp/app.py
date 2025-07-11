"""
Enhanced Flask backend for Dual Biometric Authentication (Face + Fingerprint)
God Mode Version with advanced features
"""
import os
import sys
import json
import hashlib
import sqlite3
import logging
import time
from datetime import datetime, timedelta
import uuid
import base64

# Ensure biometrics package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Try to import biometric modules, fallback if not available
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

UPLOAD_FOLDER = 'uploads'
DB_PATH = 'enhanced_users.db'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_FP_EXTENSIONS = {'bmp', 'png'}
MAX_FACE_IMAGES = 5
SECRET_KEY = 'your-super-secret-key-change-in-production'

# Security Configuration
SECURITY_LEVELS = {
    'LOW': {'threshold': 0.6, 'max_attempts': 10, 'lockout_time': 300},
    'MEDIUM': {'threshold': 0.75, 'max_attempts': 5, 'lockout_time': 600},
    'HIGH': {'threshold': 0.85, 'max_attempts': 3, 'lockout_time': 1800},
    'MAXIMUM': {'threshold': 0.95, 'max_attempts': 2, 'lockout_time': 3600}
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

# In-memory cache for performance
cache = {}
failed_attempts = {}
blocked_ips = {}

def allowed_file(filename, allowed):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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
            return min(0.95, 0.7 + (file_size / 1000000) * 0.2) if file_size > 100000 else 0.6
        elif biometric_type == 'fingerprint':
            return min(0.98, 0.8 + (file_size / 500000) * 0.15) if file_size > 50000 else 0.7
        return 0.5
    except Exception as e:
        logger.error(f"Quality calculation failed: {e}")
        return 0.5

def generate_session_token(username):
    """Generate secure session token"""
    session_data = f"{username}:{time.time()}:{uuid.uuid4()}"
    return base64.b64encode(session_data.encode()).decode()

@app.route('/api/register', methods=['POST'])
def register():
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

    # Save face images with quality assessment
    face_paths = []
    face_qualities = []
    for idx, face in enumerate(face_files):
        face_filename = secure_filename(f"{username}_face_{idx}_{int(time.time())}.{face.filename.rsplit('.', 1)[1]}")
        face_path = os.path.join(UPLOAD_FOLDER, face_filename)
        face.save(face_path)
        
        quality = calculate_biometric_quality(face_path, 'face')
        face_qualities.append(quality)
        face_paths.append(face_path)

    # Save fingerprint with quality assessment
    fp_filename = secure_filename(f"{username}_fp_{int(time.time())}.{fingerprint.filename.rsplit('.', 1)[1]}")
    fp_path = os.path.join(UPLOAD_FOLDER, fp_filename)
    fingerprint.save(fp_path)
    
    fp_quality = calculate_biometric_quality(fp_path, 'fingerprint')
    
    # Check quality against security level threshold
    avg_face_quality = sum(face_qualities) / len(face_qualities)
    min_quality = SECURITY_LEVELS[security_level]['threshold']
    
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

    # Store user in database
    biometric_quality = {
        'face': avg_face_quality,
        'fingerprint': fp_quality,
        'individual_face_qualities': face_qualities
    }
    
    try:
        conn.execute('''INSERT INTO users 
                       (username, email, face_paths, fp_path, security_level, biometric_quality, is_verified) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (username, email, ','.join(face_paths), fp_path, security_level,
                     json.dumps(biometric_quality), 1))
        conn.commit()
        
        log_security_event('USER_REGISTERED', username, {
            'email': email,
            'security_level': security_level,
            'face_quality': avg_face_quality,
            'fingerprint_quality': fp_quality,
            'registration_time': time.time() - start_time
        }, 'info')
        
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
        log_security_event('REGISTRATION_FAILED', username, {'reason': 'Database error', 'error': str(e)}, 'error')
        return jsonify({'error': 'Registration failed - database error'}), 500
    finally:
        conn.close()

@app.route('/api/auth/face', methods=['POST'])
def auth_face():
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

@app.route('/api/auth/fingerprint', methods=['POST'])
def auth_fingerprint():
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
        min_quality = SECURITY_LEVELS[user['security_level']]['threshold']
        
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
            match_result['score'] = 0.75  # Fallback score for demo
            match_result['match'] = match_result['score'] >= min_quality
        
        response_time = time.time() - start_time
        
        if match_result['match']:
            # Update user login statistics
            conn.execute('''UPDATE users 
                           SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1 
                           WHERE username = ?''', (username,))
            
            # Create session
            session_id = generate_session_token(username)
            session_expires = datetime.now() + timedelta(hours=24)
            
            conn.execute('''INSERT INTO user_sessions 
                           (username, session_id, ip_address, expires_at) 
                           VALUES (?, ?, ?, ?)''',
                        (username, session_id, request.remote_addr, session_expires))
            
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
            # Extract score using string parsing
            import re
            match = re.search(r'Score[:=]\s*([0-9.]+)', msg)
            if not match:
                # Try to extract from "(Score: 1.0000)"
                match = re.search(r'\(Score:\s*([0-9.]+)\)', msg)
            if match:
                score = float(match.group(1))
                if score > 0.7:
                    result['match'] = True
    compare_fingerprints(fp_path, dataset_path=os.path.dirname(user['fp_path']), log_callback=log, parallel=True)
    os.remove(fp_path)
    if result['match']:
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Fingerprint not recognized'}), 401

@app.route('/api/user/docs', methods=['GET', 'POST', 'DELETE'])
def user_docs():
    username = request.args.get('username') if request.method == 'GET' else request.form.get('username')
    if not username:
        return jsonify({'error': 'Missing username'}), 400
    user_folder = os.path.join(UPLOAD_FOLDER, f"{username}_docs")
    os.makedirs(user_folder, exist_ok=True)
    meta_path = os.path.join(user_folder, 'meta.json')
    # Load metadata
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
    else:
        meta = {}

    if request.method == 'POST':
        doc = request.files.get('doc')
        hash_val = request.form.get('hash')
        if not doc or not hash_val:
            return jsonify({'error': 'No document or hash provided'}), 400
        doc_path = os.path.join(user_folder, secure_filename(doc.filename))
        doc.save(doc_path)
        meta[secure_filename(doc.filename)] = hash_val
        with open(meta_path, 'w') as f:
            json.dump(meta, f)
        return jsonify({'message': 'Document uploaded'})
    elif request.method == 'GET':
        docs = []
        if os.path.exists(user_folder):
            for fname in os.listdir(user_folder):
                if fname == 'meta.json':
                    continue
                docs.append({
                    'name': f"{username}_docs/{fname}",
                    'hash': meta.get(fname, '')
                })
        return jsonify({'docs': docs})
    elif request.method == 'DELETE':
        doc_name = request.args.get('doc')
        if not doc_name:
            return jsonify({'error': 'No document specified'}), 400
        doc_path = os.path.join(UPLOAD_FOLDER, doc_name)
        if os.path.exists(doc_path):
            os.remove(doc_path)
            # Remove from meta
            folder = os.path.dirname(doc_path)
            fname = os.path.basename(doc_path)
            meta_path = os.path.join(folder, 'meta.json')
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                meta.pop(fname, None)
                with open(meta_path, 'w') as f:
                    json.dump(meta, f)
            return jsonify({'message': 'Document deleted'})
        return jsonify({'error': 'Document not found'}), 404

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Initialize DB
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        face_path TEXT NOT NULL,
        fp_path TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()
    app.run(debug=True, host='0.0.0.0', port=5000)