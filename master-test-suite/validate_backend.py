#!/usr/bin/env python3
"""
Quick Backend Validation Script
Validates the Flask backend is running and all services are initialized.
"""

import requests
import time
import sys
from pathlib import Path

def test_backend_running():
    """Test if the Flask backend is running on port 5001."""
    try:
        print("🔍 Checking if Flask backend is running...", end=" ", flush=True)
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def start_backend_if_needed():
    """Start the Flask backend if it's not running."""
    if not test_backend_running():
        print("\n🚀 Starting Flask backend...")
        backend_path = Path(__file__).parent.parent / "backend"
        
        import subprocess
        import os
        
        # Change to backend directory and start the app
        os.chdir(backend_path)
        
        try:
            # Start the Flask app in the background
            process = subprocess.Popen([
                sys.executable, "app.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("⏳ Waiting for backend to start...")
            time.sleep(3)
            
            # Test if it's now running
            if test_backend_running():
                print("✅ Backend started successfully!")
                return True
            else:
                print("❌ Backend failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    else:
        return True

if __name__ == "__main__":
    print("🏰 Podplay Sanctuary Backend Validator")
    print("=" * 50)
    
    if start_backend_if_needed():
        print("\n🎉 Backend is ready for testing!")
        print("💜 Run the master test suite with: python run_tests.py")
    else:
        print("\n⚠️  Backend startup failed")
        print("💡 Try running manually: cd backend && python app.py")
