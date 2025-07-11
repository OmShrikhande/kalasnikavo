#!/usr/bin/env python3
"""
Setup script for Advanced Dual Biometric Authentication System
God Mode Version - Automated Installation and Configuration
"""

import os
import sys
import subprocess
import sqlite3
import json
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🔐 Advanced Dual Biometric Authentication System          ║
    ║                     GOD MODE SETUP                          ║
    ║                                                              ║
    ║    🚀 Ultimate Security • 🎨 Modern UI • 📊 Analytics       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_node_version():
    """Check Node.js version"""
    print("📦 Checking Node.js version...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} detected")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    
    dependencies = [
        'flask>=2.0.0',
        'flask-cors>=3.0.0',
        'flask-limiter>=2.0.0',
        'opencv-python>=4.5.0',
        'numpy>=1.21.0',
        'pillow>=8.0.0',
        'werkzeug>=2.0.0',
        'sqlite3',  # Usually built-in
        'hashlib',  # Built-in
        'hmac',     # Built-in
        'base64',   # Built-in
        'threading', # Built-in
        'uuid',     # Built-in
        'datetime', # Built-in
        'functools', # Built-in
        'logging',  # Built-in
        'concurrent.futures', # Built-in
    ]
    
    # Filter out built-in modules
    pip_dependencies = [dep for dep in dependencies if not dep in [
        'sqlite3', 'hashlib', 'hmac', 'base64', 'threading', 
        'uuid', 'datetime', 'functools', 'logging', 'concurrent.futures'
    ]]
    
    try:
        for dep in pip_dependencies:
            print(f"  Installing {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("📦 Installing Node.js dependencies...")
    try:
        subprocess.run(['npm', 'install'], check=True, cwd='.')
        print("✅ Node.js dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        'uploads',
        'logs',
        'backups',
        'temp',
        'models',  # For AI models
        'certificates',  # For SSL certificates
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created {directory}/")
    
    return True

def setup_database():
    """Initialize the database"""
    print("🗄️ Setting up database...")
    
    db_path = 'enhanced_users.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Users table with enhanced fields
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS security_events (
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS auth_attempts (
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            device_fingerprint TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )''')
        
        # Documents table
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_security_events_timestamp ON security_events(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_auth_attempts_username ON auth_attempts(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_sessions_username ON user_sessions(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_username ON documents(username)')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_config_file():
    """Create configuration file"""
    print("⚙️ Creating configuration file...")
    
    config = {
        "app": {
            "name": "Advanced Biometric Authentication System",
            "version": "2.0.0",
            "debug": True,
            "host": "0.0.0.0",
            "port": 5000
        },
        "security": {
            "secret_key": "change-this-in-production",
            "jwt_secret": "change-this-jwt-secret",
            "session_timeout": 3600,
            "max_login_attempts": 5,
            "lockout_duration": 300
        },
        "biometrics": {
            "face_threshold": 0.75,
            "fingerprint_threshold": 0.80,
            "max_face_images": 5,
            "quality_threshold": 0.70
        },
        "storage": {
            "upload_folder": "uploads",
            "max_file_size": 52428800,
            "allowed_image_extensions": ["png", "jpg", "jpeg", "webp"],
            "allowed_fp_extensions": ["bmp", "png"]
        },
        "database": {
            "path": "enhanced_users.db",
            "backup_interval": 86400,
            "cleanup_interval": 3600
        },
        "logging": {
            "level": "INFO",
            "file": "logs/app.log",
            "max_size": 10485760,
            "backup_count": 5
        }
    }
    
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("✅ Configuration file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def create_environment_file():
    """Create environment file"""
    print("🌍 Creating environment file...")
    
    env_content = """# Advanced Biometric Authentication System - Environment Variables

# Flask Configuration
FLASK_ENV=development
FLASK_APP=app_enhanced.py
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-key-change-in-production

# Database Configuration
DB_PATH=enhanced_users.db
DB_BACKUP_PATH=backups/

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800

# Security Configuration
SECURITY_LEVEL=MEDIUM
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=300

# Biometric Configuration
FACE_THRESHOLD=0.75
FINGERPRINT_THRESHOLD=0.80
QUALITY_THRESHOLD=0.70

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Rate Limiting
RATE_LIMIT_STORAGE_URL=memory://
RATE_LIMIT_DEFAULT=100 per hour

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# SSL Configuration (for production)
SSL_CERT_PATH=certificates/cert.pem
SSL_KEY_PATH=certificates/key.pem
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Environment file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False

def download_ai_models():
    """Download AI models for face detection"""
    print("🤖 Setting up AI models...")
    
    models_dir = Path('models')
    models_dir.mkdir(exist_ok=True)
    
    # Create placeholder files for AI models
    # In production, these would be actual model files
    model_files = [
        'tiny_face_detector_model-weights_manifest.json',
        'tiny_face_detector_model-shard1',
        'face_landmark_68_model-weights_manifest.json',
        'face_landmark_68_model-shard1',
        'face_recognition_model-weights_manifest.json',
        'face_recognition_model-shard1',
        'face_expression_model-weights_manifest.json',
        'face_expression_model-shard1'
    ]
    
    for model_file in model_files:
        model_path = models_dir / model_file
        if not model_path.exists():
            # Create placeholder file
            with open(model_path, 'w') as f:
                f.write('# Placeholder for AI model file\n')
    
    print("✅ AI model placeholders created")
    print("ℹ️  Note: Download actual face-api.js models for production use")
    return True

def create_startup_scripts():
    """Create startup scripts"""
    print("🚀 Creating startup scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting Advanced Biometric Authentication System...
echo.

echo Starting Backend Server...
start "Backend" python app_enhanced.py

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend Development Server...
start "Frontend" npm run dev

echo.
echo ✅ System started successfully!
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
pause
"""
    
    # Linux/Mac shell script
    unix_script = """#!/bin/bash
echo "Starting Advanced Biometric Authentication System..."
echo

echo "Starting Backend Server..."
python3 app_enhanced.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting Frontend Development Server..."
npm run dev &
FRONTEND_PID=$!

echo
echo "✅ System started successfully!"
echo
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
"""
    
    try:
        with open('start.bat', 'w') as f:
            f.write(windows_script)
        
        with open('start.sh', 'w') as f:
            f.write(unix_script)
        
        # Make shell script executable on Unix systems
        if os.name != 'nt':
            os.chmod('start.sh', 0o755)
        
        print("✅ Startup scripts created")
        return True
    except Exception as e:
        print(f"❌ Failed to create startup scripts: {e}")
        return False

def create_documentation():
    """Create additional documentation files"""
    print("📚 Creating documentation...")
    
    # API documentation
    api_docs = """# API Documentation

## Authentication Endpoints

### POST /api/register
Register a new user with biometric data.

**Request:**
- `username` (string): Unique username
- `email` (string): User email address
- `phoneNumber` (string, optional): Phone number
- `securityLevel` (string): Security level (LOW, MEDIUM, HIGH, MAXIMUM)
- `face_0` to `face_4` (files): Face images
- `fingerprint` (file): Fingerprint image

**Response:**
```json
{
  "message": "Registration successful",
  "user_id": 123,
  "biometric_quality": {...},
  "security_level": "MEDIUM"
}
```

### POST /api/auth/face
Authenticate using face recognition.

**Request:**
- `username` (string): Username
- `face` (file): Face image for authentication

**Response:**
```json
{
  "success": true,
  "confidence": 87.5,
  "quality": 0.92,
  "response_time": 1.23
}
```

### POST /api/auth/fingerprint
Authenticate using fingerprint.

**Request:**
- `username` (string): Username
- `fingerprint` (file): Fingerprint image

**Response:**
```json
{
  "success": true,
  "score": 0.95,
  "quality": 0.88,
  "session_token": "..."
}
```

## Document Management

### GET /api/user/docs
Get user documents.

### POST /api/user/docs
Upload a document.

### DELETE /api/user/docs
Delete a document.

## Security & Analytics

### GET /api/security/events
Get security events.

### GET /api/analytics/dashboard
Get dashboard analytics.
"""
    
    try:
        with open('API_DOCS.md', 'w') as f:
            f.write(api_docs)
        print("✅ API documentation created")
        return True
    except Exception as e:
        print(f"❌ Failed to create documentation: {e}")
        return False

def run_tests():
    """Run basic system tests"""
    print("🧪 Running system tests...")
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Database connection
    try:
        conn = sqlite3.connect('enhanced_users.db')
        conn.close()
        print("  ✅ Database connection test passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Database connection test failed: {e}")
    
    # Test 2: Upload directory
    if os.path.exists('uploads') and os.path.isdir('uploads'):
        print("  ✅ Upload directory test passed")
        tests_passed += 1
    else:
        print("  ❌ Upload directory test failed")
    
    # Test 3: Configuration file
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                json.load(f)
            print("  ✅ Configuration file test passed")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ Configuration file test failed: {e}")
    else:
        print("  ❌ Configuration file test failed")
    
    # Test 4: Environment file
    if os.path.exists('.env'):
        print("  ✅ Environment file test passed")
        tests_passed += 1
    else:
        print("  ❌ Environment file test failed")
    
    print(f"📊 Tests passed: {tests_passed}/{total_tests}")
    return tests_passed == total_tests

def main():
    """Main setup function"""
    print_banner()
    
    print("🔧 Starting system setup...\n")
    
    # Check prerequisites
    if not check_python_version():
        print("❌ Setup failed: Python version incompatible")
        return False
    
    if not check_node_version():
        print("❌ Setup failed: Node.js not found")
        return False
    
    # Setup steps
    setup_steps = [
        ("Installing Python dependencies", install_python_dependencies),
        ("Installing Node.js dependencies", install_node_dependencies),
        ("Creating directories", create_directories),
        ("Setting up database", setup_database),
        ("Creating configuration", create_config_file),
        ("Creating environment file", create_environment_file),
        ("Setting up AI models", download_ai_models),
        ("Creating startup scripts", create_startup_scripts),
        ("Creating documentation", create_documentation),
        ("Running tests", run_tests),
    ]
    
    failed_steps = []
    
    for step_name, step_function in setup_steps:
        print(f"\n{step_name}...")
        if not step_function():
            failed_steps.append(step_name)
    
    # Summary
    print("\n" + "="*60)
    if not failed_steps:
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("\n✅ All components installed and configured")
        print("\n🚀 To start the system:")
        print("   Windows: double-click start.bat")
        print("   Linux/Mac: ./start.sh")
        print("\n🌐 Access URLs:")
        print("   Frontend: http://localhost:5173")
        print("   Backend:  http://localhost:5000")
        print("\n📚 Documentation:")
        print("   README.md - Complete user guide")
        print("   API_DOCS.md - API documentation")
        print("\n🔒 Security Notes:")
        print("   - Change default secrets in .env file")
        print("   - Download actual AI models for production")
        print("   - Configure SSL certificates for HTTPS")
        print("   - Review security settings in config.json")
    else:
        print("⚠️  SETUP COMPLETED WITH WARNINGS")
        print(f"\n❌ Failed steps: {', '.join(failed_steps)}")
        print("\n🔧 Manual intervention may be required")
    
    print("\n" + "="*60)
    return len(failed_steps) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)