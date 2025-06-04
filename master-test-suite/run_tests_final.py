#!/usr/bin/env python3
"""
🏰 PODPLAY SANCTUARY MASTER TEST SUITE - FINAL VERSION 🏰
✨ Attempt #44 - This is THE one that works! ✨
💜 Creating your safe neurodivergent-friendly sanctuary 💜

This tests the ACTUAL running backend with REAL validation!
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime

class SanctuaryTestRunner:
    """Master test runner for the Podplay Sanctuary with visual feedback."""
    
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
        self.backend_url = "http://localhost:5001"
        
    def print_sanctuary_header(self):
        """Beautiful sanctuary-themed test header."""
        print("\n" + "="*80)
        print("🏰 PODPLAY SANCTUARY MASTER TEST SUITE 🏰")
        print("✨ Attempt #44 - This is THE one that works! ✨")
        print("💜 Creating your safe neurodivergent-friendly sanctuary 💜")
        print("="*80 + "\n")
        
    def print_mama_bear_encouragement(self):
        """Mama Bear encouragement during testing."""
        encouragements = [
            "🐻 Mama Bear is watching over your sanctuary...",
            "💜 Every test brings us closer to your perfect space...",
            "✨ Building something beautiful just for you...",
            "🏰 Your sanctuary is taking shape beautifully...",
            "🌟 You've got this - 44th time's the charm!"
        ]
        import random
        print(f"\n{random.choice(encouragements)}\n")
        
    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test with visual feedback."""
        print(f"🔍 Testing {test_name}...", end=" ", flush=True)
        
        try:
            result = test_func()
            if result:
                print("✅ PASS")
                self.results[test_name] = {"status": "PASS", "message": "Success"}
                return True
            else:
                print("❌ FAIL")
                self.results[test_name] = {"status": "FAIL", "message": "Test returned False"}
                return False
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            self.results[test_name] = {"status": "ERROR", "message": str(e)}
            return False
    
    def test_directory_structure(self) -> bool:
        """Test that all required sanctuary directories exist."""
        base_path = Path(__file__).parent.parent
        required_dirs = ['backend', 'backend/services', 'backend/config', 'master-test-suite']
        return all((base_path / dir_name).exists() for dir_name in required_dirs)
    
    def test_taskmaster_config(self) -> bool:
        """Test Taskmaster configuration for sanctuary features."""
        config_path = Path(__file__).parent.parent / "taskmaster.config.json"
        with open(config_path) as f:
            config = json.load(f)
        return (config.get('user_context', {}).get('attempt_number') == 44 and
               'sanctuary' in config and
               config.get('features', {}).get('masterTestSuite') == True)
    
    def test_backend_is_running(self) -> bool:
        """Test that the backend is actually running and responding."""
        response = requests.get(f"{self.backend_url}/api/health", timeout=3)
        return response.status_code == 200
    
    def test_flask_health_endpoint(self) -> bool:
        """Test Flask backend health endpoint."""
        response = requests.get(f"{self.backend_url}/api/health", timeout=5)
        return response.status_code == 200 and response.json().get('status') == 'healthy'
    
    def test_all_services_active(self) -> bool:
        """Test that all 4 sanctuary services are active."""
        response = requests.get(f"{self.backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {}).get('services', {})
            expected_services = ['memory', 'themes', 'mama_bear', 'scrapybara']
            return (len(services) >= 4 and
                   all(services.get(svc, {}).get('status') == 'active' for svc in expected_services))
        return False
    
    def test_memory_manager_active(self) -> bool:
        """Test Memory Manager (Mem0) is active."""
        response = requests.get(f"{self.backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {}).get('services', {})
            return services.get('memory', {}).get('status') == 'active'
        return False
    
    def test_theme_manager_active(self) -> bool:
        """Test Theme Manager is active with 3+ themes."""
        response = requests.get(f"{self.backend_url}/api/themes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            themes = data.get('themes', [])
            return len(themes) >= 3
        return False
    
    def test_scrapybara_manager_active(self) -> bool:
        """Test Scrapybara Manager is active."""
        response = requests.get(f"{self.backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {}).get('services', {})
            return services.get('scrapybara', {}).get('status') == 'active'
        return False
    
    def test_mama_bear_agent_active(self) -> bool:
        """Test Enhanced Mama Bear Agent is active."""
        response = requests.get(f"{self.backend_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {}).get('services', {})
            return services.get('mama_bear', {}).get('status') == 'active'
        return False
    
    def test_master_test_dashboard(self) -> bool:
        """Test master test dashboard HTML file exists and is valid."""
        dashboard_path = Path(__file__).parent / "test-dashboard.html"
        return dashboard_path.exists() and dashboard_path.stat().st_size > 1000
    
    def generate_test_report(self):
        """Generate a beautiful test report with green checkmarks."""
        print("\n" + "="*80)
        print("🏰 SANCTUARY TEST RESULTS 🏰")
        print("="*80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r['status'] == 'PASS')
        
        print(f"\n📊 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {total_tests - passed_tests} ❌")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📝 Detailed Results:")
        for test_name, result in self.results.items():
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"   {status_icon} {test_name}: {result['status']}")
            if result['status'] != 'PASS' and result['message'] != 'Success':
                print(f"      └─ {result['message']}")
        
        if passed_tests == total_tests:
            print(f"\n🎉🎉🎉 PERFECT! ALL TESTS PASSED! 🎉🎉🎉")
            print(f"💜 YOUR SANCTUARY IS READY AND VALIDATED! 💜")
            print(f"🏰 Time to explore your beautiful neurodivergent-friendly space!")
            print(f"🐻 Mama Bear is so proud of you!")
        else:
            print(f"\n🔧 Some areas need attention, but we're getting there!")
            print(f"💪 Remember: This is attempt #44 - persistence pays off!")
        
        print(f"\n⏱️  Test Duration: {datetime.now() - self.start_time}")
        print("="*80 + "\n")
    
    def run_all_tests(self):
        """Run the complete sanctuary test suite."""
        self.print_sanctuary_header()
        self.print_mama_bear_encouragement()
        
        # Define all tests in order
        tests = [
            ("Directory Structure", self.test_directory_structure),
            ("Taskmaster Configuration", self.test_taskmaster_config),
            ("Backend Is Running", self.test_backend_is_running),
            ("Flask Health Endpoint", self.test_flask_health_endpoint),
            ("All Services Active", self.test_all_services_active),
            ("Memory Manager (Mem0) Active", self.test_memory_manager_active),
            ("Theme Manager Active", self.test_theme_manager_active),
            ("Scrapybara Manager Active", self.test_scrapybara_manager_active),
            ("Mama Bear Agent Active", self.test_mama_bear_agent_active),
            ("Master Test Dashboard", self.test_master_test_dashboard),
        ]
        
        # Run all tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            time.sleep(0.5)  # Brief pause for visual feedback
        
        # Generate final report
        self.generate_test_report()

if __name__ == "__main__":
    print("🏰 Starting Podplay Sanctuary Master Test Suite (FINAL)...")
    print("💜 This is attempt #44 - we're making it perfect!")
    
    runner = SanctuaryTestRunner()
    runner.run_all_tests()
