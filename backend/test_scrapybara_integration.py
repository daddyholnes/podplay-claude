"""
Comprehensive integration test for Scrapybara computer use capabilities
Demonstrates Scout.new-level autonomous operations with multi-provider fallback
"""

import asyncio
import logging
import json
import os
import sys
from typing import Dict, Any

# Add backend to path for imports
sys.path.append('/home/woody/Documents/podplay-claude/backend')

try:
    from services.enhanced_scrapybara_orchestration import (
        create_enhanced_orchestrator,
        execute_predefined_workflow,
        AUTONOMOUS_WORKFLOWS
    )
    from services.scrapybara_integration import (
        ScrapybaraConfig,
        InstanceType,
        ModelProvider
    )
    from api.computer_use_api import create_computer_use_app
except ImportError as e:
    print(f"Import error: {e}")
    print("This test requires the Scrapybara integration modules")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScrapybaraIntegrationTest:
    """Comprehensive test suite for Scrapybara integration"""
    
    def __init__(self):
        self.orchestrator = None
        self.test_results = []
        
    async def setup(self):
        """Setup test environment"""
        logger.info("Setting up Scrapybara integration test...")
        
        # Create enhanced orchestrator
        self.orchestrator = create_enhanced_orchestrator(
            scrapybara_api_key=os.getenv('SCRAPYBARA_API_KEY'),
            max_instances=2,
            timeout_hours=1
        )
        
        logger.info("Enhanced orchestrator created successfully")
    
    async def test_system_capabilities(self):
        """Test system capabilities and status"""
        logger.info("Testing system capabilities...")
        
        if not self.orchestrator:
            logger.error("Orchestrator not initialized")
            self.test_results.append({
                "test": "system_capabilities",
                "success": False,
                "error": "Orchestrator not initialized"
            })
            return
        
        try:
            status = self.orchestrator.get_system_status()
            
            assert 'enhanced_orchestrator' in status
            assert 'scrapybara_capabilities' in status
            assert 'task_routing_categories' in status
            
            logger.info(f"System status: {json.dumps(status, indent=2)}")
            
            self.test_results.append({
                "test": "system_capabilities",
                "success": True,
                "details": status
            })
            
        except Exception as e:
            logger.error(f"System capabilities test failed: {e}")
            self.test_results.append({
                "test": "system_capabilities", 
                "success": False,
                "error": str(e)
            })
    
    async def test_task_routing(self):
        """Test intelligent task routing"""
        logger.info("Testing task routing...")
        
        if not self.orchestrator:
            logger.error("Orchestrator not initialized")
            self.test_results.append({
                "test": "task_routing",
                "success": False,
                "error": "Orchestrator not initialized"
            })
            return
        
        test_tasks = [
            {
                "description": "Take a screenshot of the desktop",
                "expected_handler": "scrapybara",
                "expected_category": "computer_use"
            },
            {
                "description": "Open browser and navigate to google.com",
                "expected_handler": "scrapybara", 
                "expected_category": "web_automation"
            },
            {
                "description": "Analyze the best Python web framework",
                "expected_handler": "mama_bear",
                "expected_category": "analysis"
            },
            {
                "description": "Create a development plan for a new project",
                "expected_handler": "mama_bear",
                "expected_category": "planning"
            }
        ]
        
        for task in test_tasks:
            try:
                analysis = self.orchestrator.analyze_task_requirements(task["description"])
                
                logger.info(f"Task: {task['description']}")
                logger.info(f"Analysis: {analysis}")
                
                # Verify routing decisions
                assert analysis["category"] == task["expected_category"], \
                    f"Expected category {task['expected_category']}, got {analysis['category']}"
                
                assert analysis["handler"] == task["expected_handler"], \
                    f"Expected handler {task['expected_handler']}, got {analysis['handler']}"
                
                self.test_results.append({
                    "test": f"task_routing_{task['expected_category']}",
                    "success": True,
                    "task": task["description"],
                    "analysis": analysis
                })
                
            except Exception as e:
                logger.error(f"Task routing test failed for '{task['description']}': {e}")
                self.test_results.append({
                    "test": f"task_routing_{task['expected_category']}",
                    "success": False,
                    "error": str(e)
                })
    
    async def test_simple_computer_task(self):
        """Test simple computer use task execution"""
        logger.info("Testing simple computer task...")
        
        try:
            # Test a simple task that should work in most environments
            result = await self.orchestrator.execute_autonomous_task(
                description="Check the current directory and list its contents",
                context={"working_directory": "/tmp"}
            )
            
            logger.info(f"Computer task result: {json.dumps(result, indent=2, default=str)}")
            
            assert result.get("success") is not None
            assert "task_id" in result
            assert "handler" in result
            
            self.test_results.append({
                "test": "simple_computer_task",
                "success": result.get("success", False),
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Simple computer task test failed: {e}")
            self.test_results.append({
                "test": "simple_computer_task",
                "success": False,
                "error": str(e)
            })
    
    async def test_session_management(self):
        """Test computer use session management"""
        logger.info("Testing session management...")
        
        try:
            # Create session
            session = await self.orchestrator.create_computer_use_session(
                session_name="test_session",
                instance_type=InstanceType.UBUNTU,
                timeout_hours=1
            )
            
            logger.info(f"Session created: {json.dumps(session, indent=2, default=str)}")
            
            if "error" not in session:
                session_id = session["session_id"]
                
                # Get session status
                status = self.orchestrator.scrapybara.manager.get_instance_status(session_id)
                logger.info(f"Session status: {json.dumps(status, indent=2, default=str)}")
                
                # Stop session
                stop_result = await self.orchestrator.scrapybara.manager.stop_instance(session_id)
                logger.info(f"Session stopped: {stop_result}")
                
                self.test_results.append({
                    "test": "session_management",
                    "success": True,
                    "session": session,
                    "stopped": stop_result
                })
            else:
                self.test_results.append({
                    "test": "session_management", 
                    "success": False,
                    "error": session.get("error")
                })
                
        except Exception as e:
            logger.error(f"Session management test failed: {e}")
            self.test_results.append({
                "test": "session_management",
                "success": False,
                "error": str(e)
            })
    
    async def test_multi_step_workflow(self):
        """Test multi-step workflow execution"""
        logger.info("Testing multi-step workflow...")
        
        try:
            # Simple multi-step workflow
            steps = [
                "Check the current working directory",
                "Create a test file with current timestamp",
                "Verify the file was created successfully"
            ]
            
            result = await self.orchestrator.execute_multi_step_workflow(
                workflow_steps=steps,
                context={"test_directory": "/tmp"}
            )
            
            logger.info(f"Multi-step workflow result: {json.dumps(result, indent=2, default=str)}")
            
            assert "workflow_id" in result
            assert "total_steps" in result
            assert result["total_steps"] == len(steps)
            
            self.test_results.append({
                "test": "multi_step_workflow",
                "success": result.get("overall_success", False),
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Multi-step workflow test failed: {e}")
            self.test_results.append({
                "test": "multi_step_workflow",
                "success": False,
                "error": str(e)
            })
    
    async def test_predefined_workflow(self):
        """Test predefined workflow execution"""
        logger.info("Testing predefined workflow...")
        
        try:
            # Test development setup workflow (simplified)
            result = await execute_predefined_workflow(
                self.orchestrator,
                "development_setup",
                {
                    "project_name": "test_project",
                    "language": "python",
                    "working_directory": "/tmp"
                }
            )
            
            logger.info(f"Predefined workflow result: {json.dumps(result, indent=2, default=str)}")
            
            assert "workflow_id" in result
            assert "total_steps" in result
            
            self.test_results.append({
                "test": "predefined_workflow", 
                "success": result.get("overall_success", False),
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Predefined workflow test failed: {e}")
            self.test_results.append({
                "test": "predefined_workflow",
                "success": False,
                "error": str(e)
            })
    
    async def test_flask_api_integration(self):
        """Test Flask API integration"""
        logger.info("Testing Flask API integration...")
        
        try:
            # Create Flask app
            app, socketio = create_computer_use_app(self.orchestrator.mama_bear)
            
            # Test app creation
            assert app is not None
            assert socketio is not None
            
            # Test app configuration
            with app.app_context():
                # Test routes are registered
                routes = [rule.rule for rule in app.url_map.iter_rules()]
                expected_routes = [
                    '/api/computer-use/status',
                    '/api/computer-use/execute',
                    '/api/computer-use/workflows',
                    '/api/computer-use/health'
                ]
                
                for route in expected_routes:
                    assert route in routes, f"Route {route} not found"
                
                logger.info(f"Flask app routes: {routes}")
            
            self.test_results.append({
                "test": "flask_api_integration",
                "success": True,
                "routes": routes
            })
            
        except Exception as e:
            logger.error(f"Flask API integration test failed: {e}")
            self.test_results.append({
                "test": "flask_api_integration",
                "success": False,
                "error": str(e)
            })
    
    async def run_all_tests(self):
        """Run all integration tests"""
        logger.info("Starting comprehensive Scrapybara integration tests...")
        
        await self.setup()
        
        # Run tests
        await self.test_system_capabilities()
        await self.test_task_routing()
        await self.test_simple_computer_task()
        await self.test_session_management()
        await self.test_multi_step_workflow()
        await self.test_predefined_workflow()
        await self.test_flask_api_integration()
        
        # Cleanup
        await self.cleanup()
        
        # Generate report
        self.generate_report()
    
    async def cleanup(self):
        """Cleanup test resources"""
        logger.info("Cleaning up test resources...")
        
        try:
            # Stop any remaining instances
            instances = self.orchestrator.scrapybara.manager.instances.copy()
            for instance_id in instances:
                await self.orchestrator.scrapybara.manager.stop_instance(instance_id)
            
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        logger.info("Generating test report...")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result.get("success"))
        success_rate = successful_tests / total_tests if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "success_rate": f"{success_rate:.2%}"
            },
            "test_results": self.test_results,
            "system_info": {
                "scrapybara_available": True,  # If we got this far
                "python_version": sys.version,
                "platform": sys.platform
            }
        }
        
        # Save report to file
        report_file = "/tmp/scrapybara_integration_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Test report saved to: {report_file}")
        logger.info(f"Test Summary: {successful_tests}/{total_tests} tests passed ({success_rate:.2%})")
        
        # Print summary
        print("\n" + "="*60)
        print("SCRAPYBARA INTEGRATION TEST REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {success_rate:.2%}")
        print("="*60)
        
        for result in self.test_results:
            status = "✅ PASS" if result.get("success") else "❌ FAIL"
            print(f"{status} {result['test']}")
            if not result.get("success") and "error" in result:
                print(f"   Error: {result['error']}")
        
        print("="*60)
        print(f"Detailed report: {report_file}")
        print("="*60)


async def main():
    """Main test execution"""
    test_suite = ScrapybaraIntegrationTest()
    await test_suite.run_all_tests()


if __name__ == "__main__":
    # Check for Scrapybara API key
    if not os.getenv('SCRAPYBARA_API_KEY'):
        print("Warning: SCRAPYBARA_API_KEY not set. Some tests may fail.")
        print("You can still run the tests to check the integration architecture.")
        
        # Ask user if they want to continue
        try:
            response = input("Continue with tests? (y/n): ").lower().strip()
            if response != 'y':
                print("Tests cancelled.")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\nTests cancelled.")
            sys.exit(0)
    
    # Run tests
    asyncio.run(main())
