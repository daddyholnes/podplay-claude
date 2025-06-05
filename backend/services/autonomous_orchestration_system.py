"""
🐻 Autonomous Orchestration System - Scout.new Level Integration
Combines Workflow Intelligence + Enhanced Session Management for autonomous execution
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from enum import Enum
import uuid

# Import the enhanced session manager
from .enhanced_session_manager import (
    EnhancedSessionManager, 
    EnhancedSession, 
    SessionType, 
    SessionState,
    SessionCheckpoint
)

# Import workflow intelligence (assuming it's moved to services)
from .mama_bear_workflow_logic import (
    WorkflowIntelligence,
    CollaborationOrchestrator,
    WorkflowDecision,
    WorkflowType,
    DecisionConfidence,
    initialize_workflow_intelligence
)

logger = logging.getLogger(__name__)

class AutonomousTaskState(Enum):
    """States for autonomous task execution"""
    PLANNING = "planning"
    EXECUTING = "executing"
    COLLABORATING = "collaborating"
    CHECKPOINTING = "checkpointing"
    MONITORING = "monitoring"
    COMPLETED = "completed"
    FAILED = "failed"
    SUSPENDED = "suspended"

@dataclass
class AutonomousTask:
    """Represents a long-running autonomous task"""
    task_id: str
    session_id: str
    user_id: str
    original_request: str
    task_state: AutonomousTaskState
    workflow_decision: WorkflowDecision
    
    # Execution tracking
    created_at: datetime
    started_at: Optional[datetime] = None
    last_checkpoint: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    
    # Progress tracking
    progress_percentage: float = 0.0
    current_phase: str = "initialization"
    steps_completed: List[str] = field(default_factory=list)
    steps_remaining: List[str] = field(default_factory=list)
    
    # Agent collaboration
    active_agents: List[str] = field(default_factory=list)
    agent_results: Dict[str, Any] = field(default_factory=dict)
    collaboration_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Autonomous features
    auto_recovery_attempts: int = 0
    max_auto_recovery: int = 3
    can_self_modify: bool = True
    requires_human_approval: bool = False
    
    # Scout.new style context
    context_memory: Dict[str, Any] = field(default_factory=dict)
    learned_patterns: List[str] = field(default_factory=list)
    adaptation_history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if self.steps_completed is None:
            self.steps_completed = []
        if self.steps_remaining is None:
            self.steps_remaining = []
        if self.active_agents is None:
            self.active_agents = []
        if self.agent_results is None:
            self.agent_results = {}
        if self.collaboration_history is None:
            self.collaboration_history = []
        if self.context_memory is None:
            self.context_memory = {}
        if self.learned_patterns is None:
            self.learned_patterns = []
        if self.adaptation_history is None:
            self.adaptation_history = []

class AutonomousOrchestrationSystem:
    """
    🤖 Scout.new-level autonomous orchestration system
    Combines workflow intelligence with persistent session management
    """
    
    def __init__(self, config: Dict[str, Any], model_manager, memory_manager):
        self.config = config
        self.model_manager = model_manager
        self.memory_manager = memory_manager
        
        # Initialize enhanced session manager
        self.session_manager = EnhancedSessionManager(config)
        
        # Initialize workflow intelligence (will be set by initialize method)
        self.workflow_intelligence = None
        self.collaboration_orchestrator = None
        
        # Active autonomous tasks
        self.active_autonomous_tasks: Dict[str, AutonomousTask] = {}
        
        # Background monitoring
        self._monitoring_tasks = set()
        
    async def initialize(self):
        """Initialize async components"""
        # Initialize workflow intelligence
        try:
            self.workflow_intelligence = await initialize_workflow_intelligence(
                self.model_manager, self.memory_manager
            )
            # Create collaboration orchestrator separately 
            from .mama_bear_workflow_logic import create_collaboration_orchestrator
            self.collaboration_orchestrator = create_collaboration_orchestrator(self.workflow_intelligence)
        except Exception as e:
            logger.warning(f"Failed to initialize workflow intelligence: {e}")
            # Set fallbacks
            self.workflow_intelligence = None
            self.collaboration_orchestrator = None
        self._shutdown_event = asyncio.Event()
        
        logger.info("🚀 Autonomous Orchestration System initialized")
    
    async def create_autonomous_session(
        self,
        user_id: str,
        request_message: str,
        context: Dict[str, Any],
        autonomous_mode: bool = True,
        max_runtime_hours: int = 24
    ) -> Tuple[EnhancedSession, AutonomousTask]:
        """
        Create a new autonomous session with Scout.new-level capabilities
        """
        
        # Analyze the request to determine workflow with None guard
        if self.workflow_intelligence:
            workflow_decision = await self.workflow_intelligence.analyze_request_intent(
                request_message, context
            )
        else:
            # Create default workflow decision
            from .mama_bear_workflow_logic import WorkflowDecision, DecisionConfidence
            workflow_decision = WorkflowDecision(
                decision_type="simple",
                selected_agents=["lead_developer"],
                confidence=DecisionConfidence.MEDIUM,
                reasoning="Default workflow - workflow intelligence not available",
                estimated_duration=10,
                estimated_complexity=5
            )
        
        # Determine session type based on workflow
        session_type = self._map_workflow_to_session_type(workflow_decision)
        
        # Create enhanced session
        session = await self.session_manager.create_session(
            user_id=user_id,
            session_type=session_type,
            metadata={
                "original_request": request_message,
                "workflow_type": workflow_decision.decision_type,
                "autonomous_mode": autonomous_mode,
                "estimated_complexity": workflow_decision.estimated_complexity,
                "estimated_duration": workflow_decision.estimated_duration
            },
            agent_id=workflow_decision.selected_agents[0] if workflow_decision.selected_agents else None,
            task_description=request_message,
            max_runtime_hours=max_runtime_hours
        )
        
        # Create autonomous task
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        autonomous_task = AutonomousTask(
            task_id=task_id,
            session_id=session.session_id,
            user_id=user_id,
            original_request=request_message,
            task_state=AutonomousTaskState.PLANNING,
            workflow_decision=workflow_decision,
            created_at=datetime.now(),
            active_agents=workflow_decision.selected_agents.copy(),
            context_memory=context.copy()
        )
        
        # Store autonomous task
        self.active_autonomous_tasks[task_id] = autonomous_task
        
        # Start autonomous execution if enabled
        if autonomous_mode:
            await self._start_autonomous_execution(task_id)
        
        logger.info(f"✅ Created autonomous session {session.session_id} with task {task_id}")
        
        return session, autonomous_task
    
    async def execute_autonomous_task(self, task_id: str) -> Dict[str, Any]:
        """
        Execute an autonomous task with Scout.new-level capabilities
        """
        
        task = self.active_autonomous_tasks.get(task_id)
        if not task:
            return {"success": False, "error": "Task not found"}
        
        session = await self.session_manager.get_session(task.session_id)
        if not session:
            return {"success": False, "error": "Session not found"}
        
        try:
            # Update task state
            task.task_state = AutonomousTaskState.EXECUTING
            task.started_at = datetime.now()
            
            # Calculate estimated completion
            estimated_duration = timedelta(minutes=task.workflow_decision.estimated_duration)
            task.estimated_completion = task.started_at + estimated_duration
            
            # Create initial checkpoint
            await self.session_manager.create_checkpoint(
                task.session_id,
                "Starting autonomous execution",
                {
                    "task_id": task_id,
                    "workflow_decision": asdict(task.workflow_decision),
                    "execution_plan": self._create_execution_plan(task)
                }
            )
            
            # Execute based on workflow type
            if len(task.active_agents) == 1:
                result = await self._execute_single_agent_task(task)
            else:
                result = await self._execute_collaborative_task(task)
            
            # Update session and task
            await self._update_task_progress(task, result)
            
            # Create completion checkpoint
            if result.get("success"):
                task.task_state = AutonomousTaskState.COMPLETED
                task.progress_percentage = 100.0
                session.state = SessionState.COMPLETED
                
                await self.session_manager.create_checkpoint(
                    task.session_id,
                    "Task completed successfully",
                    {
                        "final_result": result,
                        "completion_time": datetime.now().isoformat(),
                        "total_duration": (datetime.now() - task.started_at).total_seconds() if task.started_at else 0
                    }
                )
            
            await self.session_manager.update_session(task.session_id, {
                "progress": task.progress_percentage,
                "state": session.state
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing autonomous task {task_id}: {e}")
            
            # Auto-recovery attempt
            if task.auto_recovery_attempts < task.max_auto_recovery:
                return await self._attempt_auto_recovery(task, str(e))
            else:
                task.task_state = AutonomousTaskState.FAILED
                return {"success": False, "error": str(e), "recovery_exhausted": True}
    
    async def resume_autonomous_task(self, task_id: str, checkpoint_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Resume an autonomous task from checkpoint (Scout.new style)
        """
        
        task = self.active_autonomous_tasks.get(task_id)
        if not task:
            return {"success": False, "error": "Task not found"}
        
        # Resume session from checkpoint
        session = await self.session_manager.resume_from_checkpoint(task.session_id, checkpoint_id)
        if not session:
            return {"success": False, "error": "Could not resume session"}
        
        # Restore task state from checkpoint
        latest_checkpoint = session.checkpoints[-1] if session.checkpoints else None
        if latest_checkpoint and latest_checkpoint.state_data:
            task_data = latest_checkpoint.state_data.get("task_state", {})
            if task_data:
                # Restore task progress
                task.progress_percentage = task_data.get("progress", 0.0)
                task.steps_completed = task_data.get("steps_completed", [])
                task.current_phase = task_data.get("current_phase", "resuming")
        
        task.task_state = AutonomousTaskState.EXECUTING
        
        logger.info(f"🔄 Resumed autonomous task {task_id} from checkpoint")
        
        # Continue execution
        return await self.execute_autonomous_task(task_id)
    
    async def monitor_long_running_tasks(self):
        """
        Background monitoring for long-running autonomous tasks
        """
        
        while not self._shutdown_event.is_set():
            try:
                current_time = datetime.now()
                
                for task_id, task in list(self.active_autonomous_tasks.items()):
                    
                    # Check if task needs checkpointing
                    if (task.task_state == AutonomousTaskState.EXECUTING and
                        (not task.last_checkpoint or 
                         (current_time - task.last_checkpoint).seconds >= 300)):  # 5 minutes
                        
                        await self._create_autonomous_checkpoint(task)
                    
                    # Check if task has exceeded estimated time
                    if (task.estimated_completion and 
                        current_time > task.estimated_completion and
                        task.task_state == AutonomousTaskState.EXECUTING):
                        
                        await self._handle_overrun_task(task)
                    
                    # Check for stuck tasks
                    if (task.started_at and 
                        (current_time - task.started_at).seconds > 3600 and  # 1 hour
                        task.progress_percentage < 10):
                        
                        await self._handle_stuck_task(task)
                
                # Cleanup completed tasks older than 24 hours
                await self._cleanup_old_tasks()
                
                # Wait before next monitoring cycle
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in autonomous task monitoring: {e}")
                await asyncio.sleep(60)
    
    async def get_autonomous_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get detailed status of an autonomous task"""
        
        task = self.active_autonomous_tasks.get(task_id)
        if not task:
            return {"success": False, "error": "Task not found"}
        
        session = await self.session_manager.get_session(task.session_id)
        
        return {
            "success": True,
            "task": {
                "task_id": task.task_id,
                "session_id": task.session_id,
                "state": task.task_state.value,
                "progress": task.progress_percentage,
                "current_phase": task.current_phase,
                "active_agents": task.active_agents,
                "steps_completed": len(task.steps_completed),
                "steps_remaining": len(task.steps_remaining),
                "estimated_completion": task.estimated_completion.isoformat() if task.estimated_completion else None,
                "auto_recovery_attempts": task.auto_recovery_attempts,
                "can_self_modify": task.can_self_modify
            },
            "session": {
                "session_id": session.session_id if session else None,
                "session_state": session.state.value if session else None,
                "checkpoints": len(session.checkpoints) if session else 0,
                "total_tokens": session.tokens_used if session else 0,
                "cost_estimate": session.cost_estimate if session else 0.0
            },
            "workflow": {
                "type": task.workflow_decision.decision_type,
                "confidence": task.workflow_decision.confidence.value,
                "estimated_complexity": task.workflow_decision.estimated_complexity,
                "estimated_duration": task.workflow_decision.estimated_duration
            }
        }
    
    # Private methods
    
    def _map_workflow_to_session_type(self, workflow_decision: WorkflowDecision) -> SessionType:
        """Map workflow type to session type"""
        
        mapping = {
            WorkflowType.SIMPLE_QUERY.value: SessionType.CHAT,
            WorkflowType.RESEARCH_TASK.value: SessionType.RESEARCH,
            WorkflowType.CODE_GENERATION.value: SessionType.LONG_RUNNING,
            WorkflowType.DEPLOYMENT_TASK.value: SessionType.WORKFLOW,
            WorkflowType.COMPLEX_PROJECT.value: SessionType.LONG_RUNNING,
            WorkflowType.TROUBLESHOOTING.value: SessionType.CHAT,
            WorkflowType.LEARNING_SESSION.value: SessionType.RESEARCH
        }
        
        return mapping.get(workflow_decision.decision_type, SessionType.CHAT)
    
    def _create_execution_plan(self, task: AutonomousTask) -> Dict[str, Any]:
        """Create detailed execution plan for autonomous task"""
        
        plan = {
            "phases": [],
            "agent_assignments": {},
            "checkpoint_schedule": [],
            "success_criteria": [],
            "risk_mitigation": []
        }
        
        # Create phases based on workflow type
        workflow_type = task.workflow_decision.decision_type
        
        if workflow_type == WorkflowType.COMPLEX_PROJECT.value:
            plan["phases"] = ["analysis", "design", "implementation", "testing", "deployment"]
        elif workflow_type == WorkflowType.RESEARCH_TASK.value:
            plan["phases"] = ["scoping", "data_gathering", "analysis", "synthesis", "validation"]
        elif workflow_type == WorkflowType.CODE_GENERATION.value:
            plan["phases"] = ["requirements", "design", "coding", "testing", "documentation"]
        else:
            plan["phases"] = ["analysis", "execution", "validation"]
        
        # Assign agents to phases
        for i, agent in enumerate(task.active_agents):
            plan["agent_assignments"][agent] = plan["phases"][i % len(plan["phases"])]
        
        # Schedule checkpoints
        for i, phase in enumerate(plan["phases"]):
            plan["checkpoint_schedule"].append({
                "phase": phase,
                "checkpoint_time": (i + 1) * 5,  # Every 5 minutes per phase
                "success_criteria": f"Complete {phase} phase"
            })
        
        return plan
    
    async def _execute_single_agent_task(self, task: AutonomousTask) -> Dict[str, Any]:
        """Execute task with single agent"""
        
        agent_id = task.active_agents[0]
        
        # Update progress
        task.current_phase = f"executing_with_{agent_id}"
        task.progress_percentage = 25.0
        
        # Execute with collaboration orchestrator
        if self.collaboration_orchestrator:
            # Create a workflow decision for the single agent
            from .mama_bear_workflow_logic import WorkflowDecision, DecisionConfidence
            single_agent_decision = WorkflowDecision(
                decision_type="simple",
                selected_agents=[agent_id],
                confidence=DecisionConfidence.HIGH,
                reasoning=f"Single agent execution with {agent_id}",
                estimated_duration=task.workflow_decision.estimated_duration,
                estimated_complexity=task.workflow_decision.estimated_complexity
            )
            
            result = await self.collaboration_orchestrator._execute_simple_delegation(
                single_agent_decision,
                task.original_request, 
                task.context_memory
            )
        else:
            # Fallback result when no collaboration orchestrator
            result = {
                "success": True,
                "type": "fallback_execution",
                "content": f"Executed with {agent_id}: {task.original_request}",
                "selected_agent": agent_id,
                "reasoning": "No collaboration orchestrator available"
            }
        
        # Update task state
        task.agent_results[agent_id] = result
        task.steps_completed.append(f"executed_with_{agent_id}")
        
        if result.get("success"):
            task.progress_percentage = 100.0
            task.current_phase = "completed"
        
        return result
    
    async def _execute_collaborative_task(self, task: AutonomousTask) -> Dict[str, Any]:
        """Execute task with multiple agents collaboratively"""
        
        task.task_state = AutonomousTaskState.COLLABORATING
        task.current_phase = "multi_agent_collaboration"
        task.progress_percentage = 20.0
        
        # Execute collaborative workflow
        if self.collaboration_orchestrator:
            result = await self.collaboration_orchestrator.orchestrate_collaborative_workflow(
                task.workflow_decision,
                task.original_request,
                task.context_memory
            )
        else:
            # Fallback for multi-agent collaboration
            result = {
                "success": True,
                "type": "fallback_collaboration",
                "content": f"Multi-agent collaboration with {len(task.active_agents)} agents: {task.original_request}",
                "agents": task.active_agents,
                "reasoning": "No collaboration orchestrator available"
            }
        
        # Track collaboration
        task.collaboration_history.append({
            "timestamp": datetime.now().isoformat(),
            "participating_agents": task.active_agents,
            "result_type": result.get("type"),
            "success": result.get("success")
        })
        
        # Update progress based on result
        if result.get("success"):
            task.progress_percentage = 100.0
            task.current_phase = "completed"
        else:
            task.progress_percentage = 50.0
            task.current_phase = "collaboration_issues"
        
        return result
    
    async def _update_task_progress(self, task: AutonomousTask, result: Dict[str, Any]):
        """Update task progress and session"""
        
        # Update session with tokens and costs (if available)
        if "metadata" in result:
            metadata = result["metadata"]
            
            session_updates = {}
            if "tokens_used" in metadata:
                session_updates["tokens_used"] = metadata["tokens_used"]
            if "api_calls" in metadata:
                session_updates["api_calls"] = metadata["api_calls"]
            if "cost_estimate" in metadata:
                session_updates["cost_estimate"] = metadata["cost_estimate"]
            
            if session_updates:
                await self.session_manager.update_session(task.session_id, session_updates)
        
        # Record performance for workflow intelligence
        if self.workflow_intelligence:
            await self.workflow_intelligence.update_agent_performance(
                task.active_agents[0] if task.active_agents else "unknown",
                {
                    "success": result.get("success", False),
                    "duration": result.get("duration", 0),
                    "complexity": task.workflow_decision.estimated_complexity,
                    "user_satisfaction": 4 if result.get("success") else 2  # Estimated
                }
            )
    
    async def _attempt_auto_recovery(self, task: AutonomousTask, error: str) -> Dict[str, Any]:
        """Attempt automatic recovery from task failure"""
        
        task.auto_recovery_attempts += 1
        task.task_state = AutonomousTaskState.MONITORING
        
        logger.info(f"🔧 Attempting auto-recovery for task {task.task_id} (attempt {task.auto_recovery_attempts})")
        
        # Try fallback agents if available
        fallback_agents = task.workflow_decision.fallback_options
        if fallback_agents and task.auto_recovery_attempts == 1:
            
            task.active_agents = [fallback_agents[0]]
            task.current_phase = f"auto_recovery_with_{fallback_agents[0]}"
            
            # Record adaptation
            task.adaptation_history.append({
                "timestamp": datetime.now().isoformat(),
                "adaptation_type": "agent_fallback",
                "original_error": error,
                "fallback_agent": fallback_agents[0]
            })
            
            return await self._execute_single_agent_task(task)
        
        # Try simplified approach
        elif task.auto_recovery_attempts == 2:
            
            # Simplify the request
            simplified_request = f"Help with: {task.original_request[:100]}... (simplified approach)"
            task.original_request = simplified_request
            task.current_phase = "simplified_execution"
            
            task.adaptation_history.append({
                "timestamp": datetime.now().isoformat(),
                "adaptation_type": "simplified_request",
                "original_error": error
            })
            
            return await self._execute_single_agent_task(task)
        
        # Final attempt with lead developer
        elif task.auto_recovery_attempts == 3:
            
            task.active_agents = ["lead_developer"]
            task.current_phase = "final_recovery_attempt"
            
            recovery_request = f"Previous attempts failed with error: {error}. Please help with: {task.original_request}"
            task.original_request = recovery_request
            
            task.adaptation_history.append({
                "timestamp": datetime.now().isoformat(),
                "adaptation_type": "lead_developer_escalation",
                "original_error": error
            })
            
            return await self._execute_single_agent_task(task)
        
        # Recovery exhausted
        task.task_state = AutonomousTaskState.FAILED
        return {
            "success": False,
            "error": f"Auto-recovery exhausted after {task.auto_recovery_attempts} attempts. Last error: {error}",
            "recovery_attempts": task.auto_recovery_attempts,
            "adaptation_history": task.adaptation_history
        }
    
    async def _create_autonomous_checkpoint(self, task: AutonomousTask):
        """Create autonomous checkpoint for long-running task"""
        
        checkpoint_data = {
            "task_state": {
                "progress": task.progress_percentage,
                "current_phase": task.current_phase,
                "steps_completed": task.steps_completed,
                "steps_remaining": task.steps_remaining,
                "active_agents": task.active_agents,
                "adaptation_history": task.adaptation_history[-5:],  # Last 5 adaptations
            },
            "execution_context": task.context_memory,
            "agent_results": task.agent_results
        }
        
        await self.session_manager.create_checkpoint(
            task.session_id,
            f"Autonomous checkpoint - {task.current_phase} ({task.progress_percentage:.1f}%)",
            checkpoint_data
        )
        
        task.last_checkpoint = datetime.now()
        
        logger.info(f"📍 Auto-checkpoint created for task {task.task_id}")
    
    async def _handle_overrun_task(self, task: AutonomousTask):
        """Handle task that has exceeded estimated time"""
        
        logger.warning(f"⏰ Task {task.task_id} has exceeded estimated completion time")
        
        # Create checkpoint
        await self._create_autonomous_checkpoint(task)
        
        # Extend deadline if making progress
        if task.progress_percentage > 50:
            # Extend by 50% of original estimate
            original_duration = task.workflow_decision.estimated_duration
            extension = timedelta(minutes=original_duration * 0.5)
            if task.estimated_completion:
                task.estimated_completion += extension
            
            task.adaptation_history.append({
                "timestamp": datetime.now().isoformat(),
                "adaptation_type": "deadline_extension",
                "reason": "making_good_progress",
                "new_deadline": task.estimated_completion.isoformat() if task.estimated_completion else None
            })
            
            logger.info(f"⏱️ Extended deadline for task {task.task_id} due to good progress")
        
        # Otherwise, consider switching to simpler approach
        else:
            await self._attempt_auto_recovery(task, "Task exceeded estimated time with minimal progress")
    
    async def _handle_stuck_task(self, task: AutonomousTask):
        """Handle task that appears to be stuck"""
        
        logger.warning(f"🚨 Task {task.task_id} appears to be stuck")
        
        # Suspend task for human review
        task.task_state = AutonomousTaskState.SUSPENDED
        task.requires_human_approval = True
        
        # Create diagnostic checkpoint
        await self.session_manager.create_checkpoint(
            task.session_id,
            "Task suspended - appears stuck, requires human review",
            {
                "stuck_diagnosis": {
                    "running_time_hours": ((datetime.now() - task.started_at).total_seconds() / 3600) if task.started_at else 0,
                    "progress_made": task.progress_percentage,
                    "last_activity": task.current_phase,
                    "recovery_attempts": task.auto_recovery_attempts
                }
            }
        )
    
    async def _cleanup_old_tasks(self):
        """Clean up completed tasks older than 24 hours"""
        
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        tasks_to_remove = []
        for task_id, task in self.active_autonomous_tasks.items():
            if (task.task_state in [AutonomousTaskState.COMPLETED, AutonomousTaskState.FAILED] and
                task.created_at < cutoff_time):
                tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.active_autonomous_tasks[task_id]
            logger.info(f"🧹 Cleaned up old task {task_id}")
    
    async def _start_autonomous_execution(self, task_id: str):
        """Start autonomous execution in background"""
        
        async def execute_task():
            try:
                await self.execute_autonomous_task(task_id)
            except Exception as e:
                logger.error(f"Error in autonomous execution for task {task_id}: {e}")
        
        # Start execution task
        task = asyncio.create_task(execute_task())
        self._monitoring_tasks.add(task)
        task.add_done_callback(self._monitoring_tasks.discard)
        
        logger.info(f"🚀 Started autonomous execution for task {task_id}")
    
    async def shutdown(self):
        """Graceful shutdown of autonomous system"""
        
        logger.info("🔄 Shutting down Autonomous Orchestration System...")
        
        # Signal shutdown
        self._shutdown_event.set()
        
        # Wait for monitoring tasks to complete
        if self._monitoring_tasks:
            await asyncio.gather(*self._monitoring_tasks, return_exceptions=True)
        
        # Create final checkpoints for active tasks
        for task_id, task in self.active_autonomous_tasks.items():
            if task.task_state == AutonomousTaskState.EXECUTING:
                await self._create_autonomous_checkpoint(task)
        
        logger.info("✅ Autonomous Orchestration System shutdown complete")

# Integration function
def create_autonomous_orchestration_system(config: Dict[str, Any], model_manager, memory_manager) -> AutonomousOrchestrationSystem:
    """Create autonomous orchestration system with full integration"""
    return AutonomousOrchestrationSystem(config, model_manager, memory_manager)
