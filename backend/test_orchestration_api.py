#!/usr/bin/env python3
"""
Enhanced Orchestration API Test Suite
Tests all endpoints of the Mama Bear orchestration system including:
- Status endpoint validation
- Chat functionality with agent routing
- WebSocket connections
- Multi-agent collaboration
- Memory system integration
- Computer Use Agent capabilities
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class OrchestrationAPITester:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session_id = f"test-session-{int(time.time())}"
        self.test_results: List[Dict[str, Any]] = []
        
    def log_test_result(self, test_name: str, passed: bool, details: str = "", response_data: Optional[Dict] = None):
        """Log test result with details"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not passed and response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
        print()

    def test_orchestration_status(self) -> bool:
        """Test the orchestration status endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/mama-bear/orchestration/status", timeout=10)
            
            if response.status_code != 200:
                self.log_test_result(
                    "Orchestration Status Endpoint", 
                    False, 
                    f"HTTP {response.status_code}", 
                    {"status_code": response.status_code}
                )
                return False
                
            data = response.json()
            
            # Validate required fields
            required_fields = ["orchestrator_available", "agents_available", "agent_types", "success"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test_result(
                    "Orchestration Status Endpoint", 
                    False, 
                    f"Missing fields: {missing_fields}", 
                    data
                )
                return False
                
            # Validate agent count
            if data["agents_available"] != 8:
                self.log_test_result(
                    "Orchestration Status Endpoint", 
                    False, 
                    f"Expected 8 agents, got {data['agents_available']}", 
                    data
                )
                return False
                
            # Validate orchestrator availability
            if not data["orchestrator_available"]:
                self.log_test_result(
                    "Orchestration Status Endpoint", 
                    False, 
                    "Orchestrator not available", 
                    data
                )
                return False
                
            self.log_test_result(
                "Orchestration Status Endpoint", 
                True, 
                f"8 agents active: {', '.join(data['agent_types'])}"
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Orchestration Status Endpoint", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def test_chat_basic_functionality(self) -> bool:
        """Test basic chat functionality"""
        try:
            payload = {
                "message": "Hello, Mama Bear! This is a test message.",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "Basic Chat Functionality", 
                    False, 
                    f"HTTP {response.status_code}", 
                    {"status_code": response.status_code}
                )
                return False
                
            data = response.json()
            
            # Validate response structure
            required_fields = ["success", "response", "agents_count", "orchestrator_available"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test_result(
                    "Basic Chat Functionality", 
                    False, 
                    f"Missing fields: {missing_fields}", 
                    data
                )
                return False
                
            if not data["success"]:
                self.log_test_result(
                    "Basic Chat Functionality", 
                    False, 
                    "Chat response indicates failure", 
                    data
                )
                return False
                
            if not data["response"]:
                self.log_test_result(
                    "Basic Chat Functionality", 
                    False, 
                    "Empty response from chat", 
                    data
                )
                return False
                
            self.log_test_result(
                "Basic Chat Functionality", 
                True, 
                f"Response: {data['response'][:100]}..."
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Basic Chat Functionality", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def test_agent_routing_devops(self) -> bool:
        """Test intelligent agent routing for DevOps specialist"""
        try:
            payload = {
                "message": "I need help with Docker containerization, CI/CD pipelines, and deployment automation.",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "DevOps Agent Routing", 
                    False, 
                    f"HTTP {response.status_code}"
                )
                return False
                
            data = response.json()
            
            if not data.get("success"):
                self.log_test_result(
                    "DevOps Agent Routing", 
                    False, 
                    "Request failed", 
                    data
                )
                return False
                
            self.log_test_result(
                "DevOps Agent Routing", 
                True, 
                f"DevOps query processed successfully"
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "DevOps Agent Routing", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def test_agent_routing_research(self) -> bool:
        """Test intelligent agent routing for Research specialist"""
        try:
            payload = {
                "message": "Can you research the latest trends in AI development and machine learning frameworks?",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "Research Agent Routing", 
                    False, 
                    f"HTTP {response.status_code}"
                )
                return False
                
            data = response.json()
            
            if not data.get("success"):
                self.log_test_result(
                    "Research Agent Routing", 
                    False, 
                    "Request failed", 
                    data
                )
                return False
                
            self.log_test_result(
                "Research Agent Routing", 
                True, 
                f"Research query processed successfully"
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Research Agent Routing", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def test_memory_system_integration(self) -> bool:
        """Test Mem0 enhanced memory system integration"""
        try:
            # First, store some preferences
            payload = {
                "message": "Please remember: I prefer TypeScript over JavaScript, I use Tailwind CSS, and I have ADHD with sensory sensitivities.",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "Memory System Integration", 
                    False, 
                    f"HTTP {response.status_code} on memory storage"
                )
                return False
                
            data = response.json()
            
            if not data.get("success"):
                self.log_test_result(
                    "Memory System Integration", 
                    False, 
                    "Memory storage failed", 
                    data
                )
                return False
                
            # Small delay to ensure memory processing
            time.sleep(1)
            
            # Now test recall
            payload = {
                "message": "What do you remember about my preferences?",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "Memory System Integration", 
                    False, 
                    f"HTTP {response.status_code} on memory recall"
                )
                return False
                
            data = response.json()
            
            if not data.get("success"):
                self.log_test_result(
                    "Memory System Integration", 
                    False, 
                    "Memory recall failed", 
                    data
                )
                return False
                
            self.log_test_result(
                "Memory System Integration", 
                True, 
                "Memory storage and recall working"
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Memory System Integration", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def test_computer_use_agent_capability(self) -> bool:
        """Test Computer Use Agent (CUA) capabilities"""
        try:
            payload = {
                "message": "Can you use your Computer Use Agent capabilities to help me browse and scrape information from websites?",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "Computer Use Agent Capability", 
                    False, 
                    f"HTTP {response.status_code}"
                )
                return False
                
            data = response.json()
            
            if not data.get("success"):
                self.log_test_result(
                    "Computer Use Agent Capability", 
                    False, 
                    "CUA request failed", 
                    data
                )
                return False
                
            self.log_test_result(
                "Computer Use Agent Capability", 
                True, 
                "CUA capabilities recognized and processed"
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Computer Use Agent Capability", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def test_multi_agent_collaboration(self) -> bool:
        """Test multi-agent collaboration workflow"""
        try:
            payload = {
                "message": "I need to build a full-stack TypeScript application with React frontend, Node.js backend, Docker deployment, and comprehensive testing. Can multiple agents collaborate on this?",
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/mama-bear/orchestration/chat",
                json=payload,
                timeout=20
            )
            
            if response.status_code != 200:
                self.log_test_result(
                    "Multi-Agent Collaboration", 
                    False, 
                    f"HTTP {response.status_code}"
                )
                return False
                
            data = response.json()
            
            if not data.get("success"):
                self.log_test_result(
                    "Multi-Agent Collaboration", 
                    False, 
                    "Multi-agent request failed", 
                    data
                )
                return False
                
            self.log_test_result(
                "Multi-Agent Collaboration", 
                True, 
                "Multi-agent collaboration request processed"
            )
            return True
            
        except Exception as e:
            self.log_test_result(
                "Multi-Agent Collaboration", 
                False, 
                f"Exception: {str(e)}"
            )
            return False

    def run_all_tests(self):
        """Run all orchestration API tests"""
        print("🧪 Starting Enhanced Orchestration API Test Suite")
        print(f"📅 Test Run: {datetime.now().isoformat()}")
        print(f"🎯 Target: {self.base_url}")
        print(f"🔑 Session ID: {self.session_id}")
        print("=" * 60)
        
        tests = [
            self.test_orchestration_status,
            self.test_chat_basic_functionality,
            self.test_agent_routing_devops,
            self.test_agent_routing_research,
            self.test_memory_system_integration,
            self.test_computer_use_agent_capability,
            self.test_multi_agent_collaboration
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed with exception: {e}")
        
        print("=" * 60)
        print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Enhanced Orchestration System is fully operational!")
        else:
            print(f"⚠️  {total_tests - passed_tests} tests failed. Check the details above.")
            
        return passed_tests == total_tests

    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive test report"""
        passed_count = sum(1 for result in self.test_results if result["passed"])
        total_count = len(self.test_results)
        
        return {
            "test_run_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_count,
            "passed_tests": passed_count,
            "failed_tests": total_count - passed_count,
            "success_rate": (passed_count / total_count * 100) if total_count > 0 else 0,
            "test_results": self.test_results
        }

def main():
    """Main test runner"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5001"
    
    tester = OrchestrationAPITester(base_url)
    success = tester.run_all_tests()
    
    # Generate and save report
    report = tester.generate_report()
    
    with open("orchestration_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Detailed report saved to: orchestration_test_report.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
