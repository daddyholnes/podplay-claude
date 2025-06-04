# backend/services/mama_bear_orchestration.py
"""
🐻 Mama Bear Agent Orchestration System
Core logic for agent collaboration, context awareness, and workflow management
"""
import logging
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
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
    project_context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict]] = None
    available_tools: Optional[List[str]] = None
    resource_limits: Optional[Dict[str, Any]] = None
    collaboration_state: Optional[Dict[str, Any]] = None
    
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
    dependencies: Optional[List[str]] = None
    estimated_duration: int = 300  # seconds
    max_retries: int = 3
    current_attempt: int = 0
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.context is None:
            self.context = {}

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
        
        # Persist important context to memory if save_context method exists
        if hasattr(self.memory, 'save_context'):
            try:
                await self.memory.save_context(key, value)
            except Exception as e:
                logger.warning(f"Could not save context to memory: {e}")
    
    async def get_agent_context(self, agent_id: str) -> AgentContext:
        """Get complete context for a specific agent"""
        if agent_id not in self.agent_contexts:
            self.agent_contexts[agent_id] = AgentContext(agent_id=agent_id)
        
        context = self.agent_contexts[agent_id]
        
        # Enrich context with relevant global information
        context.user_intent = self.global_context.get('user_intent', {}).get('value', '')
        context.project_context = self.global_context.get('project_state', {}).get('value', {})
        
        # Get recent conversation history from memory
        try:
            if hasattr(self.memory, 'get_recent_conversations'):
                context.conversation_history = await self.memory.get_recent_conversations(
                    agent_id=agent_id, 
                    limit=10
                )
            else:
                # Fallback for existing memory manager
                context.conversation_history = []
        except Exception as e:
            logger.warning(f"Could not get conversation history: {e}")
            context.conversation_history = []
        
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
            'research': ['scrapybara', 'web_search', 'document_analysis'],
            'devops': ['vm_management', 'deployment', 'monitoring'],
            'integration': ['api_testing', 'auth_setup', 'workflows']
        }
        
        return tool_mapping.get(agent_type, [])
    
    async def _get_resource_limits(self, agent_id: str) -> Dict[str, Any]:
        """Get resource limits for this agent"""
        # Check current quota status from model manager if available
        try:
            if hasattr(self.model_manager, 'get_model_status'):
                model_status = self.model_manager.get_model_status()
                api_quota = sum(
                    model.get('quota_limit', 100) - model.get('quota_used', 0) 
                    for model in model_status.get('models', [])
                )
            else:
                api_quota = 1000  # Default fallback
        except:
            api_quota = 1000
        
        return {
            'api_quota_remaining': api_quota,
            'scrapybara_instances': 5,  # Max concurrent instances
            'memory_limit_mb': 1024,
            'execution_timeout': 3600  # 1 hour max execution
        }

