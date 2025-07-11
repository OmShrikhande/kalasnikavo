#!/usr/bin/env python3
"""
Simple test script to verify the system is working
"""
import requests
import json
import time
import os

BASE_URL = 'http://localhost:5000'

def test_health():
    """Test if the server is running"""
    try:
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not reachable: {e}")
        return False

def test_registration():
    """Test registration endpoint"""
    try:
        # Create dummy files for testing
        test_data = {
            'username': f'test_user_{int(time.time())}',
            'email': 'test@example.com',
            'securityLevel': 'MEDIUM'
        }
        
        files = {
            'face_0': ('test_face.jpg', b'dummy_face_data', 'image/jpeg'),
            'fingerprint': ('test_fp.bmp', b'dummy_fp_data', 'image/bmp')
        }
        
        response = requests.post(f'{BASE_URL}/api/register', data=test_data, files=files, timeout=10)
        
        if response.status_code == 200:
            print("✅ Registration endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration test failed: {e}")
        return False

def main():
    print("🧪 Testing Biometric Authentication System")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing server health...")
    if not test_health():
        print("\n❌ Server health check failed. Make sure to start the server first.")
        print("   Run: python app_simple.py")
        return
    
    # Test 2: Registration
    print("\n2. Testing registration...")
    if test_registration():
        print("\n✅ All tests passed! The system is working correctly.")
    else:
        print("\n❌ Registration test failed. Check the server logs for details.")

if __name__ == "__main__":
    main()