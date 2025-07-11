"""
Flask backend for Dual Biometric Authentication (Face + Fingerprint)
"""
import os
import sys
import sqlite3
import logging
import re

# Ensure biometrics package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from biometrics.face import find_most_similar
from biometrics.fingerprint import compare_fingerprints
from flask_cors import CORS  # <-- add this import

UPLOAD_FOLDER = 'webapp/uploads'
DB_PATH = 'webapp/users.db'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_FP_EXTENSIONS = {'bmp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, supports_credentials=True)  # <-- add supports_credentials for full CORS support
logging.basicConfig(level=logging.INFO)

def allowed_file(filename, allowed):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get('username')
    face = request.files.get('face')
    fingerprint = request.files.get('fingerprint')
    # Debug: log missing fields
    missing = []
    if not username:
        missing.append('username')
    if not face:
        missing.append('face')
    if not fingerprint:
        missing.append('fingerprint')
    if missing:
        logging.warning(f"Register missing fields: {missing}")
        return jsonify({'error': f"Missing fields: {', '.join(missing)}"}), 400
    if not (allowed_file(face.filename, ALLOWED_IMAGE_EXTENSIONS) and allowed_file(fingerprint.filename, ALLOWED_FP_EXTENSIONS)):
        return jsonify({'error': 'Invalid file type'}), 400
    face_path = os.path.join(UPLOAD_FOLDER, secure_filename(f"{username}_face.{face.filename.rsplit('.', 1)[1]}"))
    fp_path = os.path.join(UPLOAD_FOLDER, secure_filename(f"{username}_fp.{fingerprint.filename.rsplit('.', 1)[1]}"))
    face.save(face_path)
    fingerprint.save(fp_path)
    # Save user to DB
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, face_path, fp_path) VALUES (?, ?, ?)', (username, face_path, fp_path))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409
    finally:
        conn.close()
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/auth/face', methods=['POST'])
def auth_face():
    username = request.form.get('username')
    face = request.files.get('face')
    if not username or not face:
        return jsonify({'error': 'Missing fields'}), 400
    if not allowed_file(face.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    face_path = os.path.join(UPLOAD_FOLDER, secure_filename(f"temp_{username}_face.{face.filename.rsplit('.', 1)[1]}"))
    face.save(face_path)
    conn = get_db()
    user = conn.execute('SELECT face_path FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if not user:
        os.remove(face_path)
        return jsonify({'error': 'User not found'}), 404
    # Compare faces
    best_match, _ = find_most_similar(face_path, dataset_folder=os.path.dirname(user['face_path']), parallel=True)
    os.remove(face_path)
    if best_match and best_match['Confidence (%)'] > 70:
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Face not recognized'}), 401

@app.route('/api/auth/fingerprint', methods=['POST'])
def auth_fingerprint():
    username = request.form.get('username')
    fingerprint = request.files.get('fingerprint')
    if not username or not fingerprint:
        return jsonify({'error': 'Missing fields'}), 400
    if not allowed_file(fingerprint.filename, ALLOWED_FP_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    fp_path = os.path.join(UPLOAD_FOLDER, secure_filename(f"temp_{username}_fp.{fingerprint.filename.rsplit('.', 1)[1]}"))
    fingerprint.save(fp_path)
    conn = get_db()
    user = conn.execute('SELECT fp_path FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if not user:
        os.remove(fp_path)
        return jsonify({'error': 'User not found'}), 404
    # Compare fingerprints
    result = {'match': False}
    def log(msg):
        # Extract score using regex, works for both "Score=..." and "(Score: ...)"
        match = re.search(r'Score[:=]\s*([0-9.]+)', msg)
        if match:
            score = float(match.group(1))
            if score > 0.7:
                result['match'] = True
    compare_fingerprints(fp_path, dataset_path=os.path.dirname(user['fp_path']), log_callback=log, parallel=True)
    os.remove(fp_path)
    if result['match']:
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Fingerprint not recognized'}), 401

@app.route('/uploads/<filename>')
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