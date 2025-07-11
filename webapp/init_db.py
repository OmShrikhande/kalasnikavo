#!/usr/bin/env python3
"""
Database initialization script for Advanced Biometric Authentication System
"""

import sqlite3
import os

def init_database():
    """Initialize the enhanced database"""
    db_path = 'enhanced_users.db'
    
    print("🗄️ Initializing database...")
    
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
        print(f"📍 Database location: {os.path.abspath(db_path)}")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    init_database()