class AgentOrchestrator:
    """Orchestrates collaboration between different Mama Bear agents"""
    
    def __init__(self, memory_manager, model_manager, scrapybara_client=None, enhanced_memory=None, workflow_intelligence=None, mem0_client=None):
        self.memory = memory_manager
        self.model_manager = model_manager
        self.scrapybara = scrapybara_client
        self.enhanced_memory = enhanced_memory
        self.workflow_intelligence = workflow_intelligence
        self.mem0_client = mem0_client
        self.context_awareness = ContextAwareness(memory_manager, model_manager)
        
        # Agent registry
        self.agents = {}
        self.active_tasks = {}
        self.task_queue = deque()
        self.completed_tasks = {}
        
        # Communication channels
        self.agent_messages = defaultdict(deque)
        self.collaboration_sessions = {}
        
        # Initialize specialized agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all Mama Bear agent types"""
        
        # Create simplified agent instances for now
        self.agents = {
            'research_specialist': MamaBearAgent('research_specialist', None, self),
            'devops_specialist': MamaBearAgent('devops_specialist', None, self),
            'scout_commander': MamaBearAgent('scout_commander', None, self),
            'model_coordinator': MamaBearAgent('model_coordinator', None, self),
            'tool_curator': MamaBearAgent('tool_curator', None, self),
            'integration_architect': MamaBearAgent('integration_architect', None, self),
            'live_api_specialist': MamaBearAgent('live_api_specialist', None, self),
            'lead_developer': LeadDeveloperAgent('lead_developer', self)
        }
    
    async def process_user_request(self, message: str, user_id: str, page_context: str = 'main_chat') -> Dict[str, Any]:
        """Main entry point for user requests - determines which agents to involve"""
        
        # Update global context with user intent
        await self.context_awareness.update_global_context('user_intent', message)
        await self.context_awareness.update_global_context('user_id', user_id)
        await self.context_awareness.update_global_context('page_context', page_context)
        
        # Analyze request to determine optimal agent strategy
        strategy = await self._analyze_request(message, page_context)
        
        if strategy['type'] == 'simple_response':
            # Single agent can handle this
            agent = self.agents[strategy['primary_agent']]
            return await agent.handle_request(message, user_id)
            
        elif strategy['type'] == 'collaborative':
            # Multiple agents need to collaborate
            return await self._orchestrate_collaboration(strategy, message, user_id)
            
        elif strategy['type'] == 'plan_and_execute':
            # Need planning phase followed by execution
            return await self._plan_and_execute(strategy, message, user_id)
        else:
            # Fallback for unknown strategy types
            agent = self.agents.get('lead_developer', list(self.agents.values())[0])
            return await agent.handle_request(message, user_id)
    
    async def _analyze_request(self, message: str, page_context: str) -> Dict[str, Any]:
        """Analyze user request to determine optimal agent strategy"""
        
        # Simple rule-based analysis for now - can be enhanced with AI later
        strategy = self._fallback_strategy(page_context, message)
        
        # Try AI analysis if model manager supports it
        try:
            if hasattr(self.model_manager, 'get_response'):
                analysis_prompt = f"""
                Analyze this user request and determine the optimal agent strategy:
                
                Request: "{message}"
                Context: {page_context}
                
                Classify as:
                1. simple_response - One agent can handle this (specify which agent)
                2. collaborative - Multiple agents need to work together
                3. plan_and_execute - Needs planning phase then execution
                
                Consider complexity and required capabilities.
                Return a JSON strategy object.
                """
                
                result = await self.model_manager.get_response(
                    prompt=analysis_prompt,
                    mama_bear_variant='research_specialist',
                    required_capabilities=['chat']
                )
                
                if result.get('success'):
                    # Try to extract strategy from response
                    extracted_strategy = self._extract_strategy_from_response(result['response'])
                    if extracted_strategy:
                        return extracted_strategy
        except Exception as e:
            logger.warning(f"AI analysis failed, using fallback: {e}")
        
        return strategy
    
    def _extract_strategy_from_response(self, response: str) -> Dict[str, Any]:
        """Extract strategy object from AI response"""
        # Try to find JSON in the response
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
        return {
            'type': 'simple_response',
            'primary_agent': 'research_specialist'
        }
    
    def _fallback_strategy(self, page_context: str, message: str = "") -> Dict[str, Any]:
        """Fallback strategy based on page context and message content"""
        
        # Page context mapping
        agent_mapping = {
            'main_chat': 'research_specialist',
            'vm_hub': 'devops_specialist',
            'scout': 'scout_commander',
            'multi_modal': 'model_coordinator',
            'mcp_hub': 'tool_curator',
            'integration': 'integration_architect',
            'live_api': 'live_api_specialist'
        }
        
        # Message content analysis
        message_lower = message.lower()
        if 'deploy' in message_lower or 'production' in message_lower:
            primary_agent = 'devops_specialist'
        elif 'code' in message_lower or 'function' in message_lower:
            primary_agent = 'lead_developer'
        elif 'research' in message_lower or 'find' in message_lower:
            primary_agent = 'research_specialist'
        elif 'api' in message_lower or 'integrate' in message_lower:
            primary_agent = 'integration_architect'
        else:
            primary_agent = agent_mapping.get(page_context, 'lead_developer')
        
        return {
            'type': 'simple_response',
            'primary_agent': primary_agent
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
        
        # For now, delegate to primary agent with collaboration context
        primary_agent = strategy.get('primary_agent', 'lead_developer')
        agent = self.agents.get(primary_agent, self.agents['lead_developer'])
        
        result = await agent.handle_request(message, user_id)
        result['collaboration_id'] = collaboration_id
        result['type'] = 'collaborative_response'
        
        return result
    
    async def _plan_and_execute(self, strategy: Dict[str, Any], message: str, user_id: str) -> Dict[str, Any]:
        """Plan and execute complex multi-step requests"""
        
        # Phase 1: Planning with lead developer
        lead_developer = self.agents.get('lead_developer')
        if lead_developer and hasattr(lead_developer, 'create_plan'):
            plan = await lead_developer.create_plan(message, user_id)
        else:
            # Fallback plan creation
            plan = {
                'title': f"Plan for: {message}",
                'steps': [
                    'Analyze requirements',
                    'Break into tasks', 
                    'Assign to specialists',
                    'Execute step by step'
                ],
                'estimated_time': '30 minutes',
                'agents_needed': ['lead_developer']
            }
        
        # For now, return the plan for user review
        return {
            'type': 'plan_proposal',
            'plan': plan,
            'message': "I've created a plan for your request. Would you like me to proceed?",
            'timestamp': datetime.now().isoformat()
        }
    
    async def send_agent_message(self, from_agent: str, to_agent: str, message: str, context: Optional[Dict] = None):
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
                'last_activity': agent.last_activity.isoformat() if agent.last_activity else None,
                'message_queue_size': len(self.agent_messages[agent_id])
            }
        
        # Get model status if available
        model_status = {}
        try:
            if hasattr(self.model_manager, 'get_model_status'):
                model_status = self.model_manager.get_model_status()
        except:
            model_status = {'status': 'unknown'}
        
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': agent_statuses,
            'active_tasks': len(self.active_tasks),
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'model_manager_status': model_status,
            'global_context': list(self.context_awareness.global_context.keys())
        }

