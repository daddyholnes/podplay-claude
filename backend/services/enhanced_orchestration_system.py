# backend/services/enhanced_orchestration_system.py
"""
🐻 Enhanced Mama Bear Agent Orchestration System
Advanced orchestration with specialized agents, intelligent planning, and collaborative workflows
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    WAITING = "waiting"
    COLLABORATING = "collaborating"
    ERROR = "error"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentContext:
    """What each agent knows about the current situation"""
    agent_id: str
    current_task: Optional[str] = None
    user_intent: str = ""
    project_context: Dict[str, Any] = None
    conversation_history: List[Dict] = None
    available_tools: List[str] = None
    resource_limits: Dict[str, Any] = None
    collaboration_state: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.project_context is None:
            self.project_context = {}
        if self.conversation_history is None:
            self.conversation_history = []
        if self.available_tools is None:
            self.available_tools = []
        if self.resource_limits is None:
            self.resource_limits = {}
        if self.collaboration_state is None:
            self.collaboration_state = {}

@dataclass
class Task:
    """Represents a task that can be executed by agents"""
    id: str
    title: str
    description: str
    agent_type: str
    priority: TaskPriority
    status: TaskStatus
    dependencies: List[str] = None
    estimated_duration: int = 300  # seconds
    max_retries: int = 3
    current_attempt: int = 0
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.context is None:
            self.context = {}

@dataclass
class Plan:
    """A collection of tasks with dependencies and execution strategy"""
    id: str
    title: str
    description: str
    tasks: List[Task]
    user_id: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    estimated_completion: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class AgentCapability(ABC):
    """Base class for agent capabilities"""
    
    @abstractmethod
    async def can_handle(self, task: Task, context: AgentContext) -> bool:
        """Check if this capability can handle the given task"""
        pass
    
    @abstractmethod
    async def execute(self, task: Task, context: AgentContext) -> Dict[str, Any]:
        """Execute the task and return results"""
        pass

class ContextAwareness:
    """Manages what agents know about the current situation"""
    
    def __init__(self, memory_manager, model_manager):
        self.memory = memory_manager
        self.model_manager = model_manager
        self.global_context = {}
        self.agent_contexts = {}
        
    async def update_global_context(self, key: str, value: Any):
        """Update global context that all agents can access"""
        self.global_context[key] = {
            'value': value,
            'timestamp': datetime.now(),
            'source': 'system'
        }
        
        # Persist important context to memory
        if key in ['user_intent', 'project_state', 'active_plan']:
            await self.memory.save_context(key, value)
    
    async def get_agent_context(self, agent_id: str) -> AgentContext:
        """Get complete context for a specific agent"""
        if agent_id not in self.agent_contexts:
            self.agent_contexts[agent_id] = AgentContext(agent_id=agent_id)
        
        context = self.agent_contexts[agent_id]
        
        # Enrich context with relevant global information
        context.user_intent = self.global_context.get('user_intent', {}).get('value', '')
        context.project_context = self.global_context.get('project_state', {}).get('value', {})
        
        # Get recent conversation history from memory
        context.conversation_history = await self.memory.get_recent_conversations(
            agent_id=agent_id, 
            limit=10
        )
        
        # Get available tools and resources
        context.available_tools = await self._get_available_tools(agent_id)
        context.resource_limits = await self._get_resource_limits(agent_id)
        
        return context
    
    async def _get_available_tools(self, agent_id: str) -> List[str]:
        """Get tools available to this agent"""
        agent_type = agent_id.split('_')[0]  # e.g., 'scout_agent_1' -> 'scout'
        
        tool_mapping = {
            'scout': ['scrapybara', 'web_search', 'document_analysis', 'github_api'],
            'mama_bear': ['code_generation', 'planning', 'review', 'coordination'],
            'model_manager': ['model_selection', 'fine_tuning', 'deployment', 'monitoring'],
            'monitor': ['resource_tracking', 'alerting', 'quota_management', 'billing'],
            'planner': ['task_decomposition', 'dependency_analysis', 'estimation', 'optimization'],
            'research': ['web_scraping', 'document_analysis', 'data_synthesis', 'trend_analysis'],
            'devops': ['deployment', 'monitoring', 'infrastructure', 'CI/CD'],
            'integration': ['api_design', 'system_integration', 'data_flow', 'service_mesh'],
            'live_api': ['real_time_data', 'webhooks', 'streaming', 'event_processing']
        }
        
        return tool_mapping.get(agent_type, [])
    
    async def _get_resource_limits(self, agent_id: str) -> Dict[str, Any]:
        """Get resource limits for this agent"""
        # Check current quota status from model manager
        model_status = self.model_manager.get_model_status()
        
        return {
            'api_quota_remaining': sum(
                model['quota_limit'] - model['quota_used'] 
                for model in model_status['models']
            ),
            'scrapybara_instances': 5,  # Max concurrent instances
            'memory_limit_mb': 1024,
            'execution_timeout': 3600  # 1 hour max execution
        }

class EnhancedAgentOrchestrator:
    """Enhanced orchestration with specialized agents and intelligent coordination"""
    
    def __init__(self, memory_manager, model_manager, scrapybara_client):
        self.memory = memory_manager
        self.model_manager = model_manager
        self.scrapybara = scrapybara_client
        self.context_awareness = ContextAwareness(memory_manager, model_manager)
        
        # Enhanced workflow systems
        self.workflow_intelligence = None
        self.collaboration_orchestrator = None
        
        # Agent registry
        self.agents = {}
        self.active_tasks = {}
        self.task_queue = deque()
        self.completed_tasks = {}
        
        # Communication channels
        self.agent_messages = defaultdict(deque)
        self.collaboration_sessions = {}
        
        # Performance tracking
        self.agent_performance = defaultdict(lambda: {'success_rate': 0.8, 'avg_response_time': 2.0})
        
        # Initialize specialized agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize enhanced specialized agents"""
        
        # Import specialized agent variants
        try:
            from .mama_bear_specialized_variants import (
                ResearchSpecialist, DevOpsSpecialist, ScoutCommander,
                ModelCoordinator, ToolCurator, IntegrationArchitect, 
                LiveAPISpecialist
            )
            
            self.agents = {
                'research_specialist': MamaBearAgent('research_specialist', ResearchSpecialist(), self),
                'devops_specialist': MamaBearAgent('devops_specialist', DevOpsSpecialist(), self),
                'scout_commander': MamaBearAgent('scout_commander', ScoutCommander(), self),
                'model_coordinator': MamaBearAgent('model_coordinator', ModelCoordinator(), self),
                'tool_curator': MamaBearAgent('tool_curator', ToolCurator(), self),
                'integration_architect': MamaBearAgent('integration_architect', IntegrationArchitect(), self),
                'live_api_specialist': MamaBearAgent('live_api_specialist', LiveAPISpecialist(), self),
                'lead_developer': LeadDeveloperAgent('lead_developer', self)  # Master coordinator
            }
        except ImportError:
            # Fallback to basic agents if specialized variants not available
            logger.warning("Specialized agent variants not found, using basic agents")
            self.agents = {
                'research_specialist': MamaBearAgent('research_specialist', BasicResearchSpecialist(), self),
                'devops_specialist': MamaBearAgent('devops_specialist', BasicDevOpsSpecialist(), self),
                'scout_commander': MamaBearAgent('scout_commander', BasicScoutCommander(), self),
                'model_coordinator': MamaBearAgent('model_coordinator', BasicModelCoordinator(), self),
                'tool_curator': MamaBearAgent('tool_curator', BasicToolCurator(), self),
                'integration_architect': MamaBearAgent('integration_architect', BasicIntegrationArchitect(), self),
                'live_api_specialist': MamaBearAgent('live_api_specialist', BasicLiveAPISpecialist(), self),
                'lead_developer': LeadDeveloperAgent('lead_developer', self)
            }
    
    async def initialize_workflow_systems(self):
        """Initialize advanced workflow intelligence systems"""
        try:
            from .mama_bear_workflow_logic import WorkflowIntelligence, CollaborationOrchestrator
            
            self.workflow_intelligence = WorkflowIntelligence(
                self.model_manager, 
                self.memory
            )
            
            self.collaboration_orchestrator = CollaborationOrchestrator(
                self.model_manager,
                self.memory,
                self.workflow_intelligence
            )
            
            logger.info("✅ Advanced workflow intelligence initialized")
            
        except ImportError:
            logger.warning("⚠️ Advanced workflow intelligence not available, using basic routing")
    
    async def process_user_request(self, message: str, user_id: str, page_context: str = 'main_chat') -> Dict[str, Any]:
        """Enhanced request processing with intelligent agent routing"""
        
        # Update global context with user intent
        await self.context_awareness.update_global_context('user_intent', message)
        await self.context_awareness.update_global_context('user_id', user_id)
        await self.context_awareness.update_global_context('page_context', page_context)
        
        # Check if workflow intelligence is available
        if self.workflow_intelligence:
            return await self._process_with_workflow_intelligence(message, user_id, page_context)
        else:
            return await self._process_with_legacy_analysis(message, user_id, page_context)
    
    async def _process_with_workflow_intelligence(self, message: str, user_id: str, page_context: str) -> Dict[str, Any]:
        """Process request using advanced workflow intelligence"""
        
        try:
            # Get user patterns for intelligent routing
            user_patterns = await self.memory.get_user_patterns(user_id)
            
            # Use workflow intelligence to make decisions
            decision = await self.workflow_intelligence.make_decision(
                user_input=message,
                context={
                    'page_context': page_context,
                    'user_patterns': user_patterns,
                    'available_agents': list(self.agents.keys()),
                    'agent_performance': dict(self.agent_performance)
                }
            )
            
            # Save decision pattern for learning
            await self.memory.save_decision_pattern(user_id, {
                'workflow_type': decision.workflow_type,
                'selected_agents': decision.agent_assignments,
                'confidence_score': decision.confidence_score,
                'reasoning': decision.reasoning,
                'user_input': message,
                'page_context': page_context
            })
            
            # Execute based on decision
            if decision.workflow_type == 'single_agent':
                # Single agent execution
                primary_agent = decision.agent_assignments[0]
                agent = self.agents.get(primary_agent)
                if agent:
                    result = await agent.handle_request(message, user_id)
                    
                    # Track performance
                    await self._track_agent_performance(primary_agent, result.get('success', False))
                    
                    return result
                else:
                    return await self._fallback_response(message, user_id)
            
            elif decision.workflow_type in ['sequential', 'parallel', 'hierarchical']:
                # Multi-agent collaboration
                return await self._execute_collaborative_workflow(decision, message, user_id)
                
            else:
                # Unknown workflow type, use fallback
                return await self._fallback_response(message, user_id)
                
        except Exception as e:
            logger.error(f"Workflow intelligence error: {e}")
            return await self._process_with_legacy_analysis(message, user_id, page_context)
    
    async def _execute_collaborative_workflow(self, decision, message: str, user_id: str) -> Dict[str, Any]:
        """Execute collaborative workflow using collaboration orchestrator"""
        
        if not self.collaboration_orchestrator:
            return await self._fallback_response(message, user_id)
        
        try:
            # Use collaboration orchestrator
            result = await self.collaboration_orchestrator.execute_workflow(
                workflow_type=decision.workflow_type,
                agent_assignments=decision.agent_assignments,
                user_input=message,
                user_id=user_id,
                orchestrator=self
            )
            
            # Track collaborative performance
            for agent_id in decision.agent_assignments:
                await self._track_agent_performance(agent_id, result.get('success', False))
            
            return result
            
        except Exception as e:
            logger.error(f"Collaborative workflow error: {e}")
            return await self._fallback_response(message, user_id)
    
    async def _process_with_legacy_analysis(self, message: str, user_id: str, page_context: str) -> Dict[str, Any]:
        """Fallback processing using basic analysis"""
        
        # Analyze request to determine optimal agent strategy
        strategy = await self._analyze_request(message, page_context)
        
        if strategy['type'] == 'simple_response':
            # Single agent can handle this
            agent = self.agents[strategy['primary_agent']]
            result = await agent.handle_request(message, user_id)
            
            # Track performance
            await self._track_agent_performance(strategy['primary_agent'], result.get('success', False))
            
            return result
            
        elif strategy['type'] == 'collaborative':
            # Multiple agents need to collaborate
            return await self._orchestrate_collaboration(strategy, message, user_id)
            
        elif strategy['type'] == 'plan_and_execute':
            # Need planning phase followed by execution
            return await self._plan_and_execute(strategy, message, user_id)
    
    async def _analyze_request(self, message: str, page_context: str) -> Dict[str, Any]:
        """Analyze user request to determine optimal agent strategy"""
        
        # Use the research specialist to analyze the request
        analysis_prompt = f"""
        Analyze this user request and determine the optimal agent strategy:
        
        Request: "{message}"
        Context: {page_context}
        
        Classify as:
        1. simple_response - One agent can handle this (specify which agent)
        2. collaborative - Multiple agents need to work together (specify agents and roles)
        3. plan_and_execute - Needs planning phase then execution (specify planning steps)
        
        Consider:
        - Complexity of the request
        - Required capabilities (coding, research, deployment, etc.)
        - Time sensitivity
        - Resource requirements
        
        Return a JSON strategy object.
        """
        
        # Get analysis from model manager
        result = await self.model_manager.get_response(
            prompt=analysis_prompt,
            mama_bear_variant='research_specialist',
            required_capabilities=['chat', 'code']
        )
        
        if result['success']:
            try:
                # Parse the strategy from the response
                strategy = self._extract_strategy_from_response(result['response'])
                return strategy
            except:
                # Fallback to simple routing based on page context
                return self._fallback_strategy(page_context)
        else:
            return self._fallback_strategy(page_context)
    
    def _extract_strategy_from_response(self, response: str) -> Dict[str, Any]:
        """Extract strategy object from AI response"""
        # Try to find JSON in the response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Fallback: analyze keywords in response
        if 'simple' in response.lower():
            if 'research' in response.lower():
                return {'type': 'simple_response', 'primary_agent': 'research_specialist'}
            elif 'code' in response.lower():
                return {'type': 'simple_response', 'primary_agent': 'lead_developer'}
            elif 'deploy' in response.lower():
                return {'type': 'simple_response', 'primary_agent': 'devops_specialist'}
        
        # Default to lead developer
        return {'type': 'simple_response', 'primary_agent': 'lead_developer'}
    
    def _fallback_strategy(self, page_context: str) -> Dict[str, Any]:
        """Fallback strategy based on page context"""
        agent_mapping = {
            'main_chat': 'research_specialist',
            'vm_hub': 'devops_specialist',
            'scout': 'scout_commander',
            'multi_modal': 'model_coordinator',
            'mcp_hub': 'tool_curator',
            'integration': 'integration_architect',
            'live_api': 'live_api_specialist'
        }
        
        return {
            'type': 'simple_response',
            'primary_agent': agent_mapping.get(page_context, 'lead_developer')
        }
    
    async def _orchestrate_collaboration(self, strategy: Dict[str, Any], message: str, user_id: str) -> Dict[str, Any]:
        """Orchestrate collaboration between multiple agents"""
        
        collaboration_id = f"collab_{datetime.now().timestamp()}"
        self.collaboration_sessions[collaboration_id] = {
            'agents': strategy.get('agents', []),
            'roles': strategy.get('roles', {}),
            'status': 'active',
            'started_at': datetime.now(),
            'messages': []
        }
        
        # Create tasks for each agent
        tasks = []
        for i, (agent_id, role) in enumerate(strategy.get('roles', {}).items()):
            task = Task(
                id=f"{collaboration_id}_task_{i}",
                title=f"Collaborative task for {agent_id}",
                description=f"Role: {role}\nOriginal request: {message}",
                agent_type=agent_id,
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                context={'collaboration_id': collaboration_id, 'role': role}
            )
            tasks.append(task)
        
        # Execute tasks concurrently
        results = await asyncio.gather(
            *[self._execute_task(task) for task in tasks],
            return_exceptions=True
        )
        
        # Synthesize results
        return await self._synthesize_collaboration_results(collaboration_id, results, message)
    
    async def _plan_and_execute(self, strategy: Dict[str, Any], message: str, user_id: str) -> Dict[str, Any]:
        """Plan and execute complex multi-step requests"""
        
        # Phase 1: Planning
        planner_agent = self.agents.get('lead_developer')  # Lead developer acts as planner
        plan = await planner_agent.create_plan(message, user_id)
        
        # Present plan to user for approval (in real implementation, you'd wait for user input)
        # For now, we'll auto-approve simple plans
        
        # Phase 2: Execution
        if plan['status'] == 'approved':
            return await self._execute_plan(plan, user_id)
        else:
            return {
                'type': 'plan_proposal',
                'plan': plan,
                'message': "I've created a plan for your request. Would you like me to proceed?"
            }
    
    async def _execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a single task with the appropriate agent"""
        
        agent = self.agents.get(task.agent_type)
        if not agent:
            return {'success': False, 'error': f'Agent {task.agent_type} not found'}
        
        # Get context for the agent
        context = await self.context_awareness.get_agent_context(agent.id)
        context.current_task = task.id
        
        # Update task status
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        self.active_tasks[task.id] = task
        
        try:
            # Execute the task
            result = await agent.execute_task(task, context)
            
            # Update task status
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            self.completed_tasks[task.id] = task
            
            return result
            
        except Exception as e:
            # Handle task failure
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.current_attempt += 1
            
            # Retry if under limit
            if task.current_attempt < task.max_retries:
                logger.warning(f"Task {task.id} failed, retrying ({task.current_attempt}/{task.max_retries})")
                return await self._execute_task(task)
            else:
                logger.error(f"Task {task.id} failed permanently: {e}")
                return {'success': False, 'error': str(e)}
        
        finally:
            # Clean up
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
    
    async def _synthesize_collaboration_results(self, collaboration_id: str, results: List[Dict], original_message: str) -> Dict[str, Any]:
        """Combine results from multiple agents into a coherent response"""
        
        synthesis_prompt = f"""
        Combine these results from different Mama Bear specialists into a coherent response:
        
        Original request: "{original_message}"
        
        Results:
        {json.dumps(results, indent=2)}
        
        Create a unified response that:
        1. Addresses the original request completely
        2. Integrates insights from all specialists
        3. Provides clear next steps if applicable
        4. Maintains Mama Bear's caring, supportive tone
        
        Return a natural, conversational response.
        """
        
        # Use lead developer to synthesize
        result = await self.model_manager.get_response(
            prompt=synthesis_prompt,
            mama_bear_variant='main_chat',
            required_capabilities=['chat']
        )
        
        return {
            'type': 'collaborative_response',
            'content': result['response'] if result['success'] else "I've gathered information from my specialists and I'm ready to help!",
            'collaboration_id': collaboration_id,
            'participating_agents': [r.get('agent_id') for r in results if isinstance(r, dict)],
            'model_used': result.get('model_used'),
            'metadata': {
                'collaboration_results': results,
                'synthesis_successful': result['success']
            }
        }
    
    async def _track_agent_performance(self, agent_id: str, success: bool):
        """Track agent performance for optimization"""
        current = self.agent_performance[agent_id]
        
        # Update success rate with exponential moving average
        alpha = 0.1
        current['success_rate'] = (1 - alpha) * current['success_rate'] + alpha * (1.0 if success else 0.0)
        
        # Update timestamp
        current['last_update'] = datetime.now()
    
    async def _fallback_response(self, message: str, user_id: str) -> Dict[str, Any]:
        """Fallback response when routing fails"""
        
        # Use lead developer as fallback
        lead_developer = self.agents.get('lead_developer')
        if lead_developer:
            return await lead_developer.handle_request(message, user_id)
        else:
            return {
                'success': True,
                'content': "🐻 I'm here to help! Let me gather my thoughts and get back to you.",
                'agent_id': 'system',
                'metadata': {'fallback': True}
            }
    
    async def send_agent_message(self, from_agent: str, to_agent: str, message: str, context: Dict = None):
        """Enable agents to communicate with each other"""
        
        message_obj = {
            'from': from_agent,
            'to': to_agent,
            'message': message,
            'context': context or {},
            'timestamp': datetime.now()
        }
        
        self.agent_messages[to_agent].append(message_obj)
        
        # Notify receiving agent if it's currently active
        if to_agent in self.active_tasks:
            agent = self.agents[to_agent]
            await agent.handle_message(message_obj)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            agent_statuses[agent_id] = {
                'state': agent.state.value,
                'current_task': agent.current_task,
                'last_activity': agent.last_activity,
                'message_queue_size': len(self.agent_messages[agent_id]),
                'performance': self.agent_performance.get(agent_id, {})
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': agent_statuses,
            'active_tasks': len(self.active_tasks),
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'collaboration_sessions': len(self.collaboration_sessions),
            'model_manager_status': self.model_manager.get_model_status(),
            'global_context': list(self.context_awareness.global_context.keys()),
            'workflow_intelligence_available': self.workflow_intelligence is not None
        }
    
    async def _monitor_system_health(self):
        """Background system health monitoring"""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                # Monitor agent health
                for agent_id, agent in self.agents.items():
                    if agent.state == AgentState.ERROR:
                        logger.warning(f"Agent {agent_id} in error state, attempting recovery")
                        # Could implement agent recovery logic here
                
                # Monitor memory usage
                memory_cache_size = len(self.memory.memory_cache)
                if memory_cache_size > 1000:
                    logger.info(f"Memory cache has {memory_cache_size} entries, consolidation may be needed")
                
                # Monitor collaboration sessions
                active_sessions = len(self.collaboration_sessions)
                if active_sessions > 10:
                    logger.info(f"High number of active collaboration sessions: {active_sessions}")
                
            except Exception as e:
                logger.error(f"System health monitor error: {e}")

class MamaBearAgent:
    """Enhanced base class for all Mama Bear agents"""
    
    def __init__(self, agent_id: str, specialist_variant, orchestrator):
        self.id = agent_id
        self.variant = specialist_variant
        self.orchestrator = orchestrator
        self.state = AgentState.IDLE
        self.current_task = None
        self.last_activity = datetime.now()
        self.capabilities = []
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'average_response_time': 0.0
        }
    
    async def handle_request(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle a direct user request"""
        
        start_time = datetime.now()
        self.state = AgentState.THINKING
        self.last_activity = start_time
        self.performance_metrics['total_requests'] += 1
        
        try:
            # Get context
            context = await self.orchestrator.context_awareness.get_agent_context(self.id)
            
            # Get relevant memory context
            relevant_context = await self.orchestrator.memory.get_relevant_context(
                user_id=user_id,
                query=message,
                agent_id=self.id,
                limit=3
            )
            
            # Get system prompt from variant
            system_prompt = self.variant.get_system_prompt() if hasattr(self.variant, 'get_system_prompt') else f"You are {self.id}, a helpful AI assistant."
            
            # Build full prompt with context
            context_str = ""
            if relevant_context:
                context_str = "\n\nRelevant context from previous conversations:\n"
                for ctx in relevant_context:
                    context_str += f"- {ctx['content'].get('user_message', '')}: {ctx['content'].get('agent_response', '')}\n"
            
            full_prompt = f"""
            {system_prompt}
            
            Current context:
            - User: {user_id}
            - Agent capabilities: {context.available_tools}
            - Resource limits: {context.resource_limits}
            {context_str}
            
            User request: {message}
            
            Please respond as this Mama Bear specialist with your unique expertise and caring approach.
            """
            
            # Get response using model manager
            result = await self.orchestrator.model_manager.get_response(
                prompt=full_prompt,
                mama_bear_variant=self.id.split('_')[0],  # e.g., 'research' from 'research_specialist'
                required_capabilities=['chat']
            )
            
            self.state = AgentState.IDLE
            response_time = (datetime.now() - start_time).total_seconds()
            
            if result['success']:
                self.performance_metrics['successful_requests'] += 1
                
                # Update average response time
                total_requests = self.performance_metrics['total_requests']
                current_avg = self.performance_metrics['average_response_time']
                self.performance_metrics['average_response_time'] = (
                    (current_avg * (total_requests - 1) + response_time) / total_requests
                )
                
                # Save interaction to memory
                await self.orchestrator.memory.save_interaction(
                    user_id=user_id,
                    message=message,
                    response=result['response'],
                    metadata={
                        'agent_id': self.id,
                        'model_used': result['model_used'],
                        'response_time': response_time,
                        'success': True
                    }
                )
                
                return {
                    'success': True,
                    'content': result['response'],
                    'agent_id': self.id,
                    'model_used': result['model_used'],
                    'response_time': response_time,
                    'metadata': result.get('metadata', {})
                }
            else:
                return {
                    'success': False,
                    'content': "I'm having trouble accessing my models right now. Let me try a different approach! 🐻",
                    'error': result.get('error'),
                    'agent_id': self.id,
                    'response_time': response_time
                }
                
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Agent {self.id} error: {e}")
            return {
                'success': False,
                'content': "I encountered an error, but I'm working on fixing it! 🐻",
                'error': str(e),
                'agent_id': self.id
            }
    
    async def execute_task(self, task: Task, context: AgentContext) -> Dict[str, Any]:
        """Execute a specific task"""
        
        self.state = AgentState.WORKING
        self.current_task = task.id
        self.last_activity = datetime.now()
        
        # Task-specific logic would go here
        # For now, delegate to handle_request
        return await self.handle_request(task.description, context.user_intent)
    
    async def handle_message(self, message: Dict[str, Any]):
        """Handle messages from other agents"""
        
        # Process inter-agent communication
        logger.info(f"Agent {self.id} received message from {message['from']}: {message['message']}")
        
        # Could trigger collaborative actions here

