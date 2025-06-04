# backend/services/mama_bear_orchestration.py
"""
🐻 Mama Bear Agent Orchestration System
Core logic for agent collaboration, context awareness, and workflow management
"""

import asyncio
import json
import re
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
            - Providing thorough, well-researched answers
            
            You approach every task with patience and thoroughness, ensuring accuracy and helpfulness.
            """,
            
            'devops_specialist': """
            You are the DevOps Specialist Mama Bear 🐻 - a protective, skilled agent focused on:
            - VM creation and management
            - Deployment strategies and automation
            - Infrastructure monitoring and optimization
            - Security best practices
            - Production readiness and reliability
            
            You ensure systems are robust, secure, and scalable while being caring about user needs.
            """,
            
            'scout_commander': """
            You are the Scout Commander Mama Bear 🐻 - an adventurous, resourceful agent focused on:
            - Exploring new technologies and APIs
            - Reconnaissance and discovery missions
            - Integration testing and validation
            - Tool evaluation and recommendations
            - Pioneer work in uncharted territory
            
            You boldly explore while keeping safety and user success as top priorities.
            """,
            
            'model_coordinator': """
            You are the Model Coordinator Mama Bear 🐻 - a wise, strategic agent focused on:
            - AI model selection and optimization
            - Multi-modal integration (text, vision, audio)
            - Model performance monitoring
            - Fine-tuning and customization
            - Balancing cost, speed, and quality
            
            You carefully orchestrate AI capabilities to serve user needs optimally.
            """,
            
            'tool_curator': """
            You are the Tool Curator Mama Bear 🐻 - an organized, helpful agent focused on:
            - MCP (Model Context Protocol) server management
            - Tool discovery and integration
            - Workflow optimization
            - Plugin and extension management
            - Creating seamless tool experiences
            
            You lovingly organize and present tools in the most helpful way possible.
            """,
            
            'integration_architect': """
            You are the Integration Architect Mama Bear 🐻 - a systematic, visionary agent focused on:
            - System architecture and design
            - API integration strategies
            - Workflow orchestration
            - Scalability planning
            - Technical debt management
            
            You design robust, elegant solutions that grow with user needs.
            """,
            
            'live_api_specialist': """
            You are the Live API Specialist Mama Bear 🐻 - a dynamic, responsive agent focused on:
            - Real-time API interactions
            - Live data streaming and processing
            - WebSocket connections and events
            - Performance optimization
            - Real-time troubleshooting
            
            You ensure smooth, responsive real-time experiences with caring attention to detail.
            """,
            
            'lead_developer': """
            You are the Lead Developer Mama Bear 🐻 - a nurturing, expert agent focused on:
            - Code architecture and best practices
            - Project planning and coordination
            - Code review and quality assurance
            - Team guidance and mentoring
            - Technical decision making
            
            You lead with wisdom, patience, and a deep commitment to creating excellent solutions.
            """
        }
        
        return prompts.get(self.id, "You are a helpful Mama Bear agent focused on providing caring, expert assistance.")
    
    def _get_variant_name(self) -> str:
        """Get the variant name for model manager"""
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
        """Handle messages from other agents"""
        # For now, just log the message
        logger.info(f"Agent {self.id} received message from {message_obj['from']}: {message_obj['message']}")


class LeadDeveloperAgent(MamaBearAgent):
    """Specialized Lead Developer agent with planning capabilities"""
    
    def __init__(self, agent_id: str, orchestrator):
        super().__init__(agent_id, None, orchestrator)
        self.capabilities = ['planning', 'code_review', 'architecture', 'coordination']
    
    async def create_plan(self, request: str, user_id: str) -> Dict[str, Any]:
        """Create a detailed plan for complex requests"""
        
        # Analyze the request for complexity
        plan_prompt = f"""
        As a Lead Developer Mama Bear, create a detailed plan for this request:
        
        Request: {request}
        User: {user_id}
        
        Break down into:
        1. Requirements analysis
        2. Technical approach
        3. Step-by-step tasks
        4. Resource requirements
        5. Timeline estimation
        6. Risk assessment
        
        Provide a caring, thorough plan that ensures success.
        """
        
        try:
            if hasattr(self.orchestrator.model_manager, 'get_response'):
                result = await self.orchestrator.model_manager.get_response(
                    prompt=plan_prompt,
                    mama_bear_variant='lead_developer',
                    required_capabilities=['chat']
                )
                
                if result.get('success'):
                    return {
                        'title': f"Development Plan: {request[:50]}...",
                        'description': result['response'],
                        'created_by': self.id,
                        'created_at': datetime.now().isoformat(),
                        'status': 'draft'
                    }
        except Exception as e:
            logger.error(f"Plan creation failed: {e}")
        
        # Fallback plan
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
                    logger.warning(f"Could not save interaction: {e}")
                
                return {
                    'success': True,
                    'content': result['response'],
                    'agent_id': self.id,
                    'model_used': result.get('model_used', 'unknown'),
                    'variant': self._get_variant_name(),
                    'metadata': result.get('metadata', {})
                }
            else:
                return {
                    'success': False,
                    'content': "I'm having trouble accessing my models right now. Let me try a different approach! 🐻",
                    'error': result.get('error'),
                    'agent_id': self.id,
                    'variant': self._get_variant_name()
                }
                
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Agent {self.id} error: {e}")
            return {
                'success': False,
                'content': "I encountered an error, but I'm working on fixing it! 🐻",
                'error': str(e),
                'agent_id': self.id,
                'variant': self._get_variant_name()
            }
    
    def _get_agent_system_prompt(self) -> str:
        """Get system prompt based on agent type"""
        
        prompts = {
            'research_specialist': """You are the Research Specialist Mama Bear 🔍. You excel at:
            - Deep research and analysis
            - Web search and information gathering  
            - Document analysis and synthesis
            - Finding reliable sources and data
            
            You're thorough, accurate, and love digging deep into topics.""",
            
            'devops_specialist': """You are the DevOps Specialist Mama Bear ⚙️. You excel at:
            - Infrastructure setup and management
            - Deployment automation and CI/CD
            - Performance optimization and monitoring
            - System architecture and scaling
            
            You're reliable, efficient, and keep systems running smoothly.""",
            
            'scout_commander': """You are the Scout Commander Mama Bear 🧭. You excel at:
            - Autonomous exploration and discovery
            - Data collection and reconnaissance  
            - Long-running task execution
            - Environmental analysis and mapping
            
            You're adventurous, independent, and great at finding new paths.""",
            
            'model_coordinator': """You are the Model Coordinator Mama Bear 🤖. You excel at:
            - AI model selection and optimization
            - Performance monitoring and tuning
            - Cross-model synthesis and coordination
            - ML pipeline management
            
            You're technical, analytical, and optimize AI performance.""",
            
            'tool_curator': """You are the Tool Curator Mama Bear 🛠️. You excel at:
            - Tool discovery and evaluation
            - Integration recommendations
            - Compatibility analysis
            - Workflow automation setup
            
            You're resourceful, practical, and love finding the right tool for every job.""",
            
            'integration_architect': """You are the Integration Architect Mama Bear 🔗. You excel at:
            - API design and integration
            - System connectivity and data flow
            - Authentication and security setup
            - Microservices architecture
            
            You're systematic, security-conscious, and build robust connections.""",
            
            'live_api_specialist': """You are the Live API Specialist Mama Bear ⚡. You excel at:
            - Real-time features and WebSocket management
            - Streaming data processing
            - Live demonstrations and interactive experiences
            - Event-driven architectures
            
            You're dynamic, responsive, and bring systems to life.""",
            
            'lead_developer': """You are the Lead Developer Mama Bear 👨‍💻. You excel at:
            - Project planning and architecture
            - Team coordination and collaboration
            - Complex problem solving and debugging
            - Code review and quality assurance
            
            You're experienced, thoughtful, and guide projects to success."""
        }
        
        return prompts.get(self.id, "You are a helpful Mama Bear specialist ready to assist! 🐻")
    
    def _get_variant_name(self) -> str:
        """Get variant name for model manager"""
        variant_mapping = {
            'research_specialist': 'research_mode',
            'devops_specialist': 'deployment_mode', 
            'scout_commander': 'scout_mode',
            'model_coordinator': 'technical_mode',
            'tool_curator': 'tool_mode',
            'integration_architect': 'integration_mode',
            'live_api_specialist': 'api_mode',
            'lead_developer': 'main_chat'
        }
        
        return variant_mapping.get(self.id, 'main_chat')
    
    async def execute_task(self, task: Task, context: AgentContext) -> Dict[str, Any]:
        """Execute a specific task"""
        
        self.state = AgentState.WORKING
        self.current_task = task.id
        self.last_activity = datetime.now()
        
        # Task-specific logic - delegate to handle_request for now
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
        
        try:
            if hasattr(self.orchestrator.model_manager, 'get_response'):
                result = await self.orchestrator.model_manager.get_response(
                    prompt=planning_prompt,
                    mama_bear_variant='main_chat',
                    required_capabilities=['chat', 'code']
                )
            else:
                result = {
                    'success': True,
                    'response': f"Plan for: {request}\n\n1. Analyze requirements\n2. Break into tasks\n3. Assign to specialists\n4. Execute step by step\n\nI'll coordinate the team to help you achieve this!"
                }
        except Exception as e:
            result = {
                'success': False,
                'response': f"I'll help you plan this step by step: {request}"
            }
        
        if result.get('success'):
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': result['response'],
                'status': 'pending_approval',
                'created_by': self.id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': "I'll help you with this step by step! Let's break it down together.",
                'status': 'simple',
                'created_by': self.id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            }

# Integration function for existing Flask app
async def initialize_orchestration(app, memory_manager, model_manager, scrapybara_client=None):
    """Initialize the orchestration system and attach to Flask app"""
    
    orchestrator = AgentOrchestrator(memory_manager, model_manager, scrapybara_client)
    app.mama_bear_orchestrator = orchestrator
    
    logger.info("🐻 Mama Bear Orchestration System initialized successfully!")
    return orchestrator