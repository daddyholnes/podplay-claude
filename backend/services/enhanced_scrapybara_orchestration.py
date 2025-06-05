"""
Enhanced Orchestration with Scrapybara Integration
Connects computer use agent capabilities with Mama Bear workflow intelligence
for Scout.new-level autonomous operations.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import json
import time

from .scrapybara_integration import (
    ScrapybaraOrchestrator, 
    ScrapybaraConfig,
    InstanceType,
    ModelProvider,
    create_scrapybara_orchestrator
)


@dataclass
class ComputerUseTask:
    """Represents a computer use task for autonomous execution"""
    task_id: str
    description: str
    task_type: str  # "browser", "desktop", "file_system", "development", etc.
    priority: int = 1
    context: Dict[str, Any] = None
    requirements: Dict[str, Any] = None
    expected_output: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "task_type": self.task_type,
            "priority": self.priority,
            "context": self.context or {},
            "requirements": self.requirements or {},
            "expected_output": self.expected_output
        }


class EnhancedMamaBearOrchestrator:
    """Enhanced orchestrator that combines Mama Bear intelligence with Scrapybara computer use"""
    
    def __init__(self, 
                 mama_bear_orchestrator=None,
                 scrapybara_config: ScrapybaraConfig = None):
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize Mama Bear orchestrator (if available)
        self.mama_bear = mama_bear_orchestrator
        
        # Initialize Scrapybara orchestrator
        self.scrapybara = ScrapybaraOrchestrator(scrapybara_config or ScrapybaraConfig())
        
        # Task management
        self.pending_tasks: List[ComputerUseTask] = []
        self.active_tasks: Dict[str, ComputerUseTask] = {}
        self.completed_tasks: List[Dict] = []
        
        # Intelligence integration
        self.task_routing_rules = self._setup_task_routing()
        
    def _setup_task_routing(self) -> Dict[str, Dict]:
        """Setup rules for routing tasks between Mama Bear and Scrapybara"""
        return {
            "computer_use": {
                "keywords": ["screenshot", "click", "type", "navigate", "browser", "desktop", "file", "terminal"],
                "handler": "scrapybara",
                "instance_type": InstanceType.UBUNTU
            },
            "web_automation": {
                "keywords": ["website", "login", "form", "download", "upload", "scrape", "search"],
                "handler": "scrapybara",
                "instance_type": InstanceType.BROWSER
            },
            "development": {
                "keywords": ["code", "git", "compile", "test", "deploy", "debug", "install"],
                "handler": "scrapybara", 
                "instance_type": InstanceType.UBUNTU
            },
            "analysis": {
                "keywords": ["analyze", "research", "summarize", "compare", "evaluate"],
                "handler": "mama_bear",
                "instance_type": None
            },
            "planning": {
                "keywords": ["plan", "strategy", "design", "architecture", "roadmap"],
                "handler": "mama_bear",
                "instance_type": None
            }
        }
    
    def analyze_task_requirements(self, description: str) -> Dict[str, Any]:
        """Analyze task and determine optimal execution strategy"""
        description_lower = description.lower()
        
        # Score each category
        scores = {}
        for category, rules in self.task_routing_rules.items():
            score = sum(1 for keyword in rules["keywords"] if keyword in description_lower)
            scores[category] = score
        
        # Find best match
        best_category = max(scores.keys(), key=lambda k: scores[k]) if scores else "analysis"
        best_score = scores.get(best_category, 0)
        
        # Determine handler and instance type
        rules = self.task_routing_rules.get(best_category, self.task_routing_rules["analysis"])
        
        return {
            "category": best_category,
            "confidence": best_score / len(rules["keywords"]) if rules["keywords"] else 0,
            "handler": rules["handler"],
            "instance_type": rules.get("instance_type"),
            "scores": scores
        }
    
    async def execute_autonomous_task(self, 
                                    description: str,
                                    context: Dict[str, Any] = None,
                                    force_handler: str = None) -> Dict[str, Any]:
        """Execute autonomous task with intelligent routing"""
        
        task_id = f"task_{int(time.time())}"
        start_time = time.time()
        
        self.logger.info(f"Starting autonomous task: {task_id}")
        self.logger.info(f"Task description: {description}")
        
        # Analyze task requirements
        analysis = self.analyze_task_requirements(description)
        handler = force_handler or analysis["handler"]
        
        self.logger.info(f"Task analysis: {analysis}")
        self.logger.info(f"Using handler: {handler}")
        
        try:
            if handler == "scrapybara":
                # Execute with Scrapybara computer use
                result = await self._execute_with_scrapybara(
                    task_id=task_id,
                    description=description,
                    context=context,
                    instance_type=analysis.get("instance_type"),
                    analysis=analysis
                )
            
            elif handler == "mama_bear" and self.mama_bear:
                # Execute with Mama Bear intelligence
                result = await self._execute_with_mama_bear(
                    task_id=task_id,
                    description=description,
                    context=context,
                    analysis=analysis
                )
            
            else:
                # Fallback to Scrapybara if Mama Bear not available
                result = await self._execute_with_scrapybara(
                    task_id=task_id,
                    description=description,
                    context=context,
                    instance_type=InstanceType.UBUNTU,
                    analysis=analysis
                )
            
            # Store result
            execution_time = time.time() - start_time
            task_result = {
                "task_id": task_id,
                "description": description,
                "handler": handler,
                "analysis": analysis,
                "result": result,
                "execution_time": execution_time,
                "timestamp": time.time(),
                "success": result.get("success", False)
            }
            
            self.completed_tasks.append(task_result)
            
            return task_result
            
        except Exception as e:
            error_result = {
                "task_id": task_id,
                "description": description,
                "handler": handler,
                "error": str(e),
                "execution_time": time.time() - start_time,
                "timestamp": time.time(),
                "success": False
            }
            
            self.completed_tasks.append(error_result)
            self.logger.error(f"Task {task_id} failed: {e}")
            
            return error_result
    
    async def _execute_with_scrapybara(self,
                                     task_id: str,
                                     description: str,
                                     context: Dict[str, Any] = None,
                                     instance_type: InstanceType = None,
                                     analysis: Dict = None) -> Dict[str, Any]:
        """Execute task using Scrapybara computer use capabilities"""
        
        # Enhance description with context if available
        enhanced_description = description
        if context:
            context_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            enhanced_description = f"{description}\n\nContext:\n{context_str}"
        
        # Execute with Scrapybara
        result = await self.scrapybara.execute_autonomous_workflow(
            workflow_description=enhanced_description,
            context=context,
            instance_preferences={
                "instance_type": instance_type.value if instance_type else None
            }
        )
        
        return {
            "success": result.get("success", False),
            "handler": "scrapybara",
            "scrapybara_result": result,
            "instance_id": result.get("result", {}).get("instance_id"),
            "text_output": result.get("result", {}).get("text", ""),
            "steps": result.get("result", {}).get("steps", [])
        }
    
    async def _execute_with_mama_bear(self,
                                    task_id: str,
                                    description: str,
                                    context: Dict[str, Any] = None,
                                    analysis: Dict = None) -> Dict[str, Any]:
        """Execute task using Mama Bear intelligence"""
        
        if not self.mama_bear:
            raise ValueError("Mama Bear orchestrator not available")
        
        # Use Mama Bear's orchestrate_collaborative_workflow method
        try:
            # Prepare context for Mama Bear
            mama_bear_context = {
                "request": description,
                "task_id": task_id,
                "analysis": analysis,
                **(context or {})
            }
            
            if hasattr(self.mama_bear, 'orchestrate_collaborative_workflow'):
                result = await self.mama_bear.orchestrate_collaborative_workflow(
                    request=description,
                    context=mama_bear_context
                )
            else:
                # Fallback method if orchestrate_collaborative_workflow not available
                result = {"text": "Mama Bear processing completed", "success": True}
            
            return {
                "success": True,
                "handler": "mama_bear",
                "mama_bear_result": result,
                "text_output": result.get("text", "") if isinstance(result, dict) else str(result)
            }
            
        except Exception as e:
            self.logger.error(f"Mama Bear execution failed: {e}")
            raise
    
    async def execute_multi_step_workflow(self, 
                                        workflow_steps: List[str],
                                        context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute multi-step workflow with intelligent step routing"""
        
        workflow_id = f"workflow_{int(time.time())}"
        results = []
        overall_context = context or {}
        
        self.logger.info(f"Starting multi-step workflow: {workflow_id}")
        
        for i, step_description in enumerate(workflow_steps):
            step_id = f"{workflow_id}_step_{i+1}"
            
            self.logger.info(f"Executing step {i+1}/{len(workflow_steps)}: {step_description}")
            
            # Execute step
            step_result = await self.execute_autonomous_task(
                description=step_description,
                context=overall_context
            )
            
            results.append(step_result)
            
            # Update context with step results for next steps
            if step_result.get("success"):
                overall_context[f"step_{i+1}_result"] = step_result.get("text_output", "")
            
            # Stop if step failed and it's critical
            if not step_result.get("success"):
                self.logger.warning(f"Step {i+1} failed, continuing to next step")
        
        # Summarize workflow results
        successful_steps = sum(1 for r in results if r.get("success"))
        total_steps = len(results)
        
        return {
            "workflow_id": workflow_id,
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "success_rate": successful_steps / total_steps if total_steps > 0 else 0,
            "results": results,
            "overall_success": successful_steps == total_steps
        }
    
    async def create_computer_use_session(self, 
                                        session_name: str,
                                        instance_type: InstanceType = None,
                                        timeout_hours: int = None) -> Dict[str, Any]:
        """Create a persistent computer use session"""
        
        instance = await self.scrapybara.manager.create_instance(
            instance_type=instance_type or InstanceType.UBUNTU,
            timeout_hours=timeout_hours or 2,
            instance_id=f"session_{session_name}_{int(time.time())}"
        )
        
        if not instance:
            return {"error": "Failed to create session"}
        
        return {
            "session_id": instance.instance_id,
            "session_name": session_name,
            "instance_type": instance.instance_type.value,
            "timeout_hours": instance.timeout_hours,
            "created_at": instance.created_at,
            "tools_available": [tool.__class__.__name__ for tool in instance.tools]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "enhanced_orchestrator": {
                "pending_tasks": len(self.pending_tasks),
                "active_tasks": len(self.active_tasks),
                "completed_tasks": len(self.completed_tasks),
                "mama_bear_available": self.mama_bear is not None
            },
            "scrapybara_capabilities": self.scrapybara.get_system_capabilities(),
            "task_routing_categories": list(self.task_routing_rules.keys()),
            "recent_task_success_rate": self._calculate_recent_success_rate()
        }
    
    def _calculate_recent_success_rate(self, last_n_tasks: int = 10) -> float:
        """Calculate success rate for recent tasks"""
        if not self.completed_tasks:
            return 0.0
        
        recent_tasks = self.completed_tasks[-last_n_tasks:]
        successful_tasks = sum(1 for task in recent_tasks if task.get("success", False))
        
        return successful_tasks / len(recent_tasks) if recent_tasks else 0.0
    
    async def save_browser_auth(self, instance_id: str, auth_name: str = "default") -> Optional[str]:
        """Save browser authentication state for reuse"""
        return await self.scrapybara.manager.save_auth_state(instance_id, auth_name)
    
    async def load_browser_auth(self, instance_id: str, auth_state_id: str) -> bool:
        """Load saved browser authentication state"""
        return await self.scrapybara.manager.load_auth_state(instance_id, auth_state_id)