class LeadDeveloperAgent(MamaBearAgent):
    """Special agent that coordinates other agents and handles complex planning"""
    
    def __init__(self, agent_id: str, orchestrator):
        super().__init__(agent_id, None, orchestrator)
        self.capabilities = ['planning', 'coordination', 'code_review', 'architecture']
    
    async def create_plan(self, request: str, user_id: str) -> Dict[str, Any]:
        """Create a detailed plan for complex requests"""
        
        planning_prompt = f"""
        As the Lead Developer Mama Bear, create a detailed plan for this request:
        
        Request: "{request}"
        User: {user_id}
        
        Break this down into:
        1. Requirements analysis
        2. Task decomposition
        3. Agent assignments
        4. Dependencies
        5. Estimated timeline
        6. Resource requirements
        
        Format as a structured plan that can be executed step by step.
        """
        
        result = await self.orchestrator.model_manager.get_response(
            prompt=planning_prompt,
            mama_bear_variant='main_chat',
            required_capabilities=['chat', 'code']
        )
        
        if result['success']:
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': result['response'],
                'status': 'pending_approval',
                'created_by': self.id,
                'user_id': user_id
            }
        else:
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': "I'll help you with this step by step!",
                'status': 'simple',
                'created_by': self.id,
                'user_id': user_id
            }

