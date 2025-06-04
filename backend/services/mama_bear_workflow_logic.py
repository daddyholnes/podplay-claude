# backend/services/mama_bear_workflow_logic.py
"""
🐻 Mama Bear Workflow Logic & Decision Engine
Defines how agents make decisions, collaborate, and execute complex workflows
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from enum import Enum
from dataclasses import dataclass, field
import logging
import re

logger = logging.getLogger(__name__)

class WorkflowType(Enum):
    SIMPLE_QUERY = "simple_query"
    RESEARCH_TASK = "research_task"
    CODE_GENERATION = "code_generation"
    DEPLOYMENT_TASK = "deployment_task"
    COMPLEX_PROJECT = "complex_project"
    TROUBLESHOOTING = "troubleshooting"
    LEARNING_SESSION = "learning_session"

class DecisionConfidence(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CERTAIN = "certain"

@dataclass
class WorkflowDecision:
    """Represents a decision made by the workflow engine"""
    decision_type: str
    confidence: DecisionConfidence
    reasoning: str
    selected_agents: List[str]
    estimated_complexity: int  # 1-10 scale
    estimated_duration: int  # minutes
    resource_requirements: Dict[str, Any]
    fallback_options: List[str] = field(default_factory=list)

@dataclass
class ContextualKnowledge:
    """What the system knows about the current context"""
    user_expertise_level: str = "intermediate"  # beginner, intermediate, expert
    project_type: Optional[str] = None
    current_focus: Optional[str] = None
    recent_patterns: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    success_history: Dict[str, float] = field(default_factory=dict)

class WorkflowIntelligence:
    """Core intelligence for workflow decisions and agent coordination"""
    
    def __init__(self, model_manager, memory_manager):
        self.model_manager = model_manager
        self.memory = memory_manager
        
        # Decision patterns learned over time
        self.decision_patterns = {}
        self.agent_performance_history = {}
        self.workflow_templates = self._initialize_workflow_templates()
        
        # Load historical knowledge
        asyncio.create_task(self._load_historical_patterns())
    
    def _initialize_workflow_templates(self) -> Dict[str, Dict]:
        """Initialize predefined workflow templates"""
        return {
            "simple_query": {
                "agent_sequence": ["research_specialist"],
                "max_duration": 5,
                "confidence_threshold": 0.7,
                "escalation_path": ["lead_developer"]
            },
            
            "research_deep_dive": {
                "agent_sequence": ["scout_commander", "research_specialist"],
                "collaboration_type": "sequential",
                "max_duration": 30,
                "tools_required": ["scrapybara", "web_search", "document_analysis"],
                "escalation_path": ["lead_developer"]
            },
            
            "code_feature_request": {
                "agent_sequence": ["lead_developer", "research_specialist", "devops_specialist"],
                "collaboration_type": "collaborative",
                "phases": ["analysis", "design", "implementation", "testing"],
                "max_duration": 120,
                "quality_gates": ["code_review", "testing", "documentation"]
            },
            
            "deployment_automation": {
                "agent_sequence": ["devops_specialist", "integration_architect"],
                "collaboration_type": "collaborative", 
                "tools_required": ["scrapybara", "deployment_tools"],
                "max_duration": 60,
                "safety_checks": ["backup", "rollback_plan", "monitoring"]
            },
            
            "learning_and_exploration": {
                "agent_sequence": ["scout_commander", "tool_curator", "research_specialist"],
                "collaboration_type": "exploratory",
                "max_duration": 45,
                "success_metrics": ["knowledge_gained", "tools_discovered", "patterns_identified"]
            },
            
            "troubleshooting_session": {
                "agent_sequence": ["devops_specialist", "model_coordinator", "lead_developer"],
                "collaboration_type": "diagnostic",
                "max_duration": 30,
                "escalation_triggers": ["error_persistence", "resource_exhaustion", "timeout"]
            }
        }
    
    async def analyze_request_intent(self, message: str, context: Dict[str, Any]) -> WorkflowDecision:
        """
        🧠 Core decision engine - analyzes user intent and determines optimal workflow
        """
        
        # Extract features from the message
        features = self._extract_message_features(message)
        
        # Get contextual knowledge about the user and situation
        contextual_knowledge = await self._build_contextual_knowledge(context)
        
        # Determine workflow type using AI analysis
        workflow_type = await self._classify_workflow_type(message, features, contextual_knowledge)
        
        # Select optimal agents for this workflow
        agent_decision = await self._select_optimal_agents(workflow_type, features, contextual_knowledge)
        
        # Estimate complexity and resources
        complexity_estimate = self._estimate_complexity(features, workflow_type)
        
        # Create the decision
        decision = WorkflowDecision(
            decision_type=workflow_type.value,
            confidence=agent_decision['confidence'],
            reasoning=agent_decision['reasoning'],
            selected_agents=agent_decision['agents'],
            estimated_complexity=complexity_estimate['complexity'],
            estimated_duration=complexity_estimate['duration'],
            resource_requirements=complexity_estimate['resources'],
            fallback_options=agent_decision.get('fallbacks', [])
        )
        
        # Learn from this decision for future improvement
        await self._record_decision_pattern(message, features, decision)
        
        return decision
    
    def _extract_message_features(self, message: str) -> Dict[str, Any]:
        """Extract key features from user message"""
        
        features = {
            'length': len(message),
            'word_count': len(message.split()),
            'has_code': bool(re.search(r'```|`[\w\s]+`|def |class |import |function', message)),
            'has_error': bool(re.search(r'error|exception|failed|broken|bug|issue', message.lower())),
            'has_deployment': bool(re.search(r'deploy|production|server|hosting|docker|kubernetes', message.lower())),
            'has_research': bool(re.search(r'research|find|search|learn|explore|analyze', message.lower())),
            'has_integration': bool(re.search(r'integrate|connect|api|webhook|sync', message.lower())),
            'has_question': '?' in message,
            'has_request': bool(re.search(r'can you|please|help|need|want|create|build|make', message.lower())),
            'urgency_indicators': len(re.findall(r'urgent|asap|immediately|quickly|fast|now', message.lower())),
            'complexity_indicators': len(re.findall(r'complex|advanced|sophisticated|enterprise|scalable', message.lower())),
            'collaborative_indicators': bool(re.search(r'team|collaborate|together|we|us|our', message.lower())),
        }
        
        # Keyword categories
        features.update({
            'keywords_research': len(re.findall(r'research|analyze|study|investigate|explore', message.lower())),
            'keywords_code': len(re.findall(r'code|function|class|method|algorithm|program', message.lower())),
            'keywords_deploy': len(re.findall(r'deploy|production|server|cloud|docker|k8s', message.lower())),
            'keywords_debug': len(re.findall(r'debug|fix|error|bug|issue|problem', message.lower())),
            'keywords_learn': len(re.findall(r'learn|tutorial|guide|documentation|example', message.lower())),
        })
        
        return features
    
    async def _build_contextual_knowledge(self, context: Dict[str, Any]) -> ContextualKnowledge:
        """Build comprehensive contextual knowledge"""
        
        user_id = context.get('user_id', 'default')
        
        # Get user patterns from memory - use fallback if method doesn't exist
        try:
            if hasattr(self.memory, 'get_user_patterns'):
                user_patterns = await self.memory.get_user_patterns(user_id)
            else:
                # Fallback for basic memory manager
                user_patterns = {'common_patterns': [], 'preferences': {}, 'success_rates_by_agent': {}}
        except Exception as e:
            logger.warning(f"Could not get user patterns: {e}")
            user_patterns = {'common_patterns': [], 'preferences': {}, 'success_rates_by_agent': {}}
        
        # Analyze recent conversation history - use fallback if method doesn't exist
        try:
            if hasattr(self.memory, 'get_recent_conversations'):
                recent_conversations = await self.memory.get_recent_conversations(user_id, limit=10)
            else:
                # Fallback for basic memory manager
                recent_conversations = []
        except Exception as e:
            logger.warning(f"Could not get recent conversations: {e}")
            recent_conversations = []
        
        # Extract expertise level from interaction history
        expertise_level = self._infer_expertise_level(recent_conversations, user_patterns)
        
        # Identify current project focus
        current_focus = self._identify_current_focus(recent_conversations)
        
        return ContextualKnowledge(
            user_expertise_level=expertise_level,
            current_focus=current_focus,
            recent_patterns=user_patterns.get('common_patterns', []),
            user_preferences=user_patterns.get('preferences', {}),
            success_history=user_patterns.get('success_rates_by_agent', {})
        )
    
    async def _classify_workflow_type(self, message: str, features: Dict, knowledge: ContextualKnowledge) -> WorkflowType:
        """Classify the type of workflow needed"""
        
        # Rule-based classification with AI backup
        classification_prompt = f"""
        Analyze this user request and classify the workflow type:
        
        Message: "{message}"
        
        User expertise: {knowledge.user_expertise_level}
        Current focus: {knowledge.current_focus}
        
        Features detected:
        - Has code: {features['has_code']}
        - Has error: {features['has_error']} 
        - Has research: {features['has_research']}
        - Has deployment: {features['has_deployment']}
        - Complexity: {features['complexity_indicators']}/10
        - Urgency: {features['urgency_indicators']}/10
        
        Classify as one of:
        1. SIMPLE_QUERY - Basic questions, quick answers
        2. RESEARCH_TASK - Deep research, analysis, learning
        3. CODE_GENERATION - Writing, reviewing, or modifying code
        4. DEPLOYMENT_TASK - Deployment, DevOps, infrastructure
        5. COMPLEX_PROJECT - Multi-step projects requiring planning
        6. TROUBLESHOOTING - Debugging, fixing issues
        7. LEARNING_SESSION - Teaching, explaining, exploring
        
        Return only the classification name.
        """
        
        try:
            # Use model manager if it has the capability
            if hasattr(self.model_manager, 'get_response'):
                result = await self.model_manager.get_response(
                    prompt=classification_prompt,
                    mama_bear_variant='lead_developer',
                    required_capabilities=['chat']
                )
                
                if result.get('success'):
                    classification = result['response'].strip().upper()
                    for workflow_type in WorkflowType:
                        if workflow_type.value.upper() in classification:
                            return workflow_type
        except Exception as e:
            logger.warning(f"AI workflow classification failed: {e}")
        
        # Fallback to rule-based classification
        if features['has_error'] or features['keywords_debug'] > 0:
            return WorkflowType.TROUBLESHOOTING
        elif features['has_deployment'] or features['keywords_deploy'] > 0:
            return WorkflowType.DEPLOYMENT_TASK
        elif features['has_code'] or features['keywords_code'] > 0:
            return WorkflowType.CODE_GENERATION
        elif features['has_research'] or features['keywords_research'] > 0:
            return WorkflowType.RESEARCH_TASK
        elif features['complexity_indicators'] > 2 or features['word_count'] > 100:
            return WorkflowType.COMPLEX_PROJECT
        elif features['keywords_learn'] > 0:
            return WorkflowType.LEARNING_SESSION
        else:
            return WorkflowType.SIMPLE_QUERY
    
    async def _select_optimal_agents(self, workflow_type: WorkflowType, features: Dict, knowledge: ContextualKnowledge) -> Dict[str, Any]:
        """Select the best agents for this workflow"""
        
        # Get template for this workflow type
        template = self.workflow_templates.get(workflow_type.value, {})
        base_agents = template.get('agent_sequence', ['lead_developer'])
        
        # AI-powered agent selection
        selection_prompt = f"""
        Select optimal Mama Bear agents for this workflow:
        
        Workflow Type: {workflow_type.value}
        User Expertise: {knowledge.user_expertise_level}
        Template Suggests: {base_agents}
        
        Available Agents:
        - research_specialist: Deep research, web search, analysis
        - devops_specialist: Deployment, infrastructure, optimization
        - scout_commander: Autonomous exploration, data gathering
        - model_coordinator: AI model management, optimization
        - tool_curator: Tool discovery, integration, recommendations
        - integration_architect: API connections, system integration
        - live_api_specialist: Real-time features, live interactions
        - lead_developer: Planning, coordination, complex coding
        
        User Success History: {knowledge.success_history}
        
        Recommend:
        1. Primary agent (most important)
        2. Supporting agents (if collaboration needed)
        3. Confidence level (low/medium/high/certain)
        4. Reasoning for selection
        5. Fallback options if primary fails
        
        Format as JSON:
        {{
          "primary": "agent_id",
          "supporting": ["agent1", "agent2"],
          "confidence": "high",
          "reasoning": "explanation",
          "fallbacks": ["fallback1", "fallback2"]
        }}
        """
        
        try:
            if hasattr(self.model_manager, 'get_response'):
                result = await self.model_manager.get_response(
                    prompt=selection_prompt,
                    mama_bear_variant='lead_developer',
                    required_capabilities=['chat']
                )
                
                if result.get('success'):
                    # Try to parse JSON from response
                    response_text = result['response']
                    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                    if json_match:
                        selection = json.loads(json_match.group())
                        
                        # Build agent list
                        agents = [selection['primary']]
                        if 'supporting' in selection:
                            agents.extend(selection['supporting'])
                        
                        return {
                            'agents': agents,
                            'confidence': DecisionConfidence(selection.get('confidence', 'medium')),
                            'reasoning': selection.get('reasoning', 'AI-selected based on workflow type'),
                            'fallbacks': selection.get('fallbacks', base_agents)
                        }
        except Exception as e:
            logger.warning(f"AI agent selection failed: {e}")
        
        # Fallback to rule-based selection
        confidence = DecisionConfidence.MEDIUM
        reasoning = f"Template-based selection for {workflow_type.value}"
        
        # Adjust based on user success history
        if knowledge.success_history:
            best_agent = max(knowledge.success_history.items(), key=lambda x: x[1])[0]
            if best_agent in base_agents:
                base_agents = [best_agent] + [a for a in base_agents if a != best_agent]
                confidence = DecisionConfidence.HIGH
                reasoning += f" (prioritized {best_agent} based on success history)"
        
        return {
            'agents': base_agents,
            'confidence': confidence,
            'reasoning': reasoning,
            'fallbacks': ['lead_developer'] if 'lead_developer' not in base_agents else ['research_specialist']
        }
    
    def _estimate_complexity(self, features: Dict, workflow_type: WorkflowType) -> Dict[str, Any]:
        """Estimate complexity and resource requirements"""
        
        base_complexity = {
            WorkflowType.SIMPLE_QUERY: 2,
            WorkflowType.RESEARCH_TASK: 5,
            WorkflowType.CODE_GENERATION: 6,
            WorkflowType.DEPLOYMENT_TASK: 7,
            WorkflowType.COMPLEX_PROJECT: 9,
            WorkflowType.TROUBLESHOOTING: 4,
            WorkflowType.LEARNING_SESSION: 3
        }.get(workflow_type, 5)
        
        # Adjust based on features
        complexity_modifiers = (
            features['complexity_indicators'] * 0.5 +
            features['word_count'] / 50 +
            (1 if features['has_code'] else 0) +
            (1 if features['has_integration'] else 0)
        )
        
        final_complexity = min(10, max(1, base_complexity + complexity_modifiers))
        
        # Estimate duration (minutes)
        duration_map = {
            1: 2, 2: 5, 3: 10, 4: 15, 5: 30,
            6: 45, 7: 60, 8: 90, 9: 120, 10: 180
        }
        duration = duration_map.get(int(final_complexity), 30)
        
        # Resource requirements
        resources = {
            'api_calls_estimated': int(final_complexity * 3),
            'scrapybara_needed': features['has_deployment'] or features['has_research'],
            'memory_intensive': final_complexity > 7,
            'requires_collaboration': final_complexity > 6,
            'max_parallel_agents': min(3, int(final_complexity / 3) + 1)
        }
        
        return {
            'complexity': int(final_complexity),
            'duration': duration,
            'resources': resources
        }
    
    def _infer_expertise_level(self, conversations: List[Dict], patterns: Dict) -> str:
        """Infer user expertise level from conversation history"""
        
        if not conversations:
            return "intermediate"
        
        # Look for indicators
        technical_terms = 0
        code_frequency = 0
        complex_requests = 0
        
        for conv in conversations[-10:]:  # Last 10 conversations
            message = conv.get('message', '').lower()
            
            # Count technical terms
            tech_keywords = ['api', 'database', 'framework', 'architecture', 'algorithm', 
                           'optimization', 'scalability', 'microservices', 'kubernetes', 'docker']
            technical_terms += sum(1 for term in tech_keywords if term in message)
            
            # Code frequency
            if '```' in conv.get('message', '') or 'function' in message:
                code_frequency += 1
            
            # Complex request patterns
            if len(message.split()) > 50 or 'complex' in message or 'advanced' in message:
                complex_requests += 1
        
        score = technical_terms + (code_frequency * 2) + (complex_requests * 1.5)
        
        if score >= 15:
            return "expert"
        elif score >= 8:
            return "advanced"
        elif score >= 3:
            return "intermediate"
        else:
            return "beginner"
    
    def _identify_current_focus(self, conversations: List[Dict]) -> Optional[str]:
        """Identify what the user is currently working on"""
        
        if not conversations:
            return None
        
        # Look for patterns in recent conversations
        recent_topics = []
        for conv in conversations[-5:]:
            message = conv.get('message', '').lower()
            
            # Project indicators
            if 'project' in message or 'app' in message or 'application' in message:
                # Try to extract project name/type
                words = message.split()
                for i, word in enumerate(words):
                    if word in ['project', 'app', 'application'] and i > 0:
                        recent_topics.append(words[i-1])
            
            # Technology focus
            tech_focus = ['react', 'python', 'node', 'django', 'flask', 'api', 'database']
            for tech in tech_focus:
                if tech in message:
                    recent_topics.append(tech)
        
        if recent_topics:
            # Return most common focus
            from collections import Counter
            return Counter(recent_topics).most_common(1)[0][0]
        
        return None
    
    async def _record_decision_pattern(self, message: str, features: Dict, decision: WorkflowDecision):
        """Record decision patterns for learning"""
        
        pattern = {
            'timestamp': datetime.now(),
            'message_hash': hash(message) % 10000,  # Anonymized
            'features': features,
            'decision': {
                'type': decision.decision_type,
                'agents': decision.selected_agents,
                'confidence': decision.confidence.value,
                'complexity': decision.estimated_complexity
            }
        }
        
        # Store pattern for learning
        pattern_key = f"{decision.decision_type}_{decision.estimated_complexity}"
        if pattern_key not in self.decision_patterns:
            self.decision_patterns[pattern_key] = []
        
        self.decision_patterns[pattern_key].append(pattern)
        
        # Keep only recent patterns (last 100 per type)
        self.decision_patterns[pattern_key] = self.decision_patterns[pattern_key][-100:]
        
        # Save to memory if enhanced memory is available
        try:
            if hasattr(self.memory, 'save_decision_pattern'):
                await self.memory.save_decision_pattern('system', pattern)
        except Exception as e:
            logger.warning(f"Could not save decision pattern: {e}")
    
    async def _load_historical_patterns(self):
        """Load historical decision patterns from memory"""
        try:
            if hasattr(self.memory, 'get_decision_patterns'):
                patterns = await self.memory.get_decision_patterns()
                if patterns:
                    self.decision_patterns = patterns
                    logger.info(f"Loaded {len(patterns)} historical decision patterns")
        except Exception as e:
            logger.warning(f"Could not load historical patterns: {e}")
    
    async def update_agent_performance(self, agent_id: str, task_result: Dict[str, Any]):
        """Update agent performance tracking"""
        
        if agent_id not in self.agent_performance_history:
            self.agent_performance_history[agent_id] = {
                'total_tasks': 0,
                'successful_tasks': 0,
                'avg_duration': 0,
                'complexity_handled': [],
                'recent_performance': []
            }
        
        history = self.agent_performance_history[agent_id]
        
        # Update metrics
        history['total_tasks'] += 1
        if task_result.get('success', False):
            history['successful_tasks'] += 1
        
        # Track performance over time
        performance_entry = {
            'timestamp': datetime.now(),
            'success': task_result.get('success', False),
            'duration': task_result.get('duration', 0),
            'complexity': task_result.get('complexity', 5),
            'user_satisfaction': task_result.get('user_satisfaction', 3)  # 1-5 scale
        }
        
        history['recent_performance'].append(performance_entry)
        history['recent_performance'] = history['recent_performance'][-50:]  # Keep last 50
        
        # Update averages
        recent_durations = [p['duration'] for p in history['recent_performance'] if p['duration'] > 0]
        if recent_durations:
            history['avg_duration'] = sum(recent_durations) / len(recent_durations)
        
        logger.info(f"Updated performance for {agent_id}: {history['successful_tasks']}/{history['total_tasks']} success rate")

class CollaborationOrchestrator:
    """Orchestrates collaboration between multiple agents"""
    
    def __init__(self, workflow_intelligence: WorkflowIntelligence):
        self.workflow_intelligence = workflow_intelligence
        self.active_collaborations = {}
    
    async def orchestrate_collaborative_workflow(self, decision: WorkflowDecision, message: str, context: Dict) -> Dict[str, Any]:
        """Orchestrate a collaborative workflow between multiple agents"""
        
        collaboration_id = f"collab_{datetime.now().timestamp()}"
        
        # Determine collaboration strategy
        strategy = await self._determine_collaboration_strategy(decision)
        
        # Execute based on strategy
        if strategy['type'] == 'sequential':
            return await self._execute_sequential_workflow(collaboration_id, decision, message, context, strategy)
        elif strategy['type'] == 'parallel':
            return await self._execute_parallel_workflow(collaboration_id, decision, message, context, strategy)
        elif strategy['type'] == 'hierarchical':
            return await self._execute_hierarchical_workflow(collaboration_id, decision, message, context, strategy)
        else:
            # Default to simple delegation
            return await self._execute_simple_delegation(decision, message, context)
    
    async def _determine_collaboration_strategy(self, decision: WorkflowDecision) -> Dict[str, Any]:
        """Determine how agents should collaborate"""
        
        agent_count = len(decision.selected_agents)
        complexity = decision.estimated_complexity
        
        if agent_count == 1:
            return {'type': 'simple', 'coordination': 'none'}
        elif complexity <= 4:
            return {'type': 'sequential', 'coordination': 'loose'}
        elif complexity <= 7:
            return {'type': 'parallel', 'coordination': 'moderate', 'sync_points': 2}
        else:
            return {'type': 'hierarchical', 'coordination': 'tight', 'lead_agent': decision.selected_agents[0]}
    
    async def _execute_simple_delegation(self, decision: WorkflowDecision, message: str, context: Dict) -> Dict[str, Any]:
        """Execute simple single-agent delegation"""
        
        primary_agent = decision.selected_agents[0] if decision.selected_agents else 'lead_developer'
        
        return {
            'success': True,
            'type': 'simple_delegation',
            'content': f"I'll handle this as {primary_agent}: {message}",
            'selected_agent': primary_agent,
            'reasoning': decision.reasoning,
            'estimated_duration': decision.estimated_duration,
            'metadata': {
                'decision_confidence': decision.confidence.value,
                'complexity': decision.estimated_complexity,
                'workflow_type': decision.decision_type
            }
        }
    
    async def _execute_sequential_workflow(self, collab_id: str, decision: WorkflowDecision, message: str, context: Dict, strategy: Dict) -> Dict[str, Any]:
        """Execute agents sequentially, each building on the previous"""
        
        # For now, return a structured response indicating sequential planning
        return {
            'success': True,
            'type': 'sequential_workflow',
            'content': f"I'll work on this step by step using {len(decision.selected_agents)} specialists:\n\n" +
                      "\n".join([f"Step {i+1}: {agent}" for i, agent in enumerate(decision.selected_agents)]) +
                      f"\n\nEstimated time: {decision.estimated_duration} minutes",
            'collaboration_id': collab_id,
            'agents': decision.selected_agents,
            'strategy': strategy,
            'reasoning': decision.reasoning
        }
    
    async def _execute_parallel_workflow(self, collab_id: str, decision: WorkflowDecision, message: str, context: Dict, strategy: Dict) -> Dict[str, Any]:
        """Execute agents in parallel for different aspects"""
        
        return {
            'success': True,
            'type': 'parallel_workflow',
            'content': f"I'll tackle this from multiple angles simultaneously:\n\n" +
                      "\n".join([f"• {agent} (specialized approach)" for agent in decision.selected_agents]) +
                      f"\n\nWe'll synthesize the results for a comprehensive solution.",
            'collaboration_id': collab_id,
            'agents': decision.selected_agents,
            'strategy': strategy,
            'reasoning': decision.reasoning
        }
    
    async def _execute_hierarchical_workflow(self, collab_id: str, decision: WorkflowDecision, message: str, context: Dict, strategy: Dict) -> Dict[str, Any]:
        """Execute hierarchical workflow with lead coordination"""
        
        lead_agent = strategy.get('lead_agent', decision.selected_agents[0])
        supporting_agents = [a for a in decision.selected_agents if a != lead_agent]
        
        return {
            'success': True,
            'type': 'hierarchical_workflow',
            'content': f"This is a complex request that needs careful coordination.\n\n" +
                      f"**Lead:** {lead_agent} (overall coordination)\n" +
                      f"**Team:** {', '.join(supporting_agents)}\n\n" +
                      f"I'll develop a detailed plan and coordinate execution across the team.",
            'collaboration_id': collab_id,
            'lead_agent': lead_agent,
            'supporting_agents': supporting_agents,
            'strategy': strategy,
            'reasoning': decision.reasoning
        }

# Integration function
async def initialize_workflow_intelligence(model_manager=None, memory_manager=None) -> WorkflowIntelligence:
    """Initialize the workflow intelligence system"""
    
    workflow_intelligence = WorkflowIntelligence(model_manager, memory_manager)
    
    logger.info("🧠 Mama Bear Workflow Intelligence initialized!")
    
    return workflow_intelligence

def create_collaboration_orchestrator(workflow_intelligence: WorkflowIntelligence) -> CollaborationOrchestrator:
    """Create collaboration orchestrator"""
    
    collaboration_orchestrator = CollaborationOrchestrator(workflow_intelligence)
    
    logger.info("🤝 Collaboration Orchestrator initialized!")
    
    return collaboration_orchestrator