class MamaBearAgent:
    """Base class for all Mama Bear agents"""
    
    def __init__(self, agent_id: str, specialist_variant, orchestrator):
        self.id = agent_id
        self.variant = specialist_variant
        self.orchestrator = orchestrator
        self.state = AgentState.IDLE
        self.current_task = None
        self.last_activity = datetime.now()
        self.capabilities = []
    
    async def handle_request(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle a direct user request"""
        
        self.state = AgentState.THINKING
        self.last_activity = datetime.now()
        
        try:
            # Get context
            context = await self.orchestrator.context_awareness.get_agent_context(self.id)
            
            # Build specialized prompt based on agent type
            system_prompt = self._get_agent_system_prompt()
            
            # Build full prompt
            full_prompt = f"""
            {system_prompt}
            
            Current context:
            - User: {user_id}
            - Available tools: {context.available_tools}
            - Page context: {context.project_context}
            
            User request: {message}
            
            Please respond as this Mama Bear specialist with care and expertise.
            """
            
            # Get response using model manager
            if hasattr(self.orchestrator.model_manager, 'get_response'):
                result = await self.orchestrator.model_manager.get_response(
                    prompt=full_prompt,
                    mama_bear_variant=self._get_variant_name(),
                    required_capabilities=['chat']
                )
            else:
                # Fallback for basic model manager
                result = {
                    'success': True,
                    'response': f"🐻 I'm {self.id} and I'm here to help with: {message}",
                    'model_used': 'fallback'
                }
            
            self.state = AgentState.IDLE
            
            if result.get('success'):
                # Save interaction to memory if possible
                try:
                    if hasattr(self.orchestrator.memory, 'save_interaction'):
                        await self.orchestrator.memory.save_interaction(
                            user_id=user_id,
                            message=message,
                            response=result['response'],
                            metadata={
                                'agent_id': self.id,
                                'model_used': result.get('model_used', 'unknown')
                            }
                        )
                except Exception as e:
                    logger.warning(f"Could not save interaction to memory: {e}")
                
                return {
                    'success': True,
                    'message': result['response'],
                    'agent': self.id,
                    'timestamp': datetime.now().isoformat(),
                    'model_used': result.get('model_used', 'unknown')
                }
            else:
                return {
                    'success': False,
                    'message': f"I encountered an issue: {result.get('error', 'Unknown error')}",
                    'agent': self.id,
                    'timestamp': datetime.now().isoformat(),
                    'error': result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Error in agent {self.id}: {e}")
            return {
                'success': False,
                'message': f"I'm experiencing technical difficulties. Please try again.",
                'agent': self.id,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _get_agent_system_prompt(self) -> str:
        """Get system prompt based on agent type"""
        prompts = {
            'research_specialist': """
            You are the Research Specialist Mama Bear 🐻 - a caring, intelligent agent focused on:
            - Deep research and information gathering
            - Web scraping with Scrapybara
            - Document analysis and synthesis
            - Finding relevant resources and solutions
            
            You approach every task with empathy and understanding, especially for neurodivergent users.
            You provide thorough, well-researched responses with clear explanations.
            """,
            'devops_specialist': """
            You are the DevOps Specialist Mama Bear 🐻 - a nurturing yet technically skilled agent focused on:
            - Infrastructure management and deployment
            - VM creation and configuration
            - Production environment setup
            - Monitoring and maintenance
            
            You ensure all deployments are safe, reliable, and user-friendly.
            You explain technical concepts in accessible ways.
            """,
            'scout_commander': """
            You are the Scout Commander Mama Bear 🐻 - an organized, proactive agent focused on:
            - Coordinating reconnaissance missions
            - Managing Scrapybara instances
            - Information gathering strategies
            - Team coordination and planning
            
            You lead with wisdom and care, ensuring all team members feel supported.
            """,
            'model_coordinator': """
            You are the Model Coordinator Mama Bear 🐻 - a knowledgeable, adaptive agent focused on:
            - AI model selection and optimization
            - Multi-modal integrations
            - Performance monitoring
            - Resource allocation
            
            You help users navigate complex AI landscapes with patience and expertise.
            """,
            'tool_curator': """
            You are the Tool Curator Mama Bear 🐻 - an organized, helpful agent focused on:
            - MCP tool discovery and integration
            - Tool compatibility analysis
            - Workflow optimization
            - Resource management
            
            You help users find and use the perfect tools for their needs.
            """,
            'integration_architect': """
            You are the Integration Architect Mama Bear 🐻 - a systematic, detail-oriented agent focused on:
            - System integrations and workflows
            - API design and implementation
            - Architecture planning
            - Technical documentation
            
            You design robust, scalable solutions that work harmoniously together.
            """,
            'live_api_specialist': """
            You are the Live API Specialist Mama Bear 🐻 - a responsive, real-time focused agent specialized in:
            - Live API integrations
            - Real-time data processing
            - WebSocket communications
            - Interactive features
            
            You create dynamic, responsive experiences that delight users.
            """,
            'lead_developer': """
            You are the Lead Developer Mama Bear 🐻 - a wise, experienced agent who:
            - Oversees technical architecture and planning
            - Coordinates between different specialists
            - Makes high-level technical decisions
            - Mentors and guides the development process
            
            You lead with both technical excellence and emotional intelligence.
            """
        }
        
        return prompts.get(self.id, prompts['research_specialist'])
    
    def _get_variant_name(self) -> str:
        """Get the mama bear variant name for model selection"""
        variant_mapping = {
            'research_specialist': 'research_specialist',
            'devops_specialist': 'devops_specialist', 
            'scout_commander': 'scout_commander',
            'model_coordinator': 'model_coordinator',
            'tool_curator': 'tool_curator',
            'integration_architect': 'integration_architect',
            'live_api_specialist': 'live_api_specialist',
            'lead_developer': 'lead_developer'
        }
        
        return variant_mapping.get(self.id, 'research_specialist')
    
    async def handle_message(self, message_obj: Dict[str, Any]):
        """Handle inter-agent communication"""
        self.last_activity = datetime.now()
        logger.info(f"Agent {self.id} received message from {message_obj['from']}: {message_obj['message']}")
        
        # For now, just log the message. In the future, this could trigger
        # more sophisticated inter-agent collaboration workflows
        return True

class LeadDeveloperAgent(MamaBearAgent):
    """Specialized Lead Developer with planning capabilities"""
    
    def __init__(self, agent_id: str, orchestrator):
        super().__init__(agent_id, 'lead_developer', orchestrator)
        self.capabilities = ['planning', 'architecture', 'coordination', 'code_review']
    
    async def create_plan(self, request: str, user_id: str) -> Dict[str, Any]:
        """Create a detailed plan for complex requests"""
        
        # Analyze the request to determine planning approach
        planning_prompt = f"""
        As the Lead Developer Mama Bear, create a detailed plan for this request:
        
        Request: {request}
        User: {user_id}
        
        Break this down into specific, actionable steps with clear deliverables.
        Consider dependencies, resource requirements, and potential challenges.
        
        Provide a structured plan with timeline estimates.
        """
        
        try:
            if hasattr(self.orchestrator.model_manager, 'get_response'):
                result = await self.orchestrator.model_manager.get_response(
                    prompt=planning_prompt,
                    mama_bear_variant='lead_developer',
                    required_capabilities=['planning', 'chat']
                )
                
                if result.get('success'):
                    # Extract structured plan from response
                    return self._parse_plan_response(result['response'], request)
        except Exception as e:
            logger.warning(f"AI planning failed, using fallback: {e}")
        
        # Fallback plan creation
        return {
            'title': f"Plan for: {request}",
            'description': "I'll help you accomplish this step by step with care and expertise.",
            'steps': [
                'Understand requirements thoroughly',
                'Design the solution approach', 
                'Implement incrementally',
                'Test and validate',
                'Deploy and monitor'
            ],
            'estimated_time': '1-2 hours',
            'created_by': self.id,
            'created_at': datetime.now().isoformat(),
            'status': 'draft'
        }
    
    def _parse_plan_response(self, response: str, original_request: str) -> Dict[str, Any]:
        """Parse AI response into structured plan"""
        
        # Try to extract structured information from the response
        lines = response.split('\n')
        steps = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('*') or line.startswith('1.')):
                # Clean up the step text
                step = line.lstrip('-*0123456789. ')
                if step:
                    steps.append(step)
        
        if not steps:
            # Fallback if no steps found
            steps = [
                'Analyze the requirements in detail',
                'Design the technical approach',
                'Implement the solution incrementally', 
                'Test thoroughly',
                'Deploy and document'
            ]
        
        return {
            'title': f"Development Plan: {original_request[:50]}...",
            'description': response[:200] + "..." if len(response) > 200 else response,
            'steps': steps,
            'estimated_time': self._estimate_time_from_steps(steps),
            'created_by': self.id,
            'created_at': datetime.now().isoformat(),
            'status': 'ready',
            'ai_generated': True
        }
    
    def _estimate_time_from_steps(self, steps: List[str]) -> str:
        """Estimate time based on number of steps"""
        step_count = len(steps)
        
        if step_count <= 3:
            return "30 minutes - 1 hour"
        elif step_count <= 5:
            return "1-2 hours"
        elif step_count <= 8:
            return "2-4 hours"
        else:
            return "4+ hours"
