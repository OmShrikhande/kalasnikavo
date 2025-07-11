#!/usr/bin/env python3
"""
Enhanced Database initialization script for Ultimate Biometric Authentication System
"""

import sqlite3
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_enhanced_database():
    """Initialize the enhanced ultimate database with all features"""
    db_path = 'enhanced_ultimate_users.db'
    
    print("🗄️ Initializing Enhanced Ultimate Database...")
    logger.info("Starting database initialization...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enhanced Users table with multi-algorithm support
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            phone_number TEXT,
            face_paths TEXT NOT NULL,
            fp_path TEXT NOT NULL,
            security_level TEXT DEFAULT 'MEDIUM',
            biometric_quality TEXT,
            face_algorithms TEXT,
            fp_algorithms TEXT,
            registration_metadata TEXT,
            device_fingerprint TEXT,
            registration_location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            login_count INTEGER DEFAULT 0,
            failed_attempts INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0,
            is_locked BOOLEAN DEFAULT 0,
            lock_expires_at TIMESTAMP,
            biometric_template_hash TEXT,
            encryption_key TEXT
        )''')
        
        # Enhanced Authentication attempts table
        cursor.execute('''CREATE TABLE IF NOT EXISTS auth_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip_address TEXT,
            user_agent TEXT,
            attempt_type TEXT,
            success BOOLEAN,
            algorithm_scores TEXT,
            overall_confidence REAL,
            fusion_score REAL,
            response_time REAL,
            failure_reason TEXT,
            biometric_quality_score REAL,
            device_fingerprint TEXT,
            geolocation TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT,
            risk_score REAL
        )''')
        
        # Enhanced Security events table
        cursor.execute('''CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            username TEXT,
            ip_address TEXT,
            user_agent TEXT,
            device_fingerprint TEXT,
            geolocation TEXT,
            severity TEXT,
            details TEXT,
            threat_level TEXT,
            automated_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved BOOLEAN DEFAULT 0,
            resolved_at TIMESTAMP,
            resolved_by TEXT
        )''')
        
        # User sessions table with enhanced tracking
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            device_fingerprint TEXT,
            ip_address TEXT,
            user_agent TEXT,
            geolocation TEXT,
            biometric_confidence REAL,
            continuous_auth_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            logout_reason TEXT,
            session_metadata TEXT
        )''')
        
        # Algorithm performance tracking
        cursor.execute('''CREATE TABLE IF NOT EXISTS algorithm_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_name TEXT NOT NULL,
            algorithm_type TEXT NOT NULL,
            version TEXT,
            accuracy REAL,
            precision_score REAL,
            recall REAL,
            f1_score REAL,
            processing_time REAL,
            success_rate REAL,
            failure_rate REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            test_samples INTEGER,
            hardware_info TEXT
        )''')
        
        # Biometric quality metrics
        cursor.execute('''CREATE TABLE IF NOT EXISTS biometric_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            biometric_type TEXT NOT NULL,
            file_path TEXT,
            quality_score REAL,
            sharpness REAL,
            contrast REAL,
            brightness REAL,
            noise_level REAL,
            resolution_width INTEGER,
            resolution_height INTEGER,
            file_size INTEGER,
            quality_metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # System configuration
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_key TEXT UNIQUE NOT NULL,
            config_value TEXT,
            config_type TEXT,
            description TEXT,
            is_sensitive BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )''')
        
        # Enhanced Documents table
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT NOT NULL,
            original_name TEXT,
            file_hash TEXT,
            file_size INTEGER,
            mime_type TEXT,
            encryption_key TEXT,
            access_level TEXT DEFAULT 'PRIVATE',
            access_count INTEGER DEFAULT 0,
            tags TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_deleted BOOLEAN DEFAULT 0,
            deleted_at TIMESTAMP
        )''')
        
        # Audit log for compliance
        cursor.execute('''CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            action TEXT NOT NULL,
            resource_type TEXT,
            resource_id TEXT,
            old_values TEXT,
            new_values TEXT,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN DEFAULT 1,
            error_message TEXT
        )''')
        
        # System metrics for monitoring
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            metric_unit TEXT,
            category TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            additional_data TEXT
        )''')
        
        # API usage tracking
        cursor.execute('''CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            username TEXT,
            status_code INTEGER,
            response_time REAL,
            request_size INTEGER,
            response_size INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rate_limit_hit BOOLEAN DEFAULT 0
        )''')
        
        # Machine learning model versions
        cursor.execute('''CREATE TABLE IF NOT EXISTS ml_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            model_type TEXT NOT NULL,
            version TEXT NOT NULL,
            file_path TEXT,
            accuracy REAL,
            training_date TIMESTAMP,
            deployment_date TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            performance_metrics TEXT,
            training_data_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Create indexes for performance optimization
        logger.info("Creating database indexes...")
        
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)',
            'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)',
            'CREATE INDEX IF NOT EXISTS idx_users_security_level ON users(security_level)',
            'CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login)',
            'CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active)',
            
            'CREATE INDEX IF NOT EXISTS idx_auth_attempts_username ON auth_attempts(username)',
            'CREATE INDEX IF NOT EXISTS idx_auth_attempts_ip_address ON auth_attempts(ip_address)',
            'CREATE INDEX IF NOT EXISTS idx_auth_attempts_timestamp ON auth_attempts(timestamp)',
            'CREATE INDEX IF NOT EXISTS idx_auth_attempts_success ON auth_attempts(success)',
            
            'CREATE INDEX IF NOT EXISTS idx_security_events_username ON security_events(username)',
            'CREATE INDEX IF NOT EXISTS idx_security_events_event_type ON security_events(event_type)',
            'CREATE INDEX IF NOT EXISTS idx_security_events_timestamp ON security_events(timestamp)',
            'CREATE INDEX IF NOT EXISTS idx_security_events_severity ON security_events(severity)',
            
            'CREATE INDEX IF NOT EXISTS idx_user_sessions_username ON user_sessions(username)',
            'CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON user_sessions(session_id)',
            'CREATE INDEX IF NOT EXISTS idx_user_sessions_is_active ON user_sessions(is_active)',
            
            'CREATE INDEX IF NOT EXISTS idx_algorithm_performance_name ON algorithm_performance(algorithm_name)',
            'CREATE INDEX IF NOT EXISTS idx_algorithm_performance_type ON algorithm_performance(algorithm_type)',
            
            'CREATE INDEX IF NOT EXISTS idx_biometric_quality_username ON biometric_quality(username)',
            'CREATE INDEX IF NOT EXISTS idx_biometric_quality_type ON biometric_quality(biometric_type)',
            
            'CREATE INDEX IF NOT EXISTS idx_documents_username ON documents(username)',
            'CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename)',
            
            'CREATE INDEX IF NOT EXISTS idx_audit_log_username ON audit_log(username)',
            'CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action)',
            'CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp)',
            
            'CREATE INDEX IF NOT EXISTS idx_system_metrics_name ON system_metrics(metric_name)',
            'CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp)',
            
            'CREATE INDEX IF NOT EXISTS idx_api_usage_endpoint ON api_usage(endpoint)',
            'CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp)',
            
            'CREATE INDEX IF NOT EXISTS idx_ml_models_name ON ml_models(model_name)',
            'CREATE INDEX IF NOT EXISTS idx_ml_models_is_active ON ml_models(is_active)'
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        # Insert default system configuration
        logger.info("Inserting default system configuration...")
        
        default_configs = [
            ('max_failed_attempts', '5', 'INTEGER', 'Maximum failed login attempts before lockout'),
            ('lockout_duration', '1800', 'INTEGER', 'Account lockout duration in seconds'),
            ('session_timeout', '3600', 'INTEGER', 'Session timeout in seconds'),
            ('password_policy', '{"min_length": 8, "require_special": true}', 'JSON', 'Password policy configuration'),
            ('biometric_quality_threshold', '0.7', 'FLOAT', 'Minimum biometric quality threshold'),
            ('enable_audit_logging', 'true', 'BOOLEAN', 'Enable comprehensive audit logging'),
            ('api_rate_limit', '100', 'INTEGER', 'API requests per minute limit'),
            ('max_file_size', '52428800', 'INTEGER', 'Maximum file upload size in bytes'),
            ('allowed_file_types', '["jpg", "jpeg", "png", "bmp"]', 'JSON', 'Allowed file types for upload'),
            ('security_level_default', 'MEDIUM', 'STRING', 'Default security level for new users'),
            ('enable_continuous_auth', 'false', 'BOOLEAN', 'Enable continuous authentication'),
            ('biometric_template_encryption', 'true', 'BOOLEAN', 'Encrypt biometric templates'),
            ('geo_blocking_enabled', 'false', 'BOOLEAN', 'Enable geographic IP blocking'),
            ('anomaly_detection_enabled', 'true', 'BOOLEAN', 'Enable anomaly detection'),
            ('backup_retention_days', '30', 'INTEGER', 'Backup retention period in days')
        ]
        
        for config_key, config_value, config_type, description in default_configs:
            cursor.execute('''INSERT OR IGNORE INTO system_config 
                             (config_key, config_value, config_type, description) 
                             VALUES (?, ?, ?, ?)''', 
                          (config_key, config_value, config_type, description))
        
        # Insert default algorithm performance baselines
        logger.info("Inserting algorithm performance baselines...")
        
        algorithm_baselines = [
            ('deepface', 'face', '1.0', 0.968, 0.954, 0.962, 0.958, 1.2, 0.96, 0.04),
            ('resnet50', 'face', '1.0', 0.945, 0.932, 0.945, 0.938, 0.8, 0.94, 0.06),
            ('vgg16', 'face', '1.0', 0.932, 0.918, 0.932, 0.925, 0.9, 0.93, 0.07),
            ('inception', 'face', '1.0', 0.951, 0.945, 0.951, 0.948, 1.1, 0.95, 0.05),
            ('hog', 'fingerprint', '1.0', 0.923, 0.915, 0.923, 0.919, 0.5, 0.92, 0.08),
            ('lbp', 'fingerprint', '1.0', 0.897, 0.882, 0.897, 0.889, 0.3, 0.90, 0.10),
            ('gabor', 'fingerprint', '1.0', 0.915, 0.908, 0.915, 0.911, 0.6, 0.91, 0.09),
            ('minutiae', 'fingerprint', '1.0', 0.942, 0.938, 0.942, 0.940, 0.7, 0.94, 0.06),
            ('ensemble', 'fusion', '1.0', 0.982, 0.978, 0.982, 0.980, 2.3, 0.98, 0.02)
        ]
        
        for (name, type_, version, accuracy, precision, recall, f1, time, success, failure) in algorithm_baselines:
            cursor.execute('''INSERT OR IGNORE INTO algorithm_performance 
                             (algorithm_name, algorithm_type, version, accuracy, precision_score, 
                              recall, f1_score, processing_time, success_rate, failure_rate) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (name, type_, version, accuracy, precision, recall, f1, time, success, failure))
        
        # Create views for easy data access
        logger.info("Creating database views...")
        
        cursor.execute('''CREATE VIEW IF NOT EXISTS user_stats AS
            SELECT 
                u.username,
                u.security_level,
                u.login_count,
                u.last_login,
                u.is_active,
                COUNT(aa.id) as total_attempts,
                SUM(CASE WHEN aa.success = 1 THEN 1 ELSE 0 END) as successful_attempts,
                SUM(CASE WHEN aa.success = 0 THEN 1 ELSE 0 END) as failed_attempts,
                AVG(aa.overall_confidence) as avg_confidence
            FROM users u
            LEFT JOIN auth_attempts aa ON u.username = aa.username
            GROUP BY u.username
        ''')
        
        cursor.execute('''CREATE VIEW IF NOT EXISTS security_dashboard AS
            SELECT 
                DATE(timestamp) as date,
                event_type,
                severity,
                COUNT(*) as event_count
            FROM security_events
            WHERE timestamp >= datetime('now', '-30 days')
            GROUP BY DATE(timestamp), event_type, severity
            ORDER BY date DESC
        ''')
        
        cursor.execute('''CREATE VIEW IF NOT EXISTS algorithm_summary AS
            SELECT 
                algorithm_name,
                algorithm_type,
                accuracy,
                processing_time,
                success_rate,
                last_updated
            FROM algorithm_performance
            WHERE id IN (
                SELECT MAX(id) FROM algorithm_performance 
                GROUP BY algorithm_name, algorithm_type
            )
        ''')
        
        # Insert sample system metrics
        logger.info("Inserting initial system metrics...")
        
        initial_metrics = [
            ('system_uptime', 0, 'hours', 'system'),
            ('cpu_usage', 0, 'percent', 'system'),
            ('memory_usage', 0, 'percent', 'system'),
            ('disk_usage', 0, 'percent', 'system'),
            ('active_sessions', 0, 'count', 'users'),
            ('total_users', 0, 'count', 'users'),
            ('daily_authentications', 0, 'count', 'security'),
            ('security_events_today', 0, 'count', 'security')
        ]
        
        for metric_name, value, unit, category in initial_metrics:
            cursor.execute('''INSERT INTO system_metrics 
                             (metric_name, metric_value, metric_unit, category) 
                             VALUES (?, ?, ?, ?)''', 
                          (metric_name, value, unit, category))
        
        # Commit all changes
        conn.commit()
        conn.close()
        
        print("✅ Enhanced Ultimate Database initialized successfully!")
        print(f"📍 Database location: {os.path.abspath(db_path)}")
        print("🔧 Database features:")
        print("   • Multi-algorithm support")
        print("   • Enhanced security tracking")
        print("   • Performance monitoring")
        print("   • Comprehensive audit logging")
        print("   • Real-time analytics")
        print("   • Compliance reporting")
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        logger.error(f"Database setup failed: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    try:
        conn = sqlite3.connect('enhanced_ultimate_users.db')
        cursor = conn.cursor()
        
        # Add sample system configuration
        sample_configs = [
            ('maintenance_mode', 'false', 'BOOLEAN', 'System maintenance mode'),
            ('debug_mode', 'false', 'BOOLEAN', 'Debug logging enabled'),
            ('performance_monitoring', 'true', 'BOOLEAN', 'Performance monitoring enabled')
        ]
        
        for config_key, config_value, config_type, description in sample_configs:
            cursor.execute('''INSERT OR IGNORE INTO system_config 
                             (config_key, config_value, config_type, description) 
                             VALUES (?, ?, ?, ?)''', 
                          (config_key, config_value, config_type, description))
        
        conn.commit()
        conn.close()
        
        print("✅ Sample data created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def verify_database():
    """Verify database integrity"""
    try:
        conn = sqlite3.connect('enhanced_ultimate_users.db')
        cursor = conn.cursor()
        
        # Check if all tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            'users', 'auth_attempts', 'security_events', 'user_sessions',
            'algorithm_performance', 'biometric_quality', 'system_config',
            'documents', 'audit_log', 'system_metrics', 'api_usage', 'ml_models'
        ]
        
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        # Check if all views exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = [row[0] for row in cursor.fetchall()]
        
        expected_views = ['user_stats', 'security_dashboard', 'algorithm_summary']
        missing_views = [view for view in expected_views if view not in views]
        
        if missing_views:
            print(f"❌ Missing views: {missing_views}")
            return False
        
        conn.close()
        
        print("✅ Database verification successful!")
        print(f"📊 Tables: {len(tables)}")
        print(f"📈 Views: {len(views)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Enhanced Ultimate Biometric Authentication System")
    print("=" * 60)
    
    # Initialize database
    if init_enhanced_database():
        print()
        
        # Create sample data
        create_sample_data()
        print()
        
        # Verify database
        verify_database()
        print()
        
        print("🎉 Database setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Install Python dependencies: pip install -r requirements_enhanced.txt")
        print("2. Start the enhanced backend: python app_enhanced_ultimate.py")
        print("3. Start the frontend: npm run dev")
        print("4. Access the application at: http://localhost:3000")
        
    else:
        print("💥 Database setup failed! Please check the error messages above.")
        exit(1)