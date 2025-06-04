#!/usr/bin/env python3
"""
Podplay Sanctuary Master Test Suite
Comprehensive validation with visual green checkmarks for a neurodivergent-friendly sanctuary experience.
This is attempt #44 - we're making this one work perfectly! 💜

Tests validate all systems before UI interaction, providing the security and confidence needed.
"""

import sys
import os
import json
import time
import asyncio
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from config.settings import Config
    from services.memory_manager import MemoryManager
    from services.theme_manager import ThemeManager
    from services.scrapybara_manager import ScrapybaraManager
    from services.mama_bear_agent import EnhancedMamaBearAgent
except ImportError as e:
    print(f"⚠️  Import error (expected if backend not initialized): {e}")

class SanctuaryTestRunner:
    """Master test runner for the Podplay Sanctuary with visual feedback."""
    
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
        self.backend_url = "http://localhost:5001"
        self.config = None
        
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
    
    def test_config_loading(self) -> bool:
        """Test configuration loading and validation."""
        try:
            self.config = Config()
            # Test basic config access
            hasattr(self.config, 'anthropic_api_key')
            hasattr(self.config, 'mem0_api_key')
            return True
        except Exception:
            return False
    
    def test_memory_manager_init(self) -> bool:
        """Test Memory Manager (Mem0) initialization."""
        try:
            if not self.config:
                return False
            memory_manager = MemoryManager(self.config)
            return hasattr(memory_manager, 'client')
        except Exception:
            return False
    
    def test_theme_manager_init(self) -> bool:
        """Test Theme Manager initialization with 3 themes."""
        try:
            theme_manager = ThemeManager()
            themes = theme_manager.get_available_themes()
            return len(themes) >= 3 and 'sky' in themes
        except Exception:
            return False
    
    def test_scrapybara_manager_init(self) -> bool:
        """Test Scrapybara Manager initialization."""
        try:
            if not self.config:
                return False
            scrapybara_manager = ScrapybaraManager(self.config)
            return hasattr(scrapybara_manager, 'api_key')
        except Exception:
            return False
    
    def test_mama_bear_agent_init(self) -> bool:
        """Test Enhanced Mama Bear Agent with 7 variants."""
        try:
            if not self.config:
                return False
            mama_bear = EnhancedMamaBearAgent(self.config)
            variants = mama_bear.get_available_variants()
            return len(variants) >= 7
        except Exception:
            return False
    
    def test_flask_health_endpoint(self) -> bool:
        """Test Flask backend health endpoint."""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            return response.status_code == 200 and response.json().get('status') == 'healthy'
        except Exception:
            return False
    
    def test_flask_services_endpoint(self) -> bool:
        """Test Flask services status endpoint."""
        try:
            response = requests.get(f"{self.backend_url}/api/services/status", timeout=5)
            data = response.json()
            return (response.status_code == 200 and 
                   data.get('memory_manager') == 'initialized' and
                   data.get('theme_manager') == 'initialized')
        except Exception:
            return False
    
    def test_taskmaster_config(self) -> bool:
        """Test Taskmaster configuration for sanctuary features."""
        try:
            config_path = Path(__file__).parent.parent / "taskmaster.config.json"
            with open(config_path) as f:
                config = json.load(f)
            
            return (config.get('user_context', {}).get('attempt_number') == 44 and
                   'sanctuary' in config and
                   config.get('features', {}).get('masterTestSuite') == True)
        except Exception:
            return False
    
    def test_master_test_dashboard(self) -> bool:
        """Test master test dashboard HTML file exists and is valid."""
        try:
            dashboard_path = Path(__file__).parent / "test-dashboard.html"
            return dashboard_path.exists() and dashboard_path.stat().st_size > 1000
        except Exception:
            return False
    
    def test_directory_structure(self) -> bool:
        """Test that all required sanctuary directories exist."""
        try:
            base_path = Path(__file__).parent.parent
            required_dirs = ['backend', 'backend/services', 'backend/config', 'master-test-suite']
            
            for dir_name in required_dirs:
                if not (base_path / dir_name).exists():
                    return False
            return True
        except Exception:
            return False
    
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
            print(f"\n🎉 PERFECT! ALL TESTS PASSED! 🎉")
            print(f"💜 Your sanctuary is ready and validated!")
            print(f"🏰 Time to explore your beautiful neurodivergent-friendly space!")
        else:
            print(f"\n🔧 Some areas need attention, but we're getting there!")
            print(f"💪 Remember: This is attempt #44 - persistence pays off!")
        
        # Update the test dashboard with real results
        self.update_test_dashboard()
        
        print(f"\n⏱️  Test Duration: {datetime.now() - self.start_time}")
        print("="*80 + "\n")
    
    def update_test_dashboard(self):
        """Update the HTML test dashboard with real results."""
        try:
            dashboard_path = Path(__file__).parent / "test-dashboard.html"
            
            # Create JavaScript object with test results
            js_results = json.dumps(self.results, indent=2)
            
            # Read current dashboard
            with open(dashboard_path, 'r') as f:
                html_content = f.read()
            
            # Update results section
            results_script = f"""
            <script>
            // Real test results from Python test runner
            const testResults = {js_results};
            const lastRun = '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}';
            
            // Update dashboard with real results
            document.addEventListener('DOMContentLoaded', function() {{
                updateDashboardWithResults(testResults, lastRun);
            }});
            
            function updateDashboardWithResults(results, timestamp) {{
                // Update timestamp
                const timestampEl = document.getElementById('last-run-timestamp');
                if (timestampEl) timestampEl.textContent = timestamp;
                
                // Update individual test results
                Object.entries(results).forEach(([testName, result]) => {{
                    const testEl = document.getElementById(testName.replace(/\\s+/g, '-').toLowerCase());
                    if (testEl) {{
                        const statusEl = testEl.querySelector('.status');
                        if (statusEl) {{
                            statusEl.textContent = result.status === 'PASS' ? '✅' : '❌';
                            testEl.className = 'test-item ' + (result.status === 'PASS' ? 'passed' : 'failed');
                        }}
                    }}
                }});
                
                // Calculate and update summary
                const totalTests = Object.keys(results).length;
                const passedTests = Object.values(results).filter(r => r.status === 'PASS').length;
                const successRate = ((passedTests / totalTests) * 100).toFixed(1);
                
                // Update summary cards
                const summaryEl = document.getElementById('test-summary');
                if (summaryEl) {{
                    summaryEl.innerHTML = `
                        <div class="summary-card">
                            <h3>Total Tests</h3>
                            <div class="metric">${{totalTests}}</div>
                        </div>
                        <div class="summary-card passed">
                            <h3>Passed</h3>
                            <div class="metric">${{passedTests}} ✅</div>
                        </div>
                        <div class="summary-card">
                            <h3>Success Rate</h3>
                            <div class="metric">${{successRate}}%</div>
                        </div>
                    `;
                }}
            }}
            </script>
            """
            
            # Insert or replace the results script
            if '<script>' in html_content and 'testResults' in html_content:
                # Replace existing script
                start = html_content.find('<script>')
                end = html_content.find('</script>') + 9
                html_content = html_content[:start] + results_script + html_content[end:]
            else:
                # Add script before closing body
                html_content = html_content.replace('</body>', results_script + '\n</body>')
            
            # Write updated dashboard
            with open(dashboard_path, 'w') as f:
                f.write(html_content)
                
            print(f"📊 Test dashboard updated with real results!")
            
        except Exception as e:
            print(f"⚠️  Could not update dashboard: {e}")
    
    def run_all_tests(self):
        """Run the complete sanctuary test suite."""
        self.print_sanctuary_header()
        self.print_mama_bear_encouragement()
        
        # Define all tests in order
        tests = [
            ("Directory Structure", self.test_directory_structure),
            ("Taskmaster Configuration", self.test_taskmaster_config),
            ("Config Loading", self.test_config_loading),
            ("Memory Manager Init", self.test_memory_manager_init),
            ("Theme Manager Init", self.test_theme_manager_init),
            ("Scrapybara Manager Init", self.test_scrapybara_manager_init),
            ("Mama Bear Agent Init", self.test_mama_bear_agent_init),
            ("Master Test Dashboard", self.test_master_test_dashboard),
            ("Flask Health Endpoint", self.test_flask_health_endpoint),
            ("Flask Services Endpoint", self.test_flask_services_endpoint),
        ]
        
        # Run all tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            time.sleep(0.5)  # Brief pause for visual feedback
        
        # Generate final report
        self.generate_test_report()

if __name__ == "__main__":
    print("🏰 Starting Podplay Sanctuary Master Test Suite...")
    print("💜 This is attempt #44 - we're making it perfect!")
    
    runner = SanctuaryTestRunner()
    runner.run_all_tests()
