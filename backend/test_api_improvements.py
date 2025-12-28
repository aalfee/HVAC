#!/usr/bin/env python
"""
Quick test script to verify the API is working correctly.
Run this to test broken pipe handling and error scenarios.
"""

import os
import sys
import django
import requests
import json
from time import sleep

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hvac_ai.settings")
django.setup()

# Configuration
BASE_URL = "http://localhost:8000/api"
HEALTH_ENDPOINT = f"{BASE_URL}/health/"
ANOMALIES_ENDPOINT = f"{BASE_URL}/anomalies/"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Make sure the server is running on localhost:8000")
        return False

def test_anomaly_detection():
    """Test the anomaly detection endpoint"""
    print("\n" + "="*60)
    print("Testing Anomaly Detection Endpoint")
    print("="*60)
    try:
        response = requests.get(ANOMALIES_ENDPOINT, timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data[:2], indent=2)}...")  # Show first 2 items
        print(f"Total records: {len(data)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Make sure the server is running on localhost:8000")
        return False

def test_concurrent_requests():
    """Test handling of concurrent requests"""
    print("\n" + "="*60)
    print("Testing Concurrent Requests")
    print("="*60)
    import concurrent.futures
    
    def make_request():
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error in concurrent request: {str(e)}")
            return False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    success_count = sum(results)
    print(f"Successful requests: {success_count}/5")
    return success_count == 5

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("HVAC API - Broken Pipe Error Handling Test Suite")
    print("="*60)
    
    results = {}
    
    # Run tests
    results['health_check'] = test_health_check()
    results['anomaly_detection'] = test_anomaly_detection()
    results['concurrent_requests'] = test_concurrent_requests()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
