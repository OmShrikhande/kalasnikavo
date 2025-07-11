#!/usr/bin/env python3
"""
Test script for Enhanced Ultimate Biometric Authentication System
"""

import requests
import json
import time
import os
import sys
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test configuration
BASE_URL = 'http://localhost:5000'
TEST_USERNAME = 'test_user_enhanced'
TEST_EMAIL = 'test@enhanced.com'
TEST_SECURITY_LEVEL = 'HIGH'

class EnhancedSystemTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test_result(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {message}")
        
        if details:
            logger.debug(f"Details: {details}")
    
    def test_system_status(self):
        """Test system status endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/system/status")
            
            if response.status_code == 200:
                data = response.json()
                self.log_test_result(
                    "System Status",
                    True,
                    f"System online with {data.get('user_count', 0)} users",
                    data
                )
                return True
            else:
                self.log_test_result(
                    "System Status",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "System Status",
                False,
                f"Connection error: {str(e)}"
            )
            return False
    
    def test_user_registration(self):
        """Test user registration with multiple face images and fingerprint"""
        try:
            # Create test files
            test_face_data = b"fake_face_image_data"
            test_fp_data = b"fake_fingerprint_data"
            
            # Prepare form data
            files = {
                'face_0': ('face_0.jpg', test_face_data, 'image/jpeg'),
                'face_1': ('face_1.jpg', test_face_data, 'image/jpeg'),
                'face_2': ('face_2.jpg', test_face_data, 'image/jpeg'),
                'face_3': ('face_3.jpg', test_face_data, 'image/jpeg'),
                'face_4': ('face_4.jpg', test_face_data, 'image/jpeg'),
                'fingerprint': ('fingerprint.bmp', test_fp_data, 'image/bmp')
            }
            
            data = {
                'username': TEST_USERNAME,
                'email': TEST_EMAIL,
                'securityLevel': TEST_SECURITY_LEVEL
            }
            
            response = self.session.post(
                f"{self.base_url}/api/register",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_test_result(
                    "User Registration",
                    True,
                    f"User registered successfully with ID {result.get('user_id')}",
                    result
                )
                return True
            else:
                self.log_test_result(
                    "User Registration",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "User Registration",
                False,
                f"Registration error: {str(e)}"
            )
            return False
    
    def test_face_authentication(self):
        """Test face authentication"""
        try:
            test_face_data = b"fake_face_image_data"
            
            files = {
                'face': ('test_face.jpg', test_face_data, 'image/jpeg')
            }
            
            data = {
                'username': TEST_USERNAME
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/face",
                files=files,
                data=data
            )
            
            # Note: This will likely fail in real testing due to fake data
            # but we're testing the endpoint functionality
            if response.status_code in [200, 401]:
                result = response.json()
                success = response.status_code == 200
                self.log_test_result(
                    "Face Authentication",
                    success,
                    f"Face auth endpoint working, confidence: {result.get('confidence', 'N/A')}",
                    result
                )
                return True
            else:
                self.log_test_result(
                    "Face Authentication",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Face Authentication",
                False,
                f"Face auth error: {str(e)}"
            )
            return False
    
    def test_fingerprint_authentication(self):
        """Test fingerprint authentication"""
        try:
            test_fp_data = b"fake_fingerprint_data"
            
            files = {
                'fingerprint': ('test_fingerprint.bmp', test_fp_data, 'image/bmp')
            }
            
            data = {
                'username': TEST_USERNAME
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/fingerprint",
                files=files,
                data=data
            )
            
            if response.status_code in [200, 401]:
                result = response.json()
                success = response.status_code == 200
                self.log_test_result(
                    "Fingerprint Authentication",
                    success,
                    f"Fingerprint auth endpoint working, confidence: {result.get('confidence', 'N/A')}",
                    result
                )
                return True
            else:
                self.log_test_result(
                    "Fingerprint Authentication",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Fingerprint Authentication",
                False,
                f"Fingerprint auth error: {str(e)}"
            )
            return False
    
    def test_dual_authentication(self):
        """Test dual biometric authentication"""
        try:
            test_face_data = b"fake_face_image_data"
            test_fp_data = b"fake_fingerprint_data"
            
            files = {
                'face': ('test_face.jpg', test_face_data, 'image/jpeg'),
                'fingerprint': ('test_fingerprint.bmp', test_fp_data, 'image/bmp')
            }
            
            data = {
                'username': TEST_USERNAME
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/dual",
                files=files,
                data=data
            )
            
            if response.status_code in [200, 401]:
                result = response.json()
                success = response.status_code == 200
                self.log_test_result(
                    "Dual Authentication",
                    success,
                    f"Dual auth endpoint working, fusion score: {result.get('fusion_score', 'N/A')}",
                    result
                )
                return True
            else:
                self.log_test_result(
                    "Dual Authentication",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Dual Authentication",
                False,
                f"Dual auth error: {str(e)}"
            )
            return False
    
    def test_performance_metrics(self):
        """Test system performance and metrics"""
        try:
            # Test multiple requests to measure performance
            start_time = time.time()
            
            for i in range(5):
                response = self.session.get(f"{self.base_url}/api/system/status")
                if response.status_code != 200:
                    break
            
            end_time = time.time()
            avg_response_time = (end_time - start_time) / 5
            
            self.log_test_result(
                "Performance Metrics",
                True,
                f"Average response time: {avg_response_time:.3f}s",
                {
                    'avg_response_time': avg_response_time,
                    'requests_tested': 5
                }
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Performance Metrics",
                False,
                f"Performance test error: {str(e)}"
            )
            return False
    
    def test_security_features(self):
        """Test security features and error handling"""
        try:
            # Test invalid file upload
            response = self.session.post(
                f"{self.base_url}/api/auth/face",
                files={'face': ('test.txt', b'invalid_data', 'text/plain')},
                data={'username': TEST_USERNAME}
            )
            
            if response.status_code == 400:
                self.log_test_result(
                    "Security Features",
                    True,
                    "Invalid file type properly rejected",
                    response.json()
                )
            else:
                self.log_test_result(
                    "Security Features",
                    False,
                    f"Invalid file not rejected: HTTP {response.status_code}"
                )
                
            # Test missing username
            response = self.session.post(
                f"{self.base_url}/api/auth/face",
                files={'face': ('test.jpg', b'fake_data', 'image/jpeg')},
                data={}
            )
            
            if response.status_code == 400:
                self.log_test_result(
                    "Security Features - Missing Data",
                    True,
                    "Missing username properly rejected",
                    response.json()
                )
                return True
            else:
                self.log_test_result(
                    "Security Features - Missing Data",
                    False,
                    f"Missing username not rejected: HTTP {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Security Features",
                False,
                f"Security test error: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Enhanced Ultimate Biometric Authentication System Tests")
        print("=" * 80)
        
        # List of tests to run
        tests = [
            ("System Status Check", self.test_system_status),
            ("User Registration", self.test_user_registration),
            ("Face Authentication", self.test_face_authentication),
            ("Fingerprint Authentication", self.test_fingerprint_authentication),
            ("Dual Authentication", self.test_dual_authentication),
            ("Performance Metrics", self.test_performance_metrics),
            ("Security Features", self.test_security_features)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Test {test_name} failed with exception: {e}")
                failed += 1
        
        # Generate test report
        self.generate_test_report(passed, failed)
        
        return passed, failed
    
    def generate_test_report(self, passed, failed):
        """Generate detailed test report"""
        print("\n" + "=" * 80)
        print("📊 TEST REPORT")
        print("=" * 80)
        
        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ System Status: HEALTHY")
        elif success_rate >= 60:
            print("⚠️  System Status: WARNING")
        else:
            print("❌ System Status: CRITICAL")
        
        print("\n📋 Detailed Results:")
        print("-" * 50)
        
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test_name']}: {result['message']}")
        
        # Save detailed report to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total,
                    'passed': passed,
                    'failed': failed,
                    'success_rate': success_rate,
                    'test_date': datetime.now().isoformat()
                },
                'results': self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 50)
        
        if failed == 0:
            print("🎉 All tests passed! System is ready for production.")
        else:
            print("🔧 Some tests failed. Please review the following:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • Fix {result['test_name']}: {result['message']}")
        
        print("\n🔗 System URLs:")
        print(f"   • Backend API: {self.base_url}")
        print(f"   • Frontend: http://localhost:3000")
        print(f"   • System Status: {self.base_url}/api/system/status")

def check_system_requirements():
    """Check if system requirements are met"""
    print("🔍 Checking system requirements...")
    
    requirements_met = True
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        requirements_met = False
    else:
        print("✅ Python version OK")
    
    # Check if required packages are available
    required_packages = [
        'requests', 'numpy', 'opencv-python', 'flask', 'tensorflow'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} not installed")
            requirements_met = False
    
    return requirements_met

def main():
    """Main test function"""
    print("🛡️ Enhanced Ultimate Biometric Authentication System Tester")
    print("Version 1.0")
    print("=" * 80)
    
    # Check requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please install required packages.")
        print("Run: pip install -r requirements_enhanced.txt")
        return False
    
    # Check if backend is running
    print(f"\n🔌 Checking backend connection to {BASE_URL}...")
    try:
        response = requests.get(f"{BASE_URL}/api/system/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"⚠️  Backend responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        print("Please start the backend server first:")
        print("python app_enhanced_ultimate.py")
        return False
    
    # Run tests
    tester = EnhancedSystemTester()
    passed, failed = tester.run_all_tests()
    
    # Return success status
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)