"""
🐻 Enhanced Session Management using Mem0
Scout.new-level session persistence and state management for autonomous agents
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from enum import Enum
import uuid
from mem0 import Memory

logger = logging.getLogger(__name__)

class SessionState(Enum):
    """Session states for autonomous agent execution"""
    ACTIVE = "active"
    PAUSED = "paused"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FAILED = "failed"
    CHECKPOINTED = "checkpointed"

class SessionType(Enum):
    """Types of sessions for different use cases"""
    CHAT = "chat"                         # Regular chat conversations
    LONG_RUNNING = "long_running"         # Hours-long autonomous tasks (Scout.new style)
    COLLABORATION = "collaboration"       # Multi-agent collaboration
    RESEARCH = "research"                 # Research and analysis sessions
    SCRAPYBARA = "scrapybara"            # Browser automation sessions
    WORKFLOW = "workflow"                 # Complex multi-step workflows

@dataclass
class SessionCheckpoint:
    """Checkpoint data for resuming sessions"""
    checkpoint_id: str
    session_id: str
    timestamp: datetime
    state_data: Dict[str, Any]
    progress_percentage: float
    description: str
    can_resume: bool = True

@dataclass 
class EnhancedSession:
    """Enhanced session with Scout.new-level capabilities"""
    session_id: str
    user_id: str
    session_type: SessionType
    state: SessionState
    created_at: datetime
    last_activity: datetime
    expires_at: Optional[datetime] = None
    
    # Core session data
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Autonomous agent features
    agent_id: Optional[str] = None
    task_description: Optional[str] = None
    progress: float = 0.0
    progress_percentage: float = 0.0 # Added for checkpointing
    milestones: List[str] = field(default_factory=list) # Added for checkpointing
    
    # Long-running session features (Scout.new style)
    checkpoints: List[SessionCheckpoint] = field(default_factory=list)
    auto_checkpoint_interval: int = 300  # 5 minutes default
    max_runtime_hours: int = 24
    
    # Collaboration features
    participants: List[str] = field(default_factory=list)
    permissions: Dict[str, Any] = field(default_factory=dict)
    
    # Scrapybara integration
    browser_session_id: Optional[str] = None
    auth_states: Dict[str, Any] = field(default_factory=dict)
    
    # Performance tracking
    tokens_used: int = 0
    api_calls: int = 0
    cost_estimate: float = 0.0

class EnhancedSessionManager:
    """Enhanced session manager using Mem0 for persistent sessions"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize Mem0 client properly
        self.memory = None
        try:
            from mem0 import MemoryClient
            mem0_api_key = config.get("MEM0_API_KEY")
            if mem0_api_key:
                self.memory = MemoryClient(api_key=mem0_api_key)
                logger.info("✅ Session Manager Mem0 client initialized")
            else:
                logger.warning("⚠️ No MEM0_API_KEY provided for session manager")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize Mem0 client in session manager: {e}")
            self.memory = None
        
        # Active session cache for performance
        self.active_sessions: Dict[str, EnhancedSession] = {}
        
        # Background tasks
        self._background_tasks = set()
        
        logger.info("🚀 Enhanced Session Manager initialized with Mem0")
    
    async def create_session(
        self, 
        user_id: str,
        session_type: SessionType = SessionType.CHAT,
        metadata: Optional[Dict[str, Any]] = None,
        agent_id: Optional[str] = None,
        task_description: Optional[str] = None,
        max_runtime_hours: int = 24
    ) -> EnhancedSession:
        """Create a new enhanced session"""
        
        session_id = f"session_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        now = datetime.now()
        expires_at = now + timedelta(hours=max_runtime_hours) if session_type == SessionType.LONG_RUNNING else None
        
        session = EnhancedSession(
            session_id=session_id,
            user_id=user_id,
            session_type=session_type,
            state=SessionState.ACTIVE,
            created_at=now,
            last_activity=now,
            expires_at=expires_at,
            metadata=metadata or {},
            agent_id=agent_id,
            task_description=task_description,
            max_runtime_hours=max_runtime_hours
        )
        
        # Store in Mem0 for persistence
        await self._store_session_to_mem0(session)
        
        # Cache for quick access
        self.active_sessions[session_id] = session
        
        # Start background monitoring for long-running sessions
        if session_type == SessionType.LONG_RUNNING:
            await self._start_session_monitoring(session_id)
        
        logger.info(f"✅ Created {session_type.value} session {session_id} for user {user_id}")
        
        return session
    
    async def get_session(self, session_id: str) -> Optional[EnhancedSession]:
        """Get session from cache or Mem0"""
        
        # Check cache first
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.last_activity = datetime.now()
            return session
        
        # Load from Mem0
        session = await self._load_session_from_mem0(session_id)
        if session:
            # Add to cache
            self.active_sessions[session_id] = session
            session.last_activity = datetime.now()
        
        return session
    
    async def update_session(
        self, 
        session_id: str, 
        updates: Dict[str, Any],
        create_checkpoint: bool = False
    ) -> bool:
        """Update session with new data"""
        
        session = await self.get_session(session_id)
        if not session:
            logger.warning(f"Session {session_id} not found for update")
            return False
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(session, key):
                setattr(session, key, value)
            else:
                session.metadata[key] = value
        
        session.last_activity = datetime.now()
        
        # Create checkpoint if requested or if it's been a while
        if (create_checkpoint or 
            session.session_type == SessionType.LONG_RUNNING and
            self._should_auto_checkpoint(session)):
            await self.create_checkpoint(session_id, f"Auto checkpoint at {datetime.now()}")
        
        # Update in Mem0
        await self._store_session_to_mem0(session)
        
        return True
    
    async def create_checkpoint(
        self, 
        session_id: str, 
        description: str,
        state_data: Optional[Dict[str, Any]] = None
    ) -> Optional[SessionCheckpoint]:
        """Create a checkpoint for session resumption"""
        
        session = await self.get_session(session_id)
        if not session:
            return None
        
        checkpoint_id = f"cp_{uuid.uuid4().hex[:8]}"
        checkpoint = SessionCheckpoint(
            checkpoint_id=checkpoint_id,
            session_id=session_id,
            timestamp=datetime.now(),
            state_data=state_data or session.context.copy(),
            progress_percentage=session.progress,
            description=description
        )
        
        session.checkpoints.append(checkpoint)
        
        # Store checkpoint in Mem0
        await self._store_checkpoint_to_mem0(checkpoint)
        
        # Update session
        await self._store_session_to_mem0(session)
        
        logger.info(f"📍 Created checkpoint {checkpoint_id} for session {session_id}: {description}")
        
        return checkpoint
    
    async def resume_from_checkpoint(
        self, 
        session_id: str, 
        checkpoint_id: Optional[str] = None
    ) -> Optional[EnhancedSession]:
        """Resume session from a specific checkpoint (Scout.new style)"""
        
        session = await self.get_session(session_id)
        if not session:
            return None
        
        # Get the checkpoint (latest if not specified)
        checkpoint = None
        if checkpoint_id:
            checkpoint = next((cp for cp in session.checkpoints if cp.checkpoint_id == checkpoint_id), None)
        else:
            # Get latest checkpoint
            if session.checkpoints:
                checkpoint = max(session.checkpoints, key=lambda x: x.timestamp)
        
        if not checkpoint:
            logger.warning(f"No valid checkpoint found for session {session_id}")
            return None
        
        # Restore state from checkpoint
        session.context.update(checkpoint.state_data)
        session.progress = checkpoint.progress_percentage
        session.state = SessionState.ACTIVE
        session.last_activity = datetime.now()
        
        await self._store_session_to_mem0(session)
        
        logger.info(f"🔄 Resumed session {session_id} from checkpoint {checkpoint.checkpoint_id}")
        
        return session
    
    async def get_user_sessions(
        self, 
        user_id: str, 
        session_type: Optional[SessionType] = None,
        active_only: bool = True
    ) -> List[EnhancedSession]:
        """Get all sessions for a user"""
        
        try:
            # Search Mem0 for user sessions
            search_query = f"user:{user_id} category:session"
            if session_type:
                search_query += f" session_type:{session_type.value}"

            if self.memory is None:
                logger.error("EnhancedSessionManager: Mem0 client (self.memory) not initialized. Cannot get user sessions.")
                return []
            
            memories = self.memory.search(search_query, limit=50)
            
            sessions = []
            for memory in memories:
                try:
                    # Mem0 stores the primary content in 'messages' not 'memory'
                    messages_content = memory.get('messages', [])
                    session_data_str = ""
                    for msg in messages_content:
                        if isinstance(msg, dict) and 'content' in msg:
                            session_data_str += msg['content'] # Reconstruct the original dict string
                    
                    session_data = json.loads(session_data_str)
                    if 'session_id' in session_data:
                        session = self._dict_to_session(session_data)
                        
                        if active_only and session.state not in [SessionState.ACTIVE, SessionState.PAUSED]:
                            continue
                            
                        sessions.append(session)
                except json.JSONDecodeError as jde:
                    logger.warning(f"Failed to parse session JSON from memory {memory.get('id', 'unknown')}: {jde}. Content: {memory.get('messages', 'N/A')}")
                    continue
                except Exception as e:
                    logger.warning(f"Failed to parse session from memory {memory.get('id', 'unknown')}: {e}")
                    continue
            
            # Sort by last_activity. Use .get() defensively for potentially missing attributes.
            return sorted(sessions, key=lambda x: x.last_activity if hasattr(x, 'last_activity') else datetime.min, reverse=True)
        except Exception as e:
            logger.error(f"Error getting user sessions: {e}")
            return []
    
    async def cleanup_expired_sessions(self):
        """Clean up expired and old sessions"""
        
        logger.info("🧹 Starting session cleanup...")
        
        try:
            if self.memory is None:
                logger.error("EnhancedSessionManager: Mem0 client (self.memory) not initialized. Cannot cleanup expired sessions.")
                return
            # Search for all sessions
            memories = self.memory.search("category:session", limit=100)
            
            cleaned_count = 0
            for memory in memories:
                try:
                    # Mem0 stores the primary content in 'messages' not 'memory'
                    messages_content = memory.get('messages', [])
                    session_data_str = ""
                    for msg in messages_content:
                        if isinstance(msg, dict) and 'content' in msg:
                            session_data_str += msg['content'] # Reconstruct the original dict string
                    
                    
                    session_data = json.loads(session_data_str)
                    if 'session_id' in session_data:
                        session = self._dict_to_session(session_data)
                        
                        # Check if expired
                        now = datetime.now()
                        if (session.expires_at and now > session.expires_at) or \
                           (hasattr(session, 'state') and session.state == SessionState.COMPLETED and
                            hasattr(session, 'last_activity') and (now - session.last_activity).days > 7):
                            
                            # Mark as expired in cache
                            if session.session_id in self.active_sessions:
                                del self.active_sessions[session.session_id]
                            
                            logger.info(f"Marked session {session.session_id} for cleanup (expired/old)")
                            cleaned_count += 1
                            # NOTE: Actual deletion from Mem0 would require Mem0's delete functionality,
                            # which might involve searching by metadata. For now, it's a soft delete/remove from cache.
                            
                except json.JSONDecodeError as jde:
                    logger.warning(f"Failed to parse session JSON during cleanup for memory {memory.get('id', 'unknown')}: {jde}. Content: {memory.get('messages', 'N/A')}")
                    continue
                except Exception as e:
                    logger.warning(f"Failed to process session during cleanup for memory {memory.get('id', 'unknown')}: {e}")
                    continue
            
            logger.info(f"🧹 Cleaned up {cleaned_count} expired sessions")
            
        except Exception as e:
            logger.error(f"Error during session cleanup: {e}")
    
    async def get_session_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get session statistics"""
        
        try:
            if self.memory is None:
                logger.error("EnhancedSessionManager: Mem0 client (self.memory) not initialized. Cannot get session stats.")
                return {}
            query = f"user:{user_id} category:session" if user_id else "category:session"
            memories = self.memory.search(query, limit=200)
            
            stats = {
                'total_sessions': 0,
                'active_sessions': 0,
                'long_running_sessions': 0,
                'total_tokens_used': 0,
                'total_api_calls': 0,
                'total_cost_estimate': 0.0,
                'session_types': {},
                'average_session_duration_hours': 0.0
            }
            
            durations = []
            
            for memory in memories:
                try:
                    # Mem0 stores the primary content in 'messages' not 'memory'
                    messages_content = memory.get('messages', [])
                    session_data_str = ""
                    for msg in messages_content:
                        if isinstance(msg, dict) and 'content' in msg:
                            session_data_str += msg['content'] # Reconstruct the original dict string
                    
                    
                    session_data = json.loads(session_data_str)
                    if 'session_id' in session_data:
                        session = self._dict_to_session(session_data)
                        
                        stats['total_sessions'] += 1
                        
                        if hasattr(session, 'state') and session.state == SessionState.ACTIVE:
                            stats['active_sessions'] += 1
                        
                        if hasattr(session, 'session_type') and session.session_type == SessionType.LONG_RUNNING:
                            stats['long_running_sessions'] += 1
                        
                        stats['total_tokens_used'] += getattr(session, 'tokens_used', 0)
                        stats['total_api_calls'] += getattr(session, 'api_calls', 0)
                        stats['total_cost_estimate'] += getattr(session, 'cost_estimate', 0.0)
                        
                        # Session type distribution
                        if hasattr(session, 'session_type'):
                            session_type = session.session_type.value
                            stats['session_types'][session_type] = stats['session_types'].get(session_type, 0) + 1
                        
                        # Duration calculation
                        if hasattr(session, 'state') and session.state in [SessionState.COMPLETED, SessionState.FAILED] and \
                           hasattr(session, 'last_activity') and hasattr(session, 'created_at'):
                            duration = (session.last_activity - session.created_at).total_seconds() / 3600
                            durations.append(duration)
                        
                except json.JSONDecodeError as jde:
                    logger.warning(f"Failed to parse session JSON for stats for memory {memory.get('id', 'unknown')}: {jde}. Content: {memory.get('messages', 'N/A')}")
                    continue
                except Exception as e:
                    logger.warning(f"Failed to process session for stats for memory {memory.get('id', 'unknown')}: {e}")
                    continue
            
            if durations:
                stats['average_session_duration_hours'] = sum(durations) / len(durations)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting session stats: {e}")
            return {}
    
    async def enable_intelligent_checkpointing(self):
        """Enable intelligent automatic checkpointing for autonomous sessions"""
        
        logger.info("💾 Enabling intelligent checkpointing...")
        
        # Enable automatic checkpointing
        self.intelligent_checkpointing_enabled = True
        
        # Start background checkpointing service
        asyncio.create_task(self._intelligent_checkpointing_service())
        
        logger.info("✅ Intelligent checkpointing enabled")
    
    async def _intelligent_checkpointing_service(self):
        """Background service for intelligent checkpointing"""
        
        while getattr(self, 'intelligent_checkpointing_enabled', False):
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                current_time = datetime.now()
                
                # Check all active sessions for checkpointing opportunities
                for session_id, session in self.active_sessions.items():
                    try:
                        # Check if session needs checkpointing
                        should_checkpoint = False
                        
                        # Time-based checkpointing (every 30 minutes for long-running tasks)
                        if session.session_type == SessionType.LONG_RUNNING:
                            last_checkpoint = session.created_at
                            if session.checkpoints:
                                last_checkpoint = max(cp.timestamp for cp in session.checkpoints)
                            
                            if (current_time - last_checkpoint) > timedelta(minutes=30):
                                should_checkpoint = True
                        
                        # Progress-based checkpointing
                        if hasattr(session, 'progress') and session.progress > 0 and session.progress % 25 == 0:
                            # Checkpoint at 25%, 50%, 75%, etc.
                            should_checkpoint = True
                        
                        # State-change based checkpointing
                        if hasattr(session, 'state') and session.state == SessionState.PAUSED:
                            should_checkpoint = True
                        
                        if should_checkpoint:
                            await self._create_intelligent_checkpoint(session)
                    
                    except Exception as e:
                        logger.error(f"Error in intelligent checkpointing for session {session_id}: {e}")
                
            except Exception as e:
                logger.error(f"Intelligent checkpointing service error: {e}")
                await asyncio.sleep(60)
    
    async def _create_intelligent_checkpoint(self, session: EnhancedSession):
        """Create an intelligent checkpoint with context analysis"""
        
        try:
            # Analyze current state
            checkpoint_data = {
                'session_state': asdict(session),
                'timestamp': datetime.now().isoformat(),
                'progress_analysis': {
                    'completion_percentage': getattr(session, 'progress', 0.0),
                    'key_milestones': getattr(session, 'milestones', []),
                    'current_phase': 'autonomous_execution'
                },
                'context_snapshot': {
                    'user_intent': getattr(session, 'user_intent', ''),
                    'agent_states': getattr(session, 'agent_states', {}),
                    'pending_actions': getattr(session, 'pending_actions', [])
                }
            }
            
            # Create checkpoint
            checkpoint_id = f"checkpoint_{datetime.now().timestamp()}"
            checkpoint = SessionCheckpoint(
                checkpoint_id=checkpoint_id,
                session_id=session.session_id,
                timestamp=datetime.now(),
                # Ensure state_data is a dict or None, not a dataclass instance
                state_data=checkpoint_data, # This is a dict, so it's correct
                progress_percentage=getattr(session, 'progress', 0.0),
                description=f"Intelligent checkpoint - {getattr(session, 'progress', 0.0)}% complete"
            )
            
            # Store checkpoint - ensure arguments match create_checkpoint signature
            await self.create_checkpoint(
                session.session_id,
                checkpoint.description, # `description` is the second argument
                checkpoint.state_data # `state_data` is the third argument
            )
            
            logger.info(f"📸 Created intelligent checkpoint for session {session.session_id}")
            
        except Exception as e:
            logger.error(f"Failed to create intelligent checkpoint: {e}")

    # Private methods
    
    async def _store_session_to_mem0(self, session: EnhancedSession):
        """Store session to Mem0 for persistence"""
        
        if self.memory is None:
            logger.error(f"EnhancedSessionManager: Mem0 client (self.memory) not initialized. Cannot store session {session.session_id}.")
            return

        try:
            session_dict = self._session_to_dict(session)
            session_description = (
                f"Session {session.session_id}: {session.session_type.value} session "
                f"for user {session.user_id}. State: {session.state.value}. "
                f"Created: {session.created_at.isoformat()}"
            )
            
            if session.task_description:
                session_description += f". Task: {session.task_description}"
            
            metadata = {
                "category": "session",
                "session_id": session.session_id,
                "user_id": session.user_id,
                "session_type": session.session_type.value,
                "state": session.state.value,
                "timestamp": session.last_activity.isoformat(),
                "agent_id": session.agent_id or "none"
            }
            
            # Mem0's `add` method stores the `messages` list. If session_dict is huge, it might exceed limits.
            # Convert session_dict to a JSON string and store it as content in a single message.
            session_json_content = json.dumps(session_dict)
            
            self.memory.add(
                messages=[{"role": "system", "content": session_json_content}],
                user_id=session.user_id,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Failed to store session to Mem0: {e}")
    
    async def _load_session_from_mem0(self, session_id: str) -> Optional[EnhancedSession]:
        """Load session from Mem0"""
        
        try:
            memories = self.memory.search(f"session_id:{session_id}", limit=1)
            
            if not memories:
                logger.debug(f"No memories found for session_id: {session_id}")
                return None
            
            # Mem0 stores the actual data in the 'messages' field as a list of dictionaries.
            # Assuming the first message's content holds the session JSON.
            memory_entry = memories[0]
            if not isinstance(memory_entry, dict):
                logger.warning(f"Unexpected memory entry format: {memory_entry}. Skipping.")
                return None

            messages_list = memory_entry.get('messages', [])
            if not messages_list:
                logger.warning(f"No messages found in memory entry for session {session_id}.")
                return None
            
            session_data_str = ""
            for msg in messages_list:
                if isinstance(msg, dict) and 'content' in msg:
                    session_data_str += msg['content'] # Reconstruct the original dict string
            
            if not session_data_str:
                logger.warning(f"Empty session data string from memory for session {session_id}.")
                return None

            session_data = json.loads(session_data_str)
            return self._dict_to_session(session_data)
            
        except json.JSONDecodeError as jde:
            logger.error(f"Failed to parse session JSON from Mem0 for session {session_id}: {jde}. Content: {session_data_str[:100] if 'session_data_str' in locals() else 'N/A'}")
            return None
        except Exception as e:
            logger.error(f"Failed to load session from Mem0 for session {session_id}: {e}")
            return None
    
    async def _store_checkpoint_to_mem0(self, checkpoint: SessionCheckpoint):
        """Store checkpoint to Mem0"""

        if self.memory is None:
            logger.error(f"EnhancedSessionManager: Mem0 client (self.memory) not initialized. Cannot store checkpoint {checkpoint.checkpoint_id}.")
            return
        
        try:
            checkpoint_dict = asdict(checkpoint)
            # Convert datetime to string for JSON serialization
            checkpoint_dict['timestamp'] = checkpoint.timestamp.isoformat()
            
            checkpoint_description = (
                f"Checkpoint {checkpoint.checkpoint_id} for session {checkpoint.session_id}: "
                f"{checkpoint.description}. Progress: {checkpoint.progress_percentage}%"
            )
            
            metadata = {
                "category": "checkpoint",
                "checkpoint_id": checkpoint.checkpoint_id,
                "session_id": checkpoint.session_id,
                "timestamp": checkpoint.timestamp.isoformat(),
                "progress": checkpoint.progress_percentage
            }
            
            # Mem0's `add` method stores the `messages` list.
            # Store the checkpoint_dict as content in a single message within the messages list.
            checkpoint_json_content = json.dumps(checkpoint_dict)

            self.memory.add(
                messages=[{"role": "system", "content": checkpoint_json_content}],
                user_id="system",  # Checkpoints are system-level
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Failed to store checkpoint to Mem0: {e}")
    
    def _session_to_dict(self, session: EnhancedSession) -> Dict[str, Any]:
        """Convert session to dictionary for serialization"""
        
        session_dict = asdict(session)
        
        # Convert datetime objects to ISO strings
        session_dict['created_at'] = session.created_at.isoformat()
        session_dict['last_activity'] = session.last_activity.isoformat()
        if session.expires_at:
            session_dict['expires_at'] = session.expires_at.isoformat()
        else:
            session_dict['expires_at'] = None
        
        # Convert enums to strings
        session_dict['session_type'] = session.session_type.value
        session_dict['state'] = session.state.value
        
        # Convert checkpoints
        checkpoints = []
        for cp in session.checkpoints:
            cp_dict = asdict(cp)
            cp_dict['timestamp'] = cp.timestamp.isoformat()
            checkpoints.append(cp_dict)
        session_dict['checkpoints'] = checkpoints
        
        return session_dict
    
    def _dict_to_session(self, session_dict: Dict[str, Any]) -> EnhancedSession:
        """Convert dictionary back to session object"""
        
        # Convert datetime strings back to datetime objects
        session_dict['created_at'] = datetime.fromisoformat(session_dict['created_at'])
        session_dict['last_activity'] = datetime.fromisoformat(session_dict['last_activity'])
        if session_dict.get('expires_at'):
            session_dict['expires_at'] = datetime.fromisoformat(session_dict['expires_at'])
        
        # Convert enum strings back to enums
        session_dict['session_type'] = SessionType(session_dict['session_type'])
        session_dict['state'] = SessionState(session_dict['state'])
        
        # Convert checkpoints
        checkpoints = []
        for cp_dict in session_dict.get('checkpoints', []):
            cp_dict['timestamp'] = datetime.fromisoformat(cp_dict['timestamp'])
            checkpoints.append(SessionCheckpoint(**cp_dict))
        session_dict['checkpoints'] = checkpoints
        
        return EnhancedSession(**session_dict)
    
    def _should_auto_checkpoint(self, session: EnhancedSession) -> bool:
        """Check if session should auto-checkpoint"""
        
        if not session.checkpoints:
            return True  # First checkpoint
        
        latest_checkpoint = max(session.checkpoints, key=lambda x: x.timestamp)
        time_since_checkpoint = (datetime.now() - latest_checkpoint.timestamp).seconds
        
        return time_since_checkpoint >= session.auto_checkpoint_interval
    
    async def _start_session_monitoring(self, session_id: str):
        """Start background monitoring for long-running sessions"""
        
        async def monitor_session():
            while session_id in self.active_sessions:
                try:
                    session = self.active_sessions[session_id]
                    
                    # Check if session should be auto-checkpointed
                    if self._should_auto_checkpoint(session):
                        await self.create_checkpoint(
                            session_id, 
                            f"Auto checkpoint - {datetime.now().strftime('%H:%M:%S')}"
                        )
                    
                    # Check if session has expired
                    if session.expires_at and datetime.now() > session.expires_at:
                        session.state = SessionState.COMPLETED
                        await self._store_session_to_mem0(session)
                        logger.info(f"⏰ Session {session_id} expired and marked as completed")
                        break
                    
                    await asyncio.sleep(60)  # Check every minute
                    
                except Exception as e:
                    logger.error(f"Error monitoring session {session_id}: {e}")
                    await asyncio.sleep(60)
        
        # Start monitoring task
        task = asyncio.create_task(monitor_session())
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        
        logger.info(f"🔍 Started monitoring for long-running session {session_id}")

    async def create_intelligent_checkpoint(self, session_id: str, description: str, state_data: Optional[Dict[str, Any]] = None) -> Optional[SessionCheckpoint]:
        """Stub for create_intelligent_checkpoint method"""
        logger.info(f"Stub: create_intelligent_checkpoint called for session {session_id}")
        session = await self.get_session(session_id)
        if session:
            # Create a mock checkpoint since this is a stub
            checkpoint_id = f"mock_cp_{uuid.uuid4().hex[:4]}"
            mock_checkpoint = SessionCheckpoint(
                checkpoint_id=checkpoint_id,
                session_id=session_id,
                timestamp=datetime.now(),
                state_data=state_data or {"message": "mock checkpoint data"},
                progress_percentage=getattr(session, 'progress', 0.0), # Use actual session progress
                description=description
            )
            session.checkpoints.append(mock_checkpoint)
            await self._store_session_to_mem0(session) # Persist the updated session with checkpoint
            logger.info(f"Stub: Successfully created mock checkpoint {checkpoint_id} for session {session_id}")
            return mock_checkpoint
        return None

    async def get_system_health(self) -> Dict[str, Any]:
        """Stub for get_system_health method"""
        logger.info("Stub: get_system_health called for EnhancedSessionManager")
        return {
            "status": "healthy",
            "message": "Session Manager is operational (stub)",
            "active_sessions_count": len(self.active_sessions),
            "mem0_client_initialized": self.memory is not None
        }

# Integration function for the orchestration system
def create_enhanced_session_manager(config: Dict[str, Any]) -> EnhancedSessionManager:
    """Create enhanced session manager with Mem0 integration"""
    return EnhancedSessionManager(config)