# Basic specialist classes as fallbacks
class BasicResearchSpecialist:
    def get_system_prompt(self):
        return "You are a research specialist focused on gathering and analyzing information."

class BasicDevOpsSpecialist:
    def get_system_prompt(self):
        return "You are a DevOps specialist focused on deployment and infrastructure."

class BasicScoutCommander:
    def get_system_prompt(self):
        return "You are a Scout commander specialized in web scraping and data gathering."

class BasicModelCoordinator:
    def get_system_prompt(self):
        return "You are a model coordinator focused on AI model management and selection."

class BasicToolCurator:
    def get_system_prompt(self):
        return "You are a tool curator specialized in integrating and managing development tools."

class BasicIntegrationArchitect:
    def get_system_prompt(self):
        return "You are an integration architect focused on system design and API integration."

class BasicLiveAPISpecialist:
    def get_system_prompt(self):
        return "You are a live API specialist focused on real-time data and webhook integrations."

# Integration function for existing Flask app
async def initialize_enhanced_orchestration(app, memory_manager, model_manager, scrapybara_client):
    """Initialize the enhanced orchestration system and attach to Flask app"""
    
    orchestrator = EnhancedAgentOrchestrator(memory_manager, model_manager, scrapybara_client)
    
    # Initialize workflow systems
    await orchestrator.initialize_workflow_systems()
    
    app.mama_bear_orchestrator = orchestrator
    
    # Start background tasks
    asyncio.create_task(orchestrator._monitor_system_health())
    
    logger.info("🐻 Enhanced Mama Bear Orchestration System initialized successfully!")
    return orchestrator