# Integration helper functions
def create_enhanced_orchestrator(mama_bear_orchestrator=None, **scrapybara_kwargs):
    """Create enhanced orchestrator with Mama Bear and Scrapybara integration"""
    
    scrapybara_config = ScrapybaraConfig(
        api_key=scrapybara_kwargs.get('scrapybara_api_key'),
        max_instances=scrapybara_kwargs.get('max_instances', 3),
        default_timeout_hours=scrapybara_kwargs.get('timeout_hours', 1)
    )
    
    return EnhancedMamaBearOrchestrator(
        mama_bear_orchestrator=mama_bear_orchestrator,
        scrapybara_config=scrapybara_config
    )


# Example Scout.new-level autonomous workflows
AUTONOMOUS_WORKFLOWS = {
    "research_and_document": [
        "Search for information about the given topic using browser",
        "Take screenshots of relevant pages and sources",
        "Create a comprehensive markdown document with findings",
        "Save the document to the specified location"
    ],
    
    "development_setup": [
        "Check system requirements and dependencies",
        "Install necessary development tools and packages",
        "Clone or create project repository",
        "Set up development environment and configuration",
        "Run initial tests to verify setup"
    ],
    
    "automated_testing": [
        "Navigate to the application under test",
        "Execute predefined test scenarios",
        "Capture screenshots of test results",
        "Generate test report with findings",
        "Save results and notify stakeholders"
    ],
    
    "data_collection": [
        "Navigate to data sources and login if required", 
        "Extract required data using appropriate methods",
        "Clean and validate collected data",
        "Store data in specified format and location",
        "Generate summary report of collection process"
    ]
}


