# backend/services/enhanced_memory_system.py
"""
🐻 Enhanced Mama Bear Memory & Context System
Advanced memory management for persistent agent context and learning
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from collections import defaultdict, deque
import hashlib
import pickle
import os

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    CONVERSATION = "conversation"
    AGENT_CONTEXT = "agent_context"
    USER_PATTERN = "user_pattern"
    DECISION_PATTERN = "decision_pattern"
    COLLABORATION_HISTORY = "collaboration_history"
    LEARNING_INSIGHT = "learning_insight"
    PROJECT_CONTEXT = "project_context"

class MemoryImportance(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1

@dataclass
class MemoryRecord:
    """Represents a single memory record"""
    id: str
    type: MemoryType
    content: Dict[str, Any]
    user_id: str
    agent_id: Optional[str] = None
    importance: MemoryImportance = MemoryImportance.MEDIUM
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    accessed_at: Optional[datetime] = None
    access_count: int = 0
    related_memories: Optional[List[str]] = None
    embedding: Optional[List[float]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.accessed_at is None:
            self.accessed_at = self.created_at
        if self.related_memories is None:
            self.related_memories = []

@dataclass
class UserProfile:
    """Comprehensive user profile built from interactions"""
    user_id: str
    expertise_level: str = "intermediate"
    preferred_agents: Optional[List[str]] = None
    communication_style: Optional[Dict[str, float]] = None
    project_history: Optional[List[Dict]] = None
    success_patterns: Optional[Dict[str, float]] = None
    learning_preferences: Optional[Dict[str, Any]] = None
    context_retention_days: int = 30
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        if self.preferred_agents is None:
            self.preferred_agents = []
        if self.communication_style is None:
            self.communication_style = {
                'technical_depth': 0.5,
                'verbosity': 0.5,
                'formality': 0.3,
                'example_preference': 0.8
            }
        if self.project_history is None:
            self.project_history = []
        if self.success_patterns is None:
            self.success_patterns = {}
        if self.learning_preferences is None:
            self.learning_preferences = {}
        if self.last_updated is None:
            self.last_updated = datetime.now()

class EnhancedMemoryManager:
    """Advanced memory management with learning and context awareness"""
    
    def __init__(self, mem0_client=None, local_storage_path="./mama_bear_memory"):
        self.mem0_client = mem0_client
        self.local_storage_path = local_storage_path
        
        # In-memory caches for performance
        self.memory_cache = {}
        self.user_profiles = {}
        self.agent_contexts = {}
        self.conversation_summaries = {}
        
        # Memory organization
        self.memory_index = defaultdict(list)  # Tags to memory IDs
        self.user_memory_index = defaultdict(list)  # User ID to memory IDs
        self.temporal_index = defaultdict(list)  # Date to memory IDs
        
        # Learning patterns
        self.pattern_frequency = defaultdict(int)
        self.success_correlation = defaultdict(float)
        
        # Initialize storage
        self._ensure_storage_directory()
        asyncio.create_task(self._load_persistent_data())
        
        # Background tasks
        asyncio.create_task(self._memory_consolidation_loop())
        asyncio.create_task(self._pattern_analysis_loop())
    
    def _ensure_storage_directory(self):
        """Ensure local storage directory exists"""
        os.makedirs(self.local_storage_path, exist_ok=True)
        os.makedirs(f"{self.local_storage_path}/memories", exist_ok=True)
        os.makedirs(f"{self.local_storage_path}/profiles", exist_ok=True)
        os.makedirs(f"{self.local_storage_path}/patterns", exist_ok=True)
    
    async def save_interaction(self, user_id: str, message: str, response: str, metadata: Optional[Dict[str, Any]] = None):
        """Save a complete interaction with rich context"""
        
        if metadata is None:
            metadata = {}
        
        # Create memory record
        memory_id = self._generate_memory_id(user_id, 'interaction')
        
        interaction_data = {
            'user_message': message,
            'agent_response': response,
            'agent_id': metadata.get('agent_id'),
            'model_used': metadata.get('model_used'),
            'response_time': metadata.get('response_time'),
            'success': metadata.get('success', True),
            'page_context': metadata.get('page_context', 'main_chat'),
            'collaboration_id': metadata.get('collaboration_id'),
            'sentiment': await self._analyze_sentiment(message),
            'topics': await self._extract_topics(message, response),
            'complexity_score': self._calculate_complexity_score(message),
            'satisfaction_score': metadata.get('satisfaction_score'),
        }
        
        memory_record = MemoryRecord(
            id=memory_id,
            type=MemoryType.CONVERSATION,
            content=interaction_data,
            user_id=user_id,
            agent_id=metadata.get('agent_id'),
            importance=self._determine_importance(interaction_data),
            tags=await self._generate_tags(interaction_data)
        )
        
        # Save to memory
        await self._store_memory(memory_record)
        
        # Update user profile
        await self._update_user_profile(user_id, interaction_data)
        
        # Save to Mem0 if available
        if self.mem0_client:
            try:
                await self._save_to_mem0(memory_record)
            except Exception as e:
                logger.warning(f"Mem0 save failed: {e}")
        
        # Update indices
        self._update_indices(memory_record)
        
        logger.debug(f"Saved interaction memory {memory_id} for user {user_id}")
    
    async def get_relevant_context(self, user_id: str, query: str, agent_id: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant context for a query using semantic similarity and recency"""
        
        # Get query embedding (placeholder - would use actual embedding model)
        query_embedding = await self._get_embedding(query)
        
        # Get candidate memories
        candidates = []
        
        # Recent conversations
        recent_memories = await self._get_recent_memories(user_id, hours=24, limit=20)
        candidates.extend(recent_memories)
        
        # Similar interactions
        if query_embedding:
            similar_memories = await self._find_similar_memories(user_id, query_embedding, limit=10)
            candidates.extend(similar_memories)
        
        # Agent-specific context
        if agent_id:
            agent_memories = await self._get_agent_specific_memories(user_id, agent_id, limit=10)
            candidates.extend(agent_memories)
        
        # Remove duplicates and rank
        unique_candidates = {m['id']: m for m in candidates}.values()
        ranked_memories = await self._rank_memories_by_relevance(query, list(unique_candidates))
        
        return ranked_memories[:limit]
    
    async def save_agent_context(self, agent_id: str, user_id: str, context_data: Dict[str, Any]):
        """Save agent-specific context"""
        
        memory_id = self._generate_memory_id(user_id, f'agent_context_{agent_id}')
        
        memory_record = MemoryRecord(
            id=memory_id,
            type=MemoryType.AGENT_CONTEXT,
            content=context_data,
            user_id=user_id,
            agent_id=agent_id,
            importance=MemoryImportance.MEDIUM,
            tags=['agent_context', agent_id]
        )
        
        await self._store_memory(memory_record)
        
        # Update agent context cache
        if agent_id not in self.agent_contexts:
            self.agent_contexts[agent_id] = {}
        
        self.agent_contexts[agent_id][user_id] = context_data
    
    async def get_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Get learned patterns for a user"""
        
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
        else:
            profile = await self._load_user_profile(user_id)
        
        # Analyze recent patterns
        recent_interactions = await self._get_recent_memories(user_id, days=7)
        patterns = await self._analyze_interaction_patterns(recent_interactions)
        
        return {
            'expertise_level': profile.expertise_level,
            'preferred_agents': profile.preferred_agents or [],
            'communication_style': profile.communication_style or {},
            'success_patterns': profile.success_patterns or {},
            'recent_patterns': patterns,
            'common_topics': await self._get_common_topics(user_id),
            'collaboration_preferences': await self._get_collaboration_preferences(user_id),
            'learning_progression': await self._track_learning_progression(user_id)
        }
    
    async def save_decision_pattern(self, user_id: str, decision_data: Dict[str, Any]):
        """Save decision patterns for learning"""
        
        memory_id = self._generate_memory_id(user_id, 'decision')
        
        memory_record = MemoryRecord(
            id=memory_id,
            type=MemoryType.DECISION_PATTERN,
            content=decision_data,
            user_id=user_id,
            importance=MemoryImportance.HIGH,
            tags=['decision', 'pattern', decision_data.get('workflow_type', 'unknown')]
        )
        
        await self._store_memory(memory_record)
    
    async def get_decision_patterns(self) -> Dict[str, List[Dict]]:
        """Get historical decision patterns for learning"""
        
        patterns = {}
        
        # Load from memory
        for memory_list in self.memory_index.get('decision', []):
            memory = await self._load_memory(memory_list)
            if memory and memory.type == MemoryType.DECISION_PATTERN:
                pattern_type = memory.content.get('workflow_type', 'unknown')
                if pattern_type not in patterns:
                    patterns[pattern_type] = []
                patterns[pattern_type].append(memory.content)
        
        return patterns
    
    async def get_recent_conversations(self, user_id: Optional[str] = None, agent_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations with optional filtering"""
        
        memories = []
        
        if user_id:
            user_memories = self.user_memory_index.get(user_id, [])
            for memory_id in reversed(user_memories[-limit*2:]):  # Get more than needed for filtering
                memory = await self._load_memory(memory_id)
                if memory and memory.type == MemoryType.CONVERSATION:
                    if agent_id is None or memory.agent_id == agent_id:
                        memories.append(self._memory_to_dict(memory))
                        if len(memories) >= limit:
                            break
        
        return memories
    
    async def save_collaboration_history(self, collaboration_id: str, participants: List[str], outcome: Dict[str, Any]):
        """Save collaboration outcomes for learning"""
        
        memory_id = f"collab_{collaboration_id}"
        
        collaboration_data = {
            'collaboration_id': collaboration_id,
            'participants': participants,
            'outcome': outcome,
            'success_score': outcome.get('success_score', 0.5),
            'duration': outcome.get('duration'),
            'user_satisfaction': outcome.get('user_satisfaction'),
            'efficiency_metrics': outcome.get('efficiency_metrics', {})
        }
        
        memory_record = MemoryRecord(
            id=memory_id,
            type=MemoryType.COLLABORATION_HISTORY,
            content=collaboration_data,
            user_id=outcome.get('user_id', 'system'),
            importance=MemoryImportance.HIGH,
            tags=['collaboration', 'team_work'] + participants
        )
        
        await self._store_memory(memory_record)
    
    async def learn_from_feedback(self, interaction_id: str, feedback: Dict[str, Any]):
        """Learn from user feedback to improve future decisions"""
        
        # Find the original interaction
        memory = await self._load_memory(interaction_id)
        if not memory:
            logger.warning(f"Could not find interaction {interaction_id} for feedback")
            return
        
        # Update the memory with feedback
        memory.content['feedback'] = feedback
        memory.importance = MemoryImportance.HIGH  # Feedback makes it important
        
        # Extract learning insights
        insight_data = {
            'original_interaction': memory.content,
            'feedback': feedback,
            'learning_points': await self._extract_learning_points(memory.content, feedback),
            'improvement_suggestions': await self._generate_improvement_suggestions(memory.content, feedback)
        }
        
        # Save as learning insight
        insight_id = self._generate_memory_id(memory.user_id, 'learning')
        insight_record = MemoryRecord(
            id=insight_id,
            type=MemoryType.LEARNING_INSIGHT,
            content=insight_data,
            user_id=memory.user_id,
            agent_id=memory.agent_id,
            importance=MemoryImportance.CRITICAL,
            tags=['learning', 'feedback', 'improvement']
        )
        
        await self._store_memory(insight_record)
        
        # Update success patterns
        await self._update_success_patterns(memory.user_id, memory.content, feedback)
        
        logger.info(f"Learned from feedback for interaction {interaction_id}")
    
    async def enable_adaptive_learning(self):
        """Enable adaptive learning capabilities for autonomous intelligence"""
        
        logger.info("🧠 Enabling adaptive learning...")
        
        # Enable learning systems
        self.adaptive_learning_enabled = True
        
        # Start background learning processes
        asyncio.create_task(self._adaptive_learning_service())
        asyncio.create_task(self._pattern_analysis_service())
        
        logger.info("✅ Adaptive learning enabled")
    
    # Private helper methods
    
    def _generate_memory_id(self, user_id: str, prefix: str) -> str:
        """Generate unique memory ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        hash_input = f"{user_id}_{prefix}_{timestamp}"
        hash_suffix = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"{prefix}_{timestamp}_{hash_suffix}"
    
    async def _store_memory(self, memory: MemoryRecord):
        """Store memory record to cache and persistent storage"""
        
        # Store in cache
        self.memory_cache[memory.id] = memory
        
        # Store persistently
        file_path = f"{self.local_storage_path}/memories/{memory.id}.pkl"
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(memory, f)
        except Exception as e:
            logger.error(f"Failed to save memory {memory.id}: {e}")
    
    async def _load_memory(self, memory_id: str) -> Optional[MemoryRecord]:
        """Load memory record from cache or storage"""
        
        # Check cache first
        if memory_id in self.memory_cache:
            memory = self.memory_cache[memory_id]
            memory.accessed_at = datetime.now()
            memory.access_count += 1
            return memory
        
        # Load from storage
        file_path = f"{self.local_storage_path}/memories/{memory_id}.pkl"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    memory = pickle.load(f)
                    memory.accessed_at = datetime.now()
                    memory.access_count += 1
                    
                    # Add to cache
                    self.memory_cache[memory_id] = memory
                    return memory
            except Exception as e:
                logger.error(f"Failed to load memory {memory_id}: {e}")
        
        return None
    
    def _update_indices(self, memory: MemoryRecord):
        """Update memory indices for fast retrieval"""
        
        # Tag index
        if memory.tags:
            for tag in memory.tags:
                self.memory_index[tag].append(memory.id)
        
        # User index
        self.user_memory_index[memory.user_id].append(memory.id)
        
        # Temporal index
        if memory.created_at:
            date_key = memory.created_at.strftime("%Y-%m-%d")
            self.temporal_index[date_key].append(memory.id)
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text (placeholder for actual implementation)"""
        
        # Simple keyword-based sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'love', 'awesome', 'perfect', 'amazing']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'horrible', 'wrong', 'error']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = len(text.split())
        
        return {
            'positive': positive_count / max(total_words, 1),
            'negative': negative_count / max(total_words, 1),
            'neutral': 1 - (positive_count + negative_count) / max(total_words, 1)
        }
    
    async def _extract_topics(self, message: str, response: str) -> List[str]:
        """Extract topics from conversation (placeholder for actual implementation)"""
        
        # Simple keyword extraction
        text = f"{message} {response}".lower()
        
        topic_keywords = {
            'coding': ['code', 'function', 'class', 'method', 'programming', 'development'],
            'deployment': ['deploy', 'production', 'server', 'hosting', 'docker', 'kubernetes'],
            'research': ['research', 'analyze', 'study', 'investigate', 'explore'],
            'debugging': ['error', 'bug', 'issue', 'problem', 'fix', 'debug'],
            'learning': ['learn', 'tutorial', 'guide', 'documentation', 'example'],
            'integration': ['integrate', 'api', 'connect', 'sync', 'webhook'],
            'planning': ['plan', 'design', 'architecture', 'strategy', 'roadmap']
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _calculate_complexity_score(self, message: str) -> float:
        """Calculate complexity score for a message"""
        
        factors = {
            'length': len(message) / 1000,  # Longer messages tend to be more complex
            'technical_terms': len([w for w in message.split() if len(w) > 8]) / len(message.split()),
            'code_presence': 2.0 if '```' in message or 'function' in message else 0.0,
            'question_complexity': message.count('?') * 0.5,
            'multiple_topics': len(set(message.lower().split())) / len(message.split()) * 2
        }
        
        return min(10.0, sum(factors.values()))
    
    def _determine_importance(self, interaction_data: Dict[str, Any]) -> MemoryImportance:
        """Determine importance of an interaction"""
        
        score = 0
        
        # Factors that increase importance
        if interaction_data.get('success', True):
            score += 1
        if interaction_data.get('collaboration_id'):
            score += 2  # Collaborative interactions are important
        if interaction_data.get('complexity_score', 0) > 7:
            score += 2  # Complex interactions are important
        if interaction_data.get('satisfaction_score', 3) >= 4:
            score += 1  # High satisfaction is important
        if 'error' in interaction_data.get('user_message', '').lower():
            score += 1  # Error situations are important for learning
        
        # Map score to importance level
        if score >= 5:
            return MemoryImportance.CRITICAL
        elif score >= 4:
            return MemoryImportance.HIGH
        elif score >= 2:
            return MemoryImportance.MEDIUM
        elif score >= 1:
            return MemoryImportance.LOW
        else:
            return MemoryImportance.TRIVIAL
    
    async def _generate_tags(self, interaction_data: Dict[str, Any]) -> List[str]:
        """Generate tags for an interaction"""
        
        tags = []
        
        # Agent-based tags
        if interaction_data.get('agent_id'):
            tags.append(interaction_data['agent_id'])
        
        # Topic-based tags
        topics = interaction_data.get('topics', [])
        tags.extend(topics)
        
        # Context-based tags
        page_context = interaction_data.get('page_context')
        if page_context:
            tags.append(page_context)
        
        # Success/failure tags
        if interaction_data.get('success', True):
            tags.append('success')
        else:
            tags.append('failure')
        
        # Collaboration tags
        if interaction_data.get('collaboration_id'):
            tags.append('collaboration')
        
        # Complexity tags
        complexity = interaction_data.get('complexity_score', 0)
        if complexity > 7:
            tags.append('complex')
        elif complexity < 3:
            tags.append('simple')
        
        return list(set(tags))  # Remove duplicates
    
    async def _save_to_mem0(self, memory_record: MemoryRecord):
        """Save memory to Mem0 for advanced RAG capabilities"""
        
        if not self.mem0_client:
            return
        
        # Convert memory to Mem0 format
        mem0_data = {
            'content': json.dumps(memory_record.content),
            'metadata': {
                'id': memory_record.id,
                'type': memory_record.type.value,
                'user_id': memory_record.user_id,
                'agent_id': memory_record.agent_id,
                'importance': memory_record.importance.value,
                'tags': memory_record.tags,
                'created_at': memory_record.created_at.isoformat() if memory_record.created_at else None
            }
        }
        
        try:
            # Save to Mem0 with user-specific organization
            await self.mem0_client.add(
                messages=[{
                    "content": mem0_data['content'],
                    "role": "user"
                }],
                user_id=memory_record.user_id,
                metadata=mem0_data['metadata']
            )
        except Exception as e:
            logger.warning(f"Failed to save to Mem0: {e}")
    
    def _memory_to_dict(self, memory: MemoryRecord) -> Dict[str, Any]:
        """Convert memory record to dictionary"""
        
        result = asdict(memory)
        result['created_at'] = memory.created_at.isoformat() if memory.created_at else None
        result['accessed_at'] = memory.accessed_at.isoformat() if memory.accessed_at else None
        return result
    
    async def _get_recent_memories(self, user_id: str, hours: int = 24, days: Optional[int] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent memories for a user"""
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
        else:
            cutoff = datetime.now() - timedelta(hours=hours)
        
        recent_memories = []
        user_memory_ids = self.user_memory_index.get(user_id, [])
        
        for memory_id in reversed(user_memory_ids):  # Most recent first
            memory = await self._load_memory(memory_id)
            if memory and memory.created_at and memory.created_at >= cutoff:
                recent_memories.append(self._memory_to_dict(memory))
                if len(recent_memories) >= limit:
                    break
        
        return recent_memories
    
    async def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding for text (placeholder for actual implementation)"""
        
        # This would use an actual embedding model
        # For now, return None to skip embedding-based similarity
        return None
    
    async def _find_similar_memories(self, user_id: str, query_embedding: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """Find memories similar to query embedding"""
        
        # Placeholder for actual similarity search
        # Would use vector similarity with stored embeddings
        return []
    
    async def _get_agent_specific_memories(self, user_id: str, agent_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get memories specific to an agent"""
        
        agent_memories = []
        user_memory_ids = self.user_memory_index.get(user_id, [])
        
        for memory_id in reversed(user_memory_ids):
            memory = await self._load_memory(memory_id)
            if memory and memory.agent_id == agent_id:
                agent_memories.append(self._memory_to_dict(memory))
                if len(agent_memories) >= limit:
                    break
        
        return agent_memories
    
    async def _rank_memories_by_relevance(self, query: str, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank memories by relevance to query"""
        
        # Simple keyword-based ranking
        query_words = set(query.lower().split())
        
        def relevance_score(memory):
            content_text = str(memory.get('content', {})).lower()
            content_words = set(content_text.split())
            
            # Keyword overlap
            overlap = len(query_words.intersection(content_words))
            
            # Recency boost
            days_old = (datetime.now() - datetime.fromisoformat(memory['created_at'])).days
            recency_boost = max(0, 7 - days_old) / 7
            
            # Importance boost
            importance_map = {'critical': 5, 'high': 4, 'medium': 3, 'low': 2, 'trivial': 1}
            importance_boost = importance_map.get(memory.get('importance'), 3) / 5
            
            return overlap + recency_boost + importance_boost
        
        return sorted(memories, key=relevance_score, reverse=True)
    
    async def _load_user_profile(self, user_id: str) -> UserProfile:
        """Load or create user profile"""
        
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        
        # Try to load from storage
        profile_path = f"{self.local_storage_path}/profiles/{user_id}.pkl"
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'rb') as f:
                    profile = pickle.load(f)
                    self.user_profiles[user_id] = profile
                    return profile
            except Exception as e:
                logger.error(f"Failed to load user profile {user_id}: {e}")
        
        # Create new profile
        profile = UserProfile(user_id=user_id)
        self.user_profiles[user_id] = profile
        await self._save_user_profile(profile)
        
        return profile
    
    async def _save_user_profile(self, profile: UserProfile):
        """Save user profile to storage"""
        
        profile.last_updated = datetime.now()
        
        profile_path = f"{self.local_storage_path}/profiles/{profile.user_id}.pkl"
        try:
            with open(profile_path, 'wb') as f:
                pickle.dump(profile, f)
        except Exception as e:
            logger.error(f"Failed to save user profile {profile.user_id}: {e}")
    
    async def _update_user_profile(self, user_id: str, interaction_data: Dict[str, Any]):
        """Update user profile based on interaction"""
        
        profile = await self._load_user_profile(user_id)
        
        # Update expertise level based on interaction complexity
        complexity = interaction_data.get('complexity_score', 0)
        if complexity > 8:
            if profile.expertise_level == 'beginner':
                profile.expertise_level = 'intermediate'
            elif profile.expertise_level == 'intermediate':
                profile.expertise_level = 'advanced'
        
        # Update preferred agents
        agent_id = interaction_data.get('agent_id')
        success = interaction_data.get('success', True)
        if agent_id and success:
            if profile.preferred_agents is None:
                profile.preferred_agents = []
            if agent_id not in profile.preferred_agents:
                profile.preferred_agents.append(agent_id)
        
        # Update communication style
        sentiment = interaction_data.get('sentiment', {})
        if sentiment.get('positive', 0) > 0.5:
            if profile.communication_style is None:
                profile.communication_style = {'formality': 0.5}
            profile.communication_style['formality'] = max(0, profile.communication_style.get('formality', 0.5) - 0.05)
        
        # Save updated profile
        await self._save_user_profile(profile)
    
    async def _memory_consolidation_loop(self):
        """Background task to consolidate and clean up memories"""
        
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                # Remove old trivial memories
                cutoff = datetime.now() - timedelta(days=7)
                
                memories_to_remove = []
                for memory_id, memory in self.memory_cache.items():
                    if (memory.importance == MemoryImportance.TRIVIAL and 
                        memory.created_at < cutoff and 
                        memory.access_count == 0):
                        memories_to_remove.append(memory_id)
                
                for memory_id in memories_to_remove:
                    del self.memory_cache[memory_id]
                    # Also remove from storage
                    file_path = f"{self.local_storage_path}/memories/{memory_id}.pkl"
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                if memories_to_remove:
                    logger.info(f"Consolidated {len(memories_to_remove)} old memories")
                
            except Exception as e:
                logger.error(f"Memory consolidation error: {e}")
    
    async def _pattern_analysis_loop(self):
        """Background task to analyze patterns and update learning"""
        
        while True:
            try:
                await asyncio.sleep(1800)  # Run every 30 minutes
                
                # Analyze user patterns
                for user_id in self.user_memory_index.keys():
                    await self._analyze_user_patterns(user_id)
                
            except Exception as e:
                logger.error(f"Pattern analysis error: {e}")
    
    async def _analyze_user_patterns(self, user_id: str):
        """Analyze patterns for a specific user"""
        
        recent_memories = await self._get_recent_memories(user_id, days=7)
        
        if len(recent_memories) < 3:
            return  # Not enough data
        
        # Analyze success patterns
        successful_interactions = [m for m in recent_memories if m['content'].get('success', True)]
        failed_interactions = [m for m in recent_memories if not m['content'].get('success', True)]
        
        # Update user profile with insights
        profile = await self._load_user_profile(user_id)
        
        if successful_interactions:
            # Find patterns in successful interactions
            successful_agents = [m['agent_id'] for m in successful_interactions if m.get('agent_id')]
            for agent in set(successful_agents):
                if profile.success_patterns is None:
                    profile.success_patterns = {}
                if agent not in profile.success_patterns:
                    profile.success_patterns[agent] = 0
                profile.success_patterns[agent] += successful_agents.count(agent) / len(successful_interactions)
        
        await self._save_user_profile(profile)
    
    async def _load_persistent_data(self):
        """Load persistent data on startup"""
        
        try:
            # Load user profiles
            profiles_dir = f"{self.local_storage_path}/profiles"
            if os.path.exists(profiles_dir):
                for filename in os.listdir(profiles_dir):
                    if filename.endswith('.pkl'):
                        user_id = filename[:-4]  # Remove .pkl extension
                        profile = await self._load_user_profile(user_id)
                        self.user_profiles[user_id] = profile
            
            logger.info(f"Loaded {len(self.user_profiles)} user profiles")
            
        except Exception as e:
            logger.error(f"Failed to load persistent data: {e}")

    # Additional methods to support patterns and learning
    async def _analyze_interaction_patterns(self, recent_interactions: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in recent interactions"""
        if not recent_interactions:
            return {}
        
        patterns = {
            'avg_complexity': sum(i['content'].get('complexity_score', 0) for i in recent_interactions) / len(recent_interactions),
            'common_contexts': {},
            'success_rate': sum(1 for i in recent_interactions if i['content'].get('success', True)) / len(recent_interactions),
            'agent_preferences': {}
        }
        
        # Context analysis
        for interaction in recent_interactions:
            context = interaction['content'].get('page_context', 'unknown')
            patterns['common_contexts'][context] = patterns['common_contexts'].get(context, 0) + 1
        
        # Agent preferences
        for interaction in recent_interactions:
            agent = interaction.get('agent_id')
            if agent:
                patterns['agent_preferences'][agent] = patterns['agent_preferences'].get(agent, 0) + 1
        
        return patterns
    
    async def _get_common_topics(self, user_id: str) -> List[str]:
        """Get most common topics for a user"""
        recent_memories = await self._get_recent_memories(user_id, days=30)
        topic_counts = {}
        
        for memory in recent_memories:
            topics = memory['content'].get('topics', [])
            for topic in topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return sorted(topic_counts.keys(), key=lambda x: topic_counts[x], reverse=True)[:5]
    
    async def _get_collaboration_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get collaboration preferences for a user"""
        collaboration_memories = []
        for memory_list in self.user_memory_index.get(user_id, []):
            memory = await self._load_memory(memory_list)
            if memory and memory.type == MemoryType.COLLABORATION_HISTORY:
                collaboration_memories.append(memory)
        
        if not collaboration_memories:
            return {'prefers_collaboration': False, 'successful_collaborations': 0}
        
        successful_collabs = sum(1 for m in collaboration_memories 
                               if m.content.get('success_score', 0) > 0.7)
        
        return {
            'prefers_collaboration': len(collaboration_memories) > 2,
            'successful_collaborations': successful_collabs,
            'collaboration_success_rate': successful_collabs / len(collaboration_memories)
        }
    
    async def _track_learning_progression(self, user_id: str) -> Dict[str, Any]:
        """Track learning progression for a user"""
        profile = await self._load_user_profile(user_id)
        recent_memories = await self._get_recent_memories(user_id, days=30)
        
        if len(recent_memories) < 5:
            return {'progression': 'insufficient_data'}
        
        # Calculate average complexity over time
        first_half = recent_memories[:len(recent_memories)//2]
        second_half = recent_memories[len(recent_memories)//2:]
        
        first_complexity = sum(m['content'].get('complexity_score', 0) for m in first_half) / len(first_half)
        second_complexity = sum(m['content'].get('complexity_score', 0) for m in second_half) / len(second_half)
        
        return {
            'progression': 'improving' if second_complexity > first_complexity else 'stable',
            'complexity_trend': second_complexity - first_complexity,
            'current_level': profile.expertise_level
        }
    
    async def _extract_learning_points(self, interaction: Dict[str, Any], feedback: Dict[str, Any]) -> List[str]:
        """Extract learning points from feedback"""
        points = []
        
        if feedback.get('rating', 3) < 3:
            points.append("User was not satisfied with the response")
            if 'too_complex' in str(feedback):
                points.append("Response was too complex for user level")
            if 'not_helpful' in str(feedback):
                points.append("Response did not address user's actual need")
        
        if feedback.get('rating', 3) > 4:
            points.append("User was very satisfied with the response")
            points.append("This approach was effective for this user")
        
        return points
    
    async def _generate_improvement_suggestions(self, interaction: Dict[str, Any], feedback: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on feedback"""
        suggestions = []
        
        if feedback.get('rating', 3) < 3:
            agent_id = interaction.get('agent_id')
            if agent_id:
                suggestions.append(f"Consider routing similar requests to a different agent than {agent_id}")
            
            complexity = interaction.get('complexity_score', 0)
            if complexity > 7:
                suggestions.append("Simplify responses for this user")
                suggestions.append("Break down complex topics into smaller parts")
        
        return suggestions
    
    async def _update_success_patterns(self, user_id: str, interaction: Dict[str, Any], feedback: Dict[str, Any]):
        """Update success patterns based on feedback"""
        profile = await self._load_user_profile(user_id)
        
        agent_id = interaction.get('agent_id')
        if agent_id:
            rating = feedback.get('rating', 3)
            if profile.success_patterns is None:
                profile.success_patterns = {}
            if agent_id not in profile.success_patterns:
                profile.success_patterns[agent_id] = 0.5
            
            # Update pattern based on feedback
            current_pattern = profile.success_patterns[agent_id]
            feedback_factor = (rating - 3) / 2  # Scale to -1 to 1
            
            # Exponential moving average
            alpha = 0.1
            profile.success_patterns[agent_id] = (1 - alpha) * current_pattern + alpha * (0.5 + feedback_factor * 0.5)
        
        await self._save_user_profile(profile)
    
    async def _adaptive_learning_service(self):
        """Background service for adaptive learning from user interactions"""
        
        while getattr(self, 'adaptive_learning_enabled', False):
            try:
                await asyncio.sleep(600)  # Analyze every 10 minutes
                
                # Analyze recent interactions for learning patterns
                recent_memories = []
                cutoff_time = datetime.now() - timedelta(hours=1)
                
                for memory_list in self.memory_cache.values():
                    for memory in memory_list:
                        if memory.created_at and memory.created_at > cutoff_time:
                            recent_memories.append(memory)
                
                if recent_memories:
                    await self._extract_learning_insights(recent_memories)
                
            except Exception as e:
                logger.error(f"Adaptive learning service error: {e}")
                await asyncio.sleep(60)
    
    async def _pattern_analysis_service(self):
        """Background service for analyzing user and agent patterns"""
        
        while getattr(self, 'adaptive_learning_enabled', False):
            try:
                await asyncio.sleep(1800)  # Analyze every 30 minutes
                
                # Analyze patterns across all users
                all_patterns = {}
                for user_id in self.user_profiles.keys():
                    profile = self.user_profiles.get(user_id)
                    if profile:
                        all_patterns[user_id] = {
                            'preferences': profile.learning_preferences,
                            'success_patterns': profile.success_patterns,
                            'interaction_history': profile.interaction_history[-10:]  # Last 10 interactions
                        }
                
                # Extract global patterns
                if all_patterns:
                    global_insights = await self._analyze_global_patterns(all_patterns)
                    await self._store_global_insights(global_insights)
                
            except Exception as e:
                logger.error(f"Pattern analysis service error: {e}")
                await asyncio.sleep(300)
    
    async def _extract_learning_insights(self, memories: List[MemoryRecord]):
        """Extract learning insights from recent memories"""
        
        try:
            insights = []
            
            # Group memories by user
            user_memories = defaultdict(list)
            for memory in memories:
                user_memories[memory.user_id].append(memory)
            
            # Analyze each user's recent patterns
            for user_id, user_memory_list in user_memories.items():
                # Analyze conversation patterns
                conversation_memories = [m for m in user_memory_list if m.type == MemoryType.CONVERSATION]
                if len(conversation_memories) >= 3:
                    # Look for recurring themes or preferences
                    themes = self._extract_conversation_themes(conversation_memories)
                    if themes:
                        insight = {
                            'type': 'user_preference_pattern',
                            'user_id': user_id,
                            'themes': themes,
                            'confidence': min(len(conversation_memories) / 10.0, 1.0)
                        }
                        insights.append(insight)
                
                # Analyze success patterns
                decision_memories = [m for m in user_memory_list if m.type == MemoryType.DECISION_PATTERN]
                if decision_memories:
                    success_patterns = self._analyze_decision_success(decision_memories)
                    if success_patterns:
                        insight = {
                            'type': 'decision_success_pattern',
                            'user_id': user_id,
                            'patterns': success_patterns,
                            'confidence': len(decision_memories) / 5.0
                        }
                        insights.append(insight)
            
            # Store insights
            for insight in insights:
                # Create memory record for the insight
                memory_record = MemoryRecord(
                    id=f"insight_{datetime.now().timestamp()}",
                    type=MemoryType.LEARNING_INSIGHT,
                    content=insight,
                    user_id=insight['user_id'],
                    importance=MemoryImportance.HIGH,
                    tags=['adaptive_learning', 'insight'],
                    created_at=datetime.now()
                )
                await self._store_memory(memory_record)
            
            logger.info(f"🎯 Extracted {len(insights)} learning insights")
            
        except Exception as e:
            logger.error(f"Error extracting learning insights: {e}")
    
    def _extract_conversation_themes(self, memories: List[MemoryRecord]) -> List[str]:
        """Extract common themes from conversation memories"""
        
        themes = []
        try:
            # Simple theme extraction based on content keywords
            theme_keywords = defaultdict(int)
            
            for memory in memories:
                content = memory.content
                if 'user_message' in content:
                    message = content['user_message'].lower()
                    # Count key technical terms
                    keywords = ['python', 'javascript', 'react', 'api', 'database', 'frontend', 'backend', 'deployment']
                    for keyword in keywords:
                        if keyword in message:
                            theme_keywords[keyword] += 1
            
            # Return themes that appear in multiple conversations
            themes = [theme for theme, count in theme_keywords.items() if count >= 2]
            
        except Exception as e:
            logger.error(f"Error extracting themes: {e}")
        
        return themes
    
    def _analyze_decision_success(self, memories: List[MemoryRecord]) -> Dict[str, float]:
        """Analyze success patterns in decision memories"""
        
        patterns = {}
        try:
            for memory in memories:
                content = memory.content
                if 'decision_type' in content and 'success' in content:
                    decision_type = content['decision_type']
                    success = content['success']
                    
                    if decision_type not in patterns:
                        patterns[decision_type] = []
                    patterns[decision_type].append(1.0 if success else 0.0)
            
            # Calculate success rates
            success_rates = {}
            for decision_type, successes in patterns.items():
                if successes:
                    success_rates[decision_type] = sum(successes) / len(successes)
            
            return success_rates
            
        except Exception as e:
            logger.error(f"Error analyzing decision success: {e}")
            return {}
    
    async def _analyze_global_patterns(self, all_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns across all users to extract global insights"""
        
        global_insights = {
            'common_preferences': {},
            'successful_strategies': {},
            'user_clusters': [],
            'temporal_patterns': {}
        }
        
        try:
            # Find common preferences across users
            preference_counts = defaultdict(int)
            for user_id, patterns in all_patterns.items():
                preferences = patterns.get('preferences', {})
                for pref_key, pref_value in preferences.items():
                    preference_counts[f"{pref_key}:{pref_value}"] += 1
            
            # Store preferences that appear in multiple users
            total_users = len(all_patterns)
            for pref, count in preference_counts.items():
                if count >= max(2, total_users * 0.3):  # At least 30% of users
                    global_insights['common_preferences'][pref] = count / total_users
            
            # Analyze successful strategies
            strategy_success = defaultdict(list)
            for user_id, patterns in all_patterns.items():
                success_patterns = patterns.get('success_patterns', {})
                for strategy, success_rate in success_patterns.items():
                    strategy_success[strategy].append(success_rate)
            
            for strategy, rates in strategy_success.items():
                if rates:
                    global_insights['successful_strategies'][strategy] = {
                        'average_success': sum(rates) / len(rates),
                        'sample_size': len(rates)
                    }
            
        except Exception as e:
            logger.error(f"Error analyzing global patterns: {e}")
        
        return global_insights
    
    async def _store_global_insights(self, insights: Dict[str, Any]):
        """Store global insights for system-wide learning"""
        
        try:
            # Store in Mem0 if available
            if self.mem0_client:
                await self.mem0_client.add(
                    messages=[{
                        "role": "system",
                        "content": f"Global learning insights: {json.dumps(insights)}"
                    }],
                    user_id="system_global",
                    metadata={
                        "type": "global_insights",
                        "timestamp": datetime.now().isoformat(),
                        "insights_count": len(insights)
                    }
                )
            
            # Also store locally
            insights_path = os.path.join(self.local_storage_path, "global_insights.json")
            with open(insights_path, 'w') as f:
                json.dump({
                    'insights': insights,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2, default=str)
            
            logger.info("💡 Stored global learning insights")
            
        except Exception as e:
            logger.error(f"Error storing global insights: {e}")

# Integration function
def initialize_enhanced_memory(mem0_client=None) -> EnhancedMemoryManager:
    """Initialize the enhanced memory system"""
    
    memory_manager = EnhancedMemoryManager(mem0_client)
    logger.info("🧠 Enhanced Mama Bear Memory System initialized!")
    
    return memory_manager