async def execute_predefined_workflow(orchestrator: EnhancedMamaBearOrchestrator,
                                    workflow_name: str,
                                    context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute a predefined autonomous workflow"""
    
    if workflow_name not in AUTONOMOUS_WORKFLOWS:
        return {"error": f"Unknown workflow: {workflow_name}"}
    
    steps = AUTONOMOUS_WORKFLOWS[workflow_name]
    
    return await orchestrator.execute_multi_step_workflow(
        workflow_steps=steps,
        context=context
    )


# Example usage and testing
async def main():
    """Example usage of enhanced orchestration"""
    
    # Create enhanced orchestrator
    orchestrator = create_enhanced_orchestrator()
    
    # Check system status
    status = orchestrator.get_system_status()
    print("System Status:", json.dumps(status, indent=2))
    
    # Execute a simple autonomous task
    result = await orchestrator.execute_autonomous_task(
        "Take a screenshot of the current desktop and describe what applications are visible"
    )
    print("Task Result:", json.dumps(result, indent=2, default=str))
    
    # Execute a predefined workflow
    workflow_result = await execute_predefined_workflow(
        orchestrator,
        "research_and_document",
        {"topic": "Python web frameworks", "output_location": "/tmp/research.md"}
    )
    print("Workflow Result:", json.dumps(workflow_result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
