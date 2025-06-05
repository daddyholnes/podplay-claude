"""
🐻 Mama Bear Collaborative Workspace System
Provides multi-user collaboration capabilities with cloud Scrapybara and local storage options
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import sqlite3
import aiosqlite
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class WorkspaceType(Enum):
    """Types of collaborative workspaces"""
    LOCAL = "local"  # Local storage only - Mama Bear focused
    CLOUD = "cloud"  # Cloud Scrapybara integration
    HYBRID = "hybrid"  # Both local and cloud capabilities


class CollaborationMode(Enum):
    """Collaboration modes for workspaces"""
    SOLO = "solo"  # Single user workspace
    SHARED = "shared"  # Multiple users can view and edit
    OBSERVER = "observer"  # Read-only access for additional users
    CONCURRENT = "concurrent"  # Real-time collaborative editing


class WorkspaceRole(Enum):
    """User roles within a workspace"""
    OWNER = "owner"
    COLLABORATOR = "collaborator"
    OBSERVER = "observer"
    GUEST = "guest"


@dataclass
class WorkspaceUser:
    """Represents a user in a workspace"""
    user_id: str
    username: str
    role: WorkspaceRole
    joined_at: datetime
    last_active: datetime
    permissions: Dict[str, bool] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkspaceSession:
    """Represents an active session within a workspace"""
    session_id: str
    user_id: str
    workspace_id: str
    started_at: datetime
    last_activity: datetime
    agent_states: Dict[str, Any] = field(default_factory=dict)
    active_tasks: List[str] = field(default_factory=list)
    shared_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SharedResource:
    """Represents a shared resource in a workspace"""
    resource_id: str
    resource_type: str  # 'file', 'agent_session', 'scrapybara_instance', 'memory_context'
    name: str
    description: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    permissions: Dict[str, List[str]]  # user_id -> [permissions]
    metadata: Dict[str, Any] = field(default_factory=dict)
    content: Optional[Any] = None


@dataclass
class CollaborativeWorkspace:
    """Main workspace data structure"""
    workspace_id: str
    name: str
    description: str
    workspace_type: WorkspaceType
    collaboration_mode: CollaborationMode
    owner_id: str
    created_at: datetime
    updated_at: datetime
    users: Dict[str, WorkspaceUser] = field(default_factory=dict)
    active_sessions: Dict[str, WorkspaceSession] = field(default_factory=dict)
    shared_resources: Dict[str, SharedResource] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    sync_metadata: Dict[str, Any] = field(default_factory=dict)


class LocalStorageManager:
    """Manages local storage for Mama Bear workspaces"""
    
    def __init__(self, storage_path: str = "data/workspaces"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.storage_path / "workspaces.db"
        asyncio.create_task(self._initialize_database())
    
    async def _initialize_database(self):
        """Initialize SQLite database for workspace storage"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS workspaces (
                    workspace_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    workspace_type TEXT NOT NULL,
                    collaboration_mode TEXT NOT NULL,
                    owner_id TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    settings TEXT,
                    sync_metadata TEXT
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS workspace_users (
                    workspace_id TEXT,
                    user_id TEXT,
                    username TEXT NOT NULL,
                    role TEXT NOT NULL,
                    joined_at TIMESTAMP NOT NULL,
                    last_active TIMESTAMP NOT NULL,
                    permissions TEXT,
                    preferences TEXT,
                    PRIMARY KEY (workspace_id, user_id),
                    FOREIGN KEY (workspace_id) REFERENCES workspaces (workspace_id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS workspace_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    started_at TIMESTAMP NOT NULL,
                    last_activity TIMESTAMP NOT NULL,
                    agent_states TEXT,
                    active_tasks TEXT,
                    shared_context TEXT,
                    FOREIGN KEY (workspace_id) REFERENCES workspaces (workspace_id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS shared_resources (
                    resource_id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    owner_id TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    permissions TEXT,
                    metadata TEXT,
                    content TEXT,
                    FOREIGN KEY (workspace_id) REFERENCES workspaces (workspace_id)
                )
            """)
            
            await db.commit()
    
    async def save_workspace(self, workspace: CollaborativeWorkspace) -> bool:
        """Save workspace to local storage"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Save main workspace record
                await db.execute("""
                    INSERT OR REPLACE INTO workspaces 
                    (workspace_id, name, description, workspace_type, collaboration_mode, 
                     owner_id, created_at, updated_at, settings, sync_metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    workspace.workspace_id,
                    workspace.name,
                    workspace.description,
                    workspace.workspace_type.value,
                    workspace.collaboration_mode.value,
                    workspace.owner_id,
                    workspace.created_at,
                    workspace.updated_at,
                    json.dumps(workspace.settings),
                    json.dumps(workspace.sync_metadata)
                ))
                
                # Save users
                for user in workspace.users.values():
                    await db.execute("""
                        INSERT OR REPLACE INTO workspace_users
                        (workspace_id, user_id, username, role, joined_at, last_active, permissions, preferences)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        workspace.workspace_id,
                        user.user_id,
                        user.username,
                        user.role.value,
                        user.joined_at,
                        user.last_active,
                        json.dumps(user.permissions),
                        json.dumps(user.preferences)
                    ))
                
                # Save shared resources
                for resource in workspace.shared_resources.values():
                    await db.execute("""
                        INSERT OR REPLACE INTO shared_resources
                        (resource_id, workspace_id, resource_type, name, description, owner_id,
                         created_at, updated_at, permissions, metadata, content)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        resource.resource_id,
                        workspace.workspace_id,
                        resource.resource_type,
                        resource.name,
                        resource.description,
                        resource.owner_id,
                        resource.created_at,
                        resource.updated_at,
                        json.dumps(resource.permissions),
                        json.dumps(resource.metadata),
                        json.dumps(resource.content) if resource.content else None
                    ))
                
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to save workspace {workspace.workspace_id}: {e}")
            return False
    
    async def load_workspace(self, workspace_id: str) -> Optional[CollaborativeWorkspace]:
        """Load workspace from local storage"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Load main workspace
                cursor = await db.execute("""
                    SELECT * FROM workspaces WHERE workspace_id = ?
                """, (workspace_id,))
                
                workspace_row = await cursor.fetchone()
                if not workspace_row:
                    return None
                
                workspace = CollaborativeWorkspace(
                    workspace_id=workspace_row[0],
                    name=workspace_row[1],
                    description=workspace_row[2],
                    workspace_type=WorkspaceType(workspace_row[3]),
                    collaboration_mode=CollaborationMode(workspace_row[4]),
                    owner_id=workspace_row[5],
                    created_at=datetime.fromisoformat(workspace_row[6]),
                    updated_at=datetime.fromisoformat(workspace_row[7]),
                    settings=json.loads(workspace_row[8]) if workspace_row[8] else {},
                    sync_metadata=json.loads(workspace_row[9]) if workspace_row[9] else {}
                )
                
                # Load users
                cursor = await db.execute("""
                    SELECT * FROM workspace_users WHERE workspace_id = ?
                """, (workspace_id,))
                
                for user_row in await cursor.fetchall():
                    user = WorkspaceUser(
                        user_id=user_row[1],
                        username=user_row[2],
                        role=WorkspaceRole(user_row[3]),
                        joined_at=datetime.fromisoformat(user_row[4]),
                        last_active=datetime.fromisoformat(user_row[5]),
                        permissions=json.loads(user_row[6]) if user_row[6] else {},
                        preferences=json.loads(user_row[7]) if user_row[7] else {}
                    )
                    workspace.users[user.user_id] = user
                
                # Load shared resources
                cursor = await db.execute("""
                    SELECT * FROM shared_resources WHERE workspace_id = ?
                """, (workspace_id,))
                
                for resource_row in await cursor.fetchall():
                    resource = SharedResource(
                        resource_id=resource_row[0],
                        resource_type=resource_row[2],
                        name=resource_row[3],
                        description=resource_row[4],
                        owner_id=resource_row[5],
                        created_at=datetime.fromisoformat(resource_row[6]),
                        updated_at=datetime.fromisoformat(resource_row[7]),
                        permissions=json.loads(resource_row[8]) if resource_row[8] else {},
                        metadata=json.loads(resource_row[9]) if resource_row[9] else {},
                        content=json.loads(resource_row[10]) if resource_row[10] else None
                    )
                    workspace.shared_resources[resource.resource_id] = resource
                
                return workspace
                
        except Exception as e:
            logger.error(f"Failed to load workspace {workspace_id}: {e}")
            return None


class CloudSyncManager:
    """Manages synchronization with cloud Scrapybara instances"""
    
    def __init__(self, scrapybara_integration):
        self.scrapybara = scrapybara_integration
        self.sync_tasks = {}  # workspace_id -> asyncio.Task
        self.sync_intervals = {}  # workspace_id -> interval_seconds
    
    async def enable_cloud_sync(self, workspace_id: str, sync_interval: int = 30):
        """Enable cloud synchronization for a workspace"""
        if workspace_id in self.sync_tasks:
            # Cancel existing sync task
            self.sync_tasks[workspace_id].cancel()
        
        self.sync_intervals[workspace_id] = sync_interval
        self.sync_tasks[workspace_id] = asyncio.create_task(
            self._sync_workspace_loop(workspace_id)
        )
    
    async def disable_cloud_sync(self, workspace_id: str):
        """Disable cloud synchronization for a workspace"""
        if workspace_id in self.sync_tasks:
            self.sync_tasks[workspace_id].cancel()
            del self.sync_tasks[workspace_id]
        
        if workspace_id in self.sync_intervals:
            del self.sync_intervals[workspace_id]
    
    async def _sync_workspace_loop(self, workspace_id: str):
        """Background sync loop for a workspace"""
        try:
            while True:
                await self._sync_workspace_to_cloud(workspace_id)
                interval = self.sync_intervals.get(workspace_id, 30)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logger.info(f"Cloud sync cancelled for workspace {workspace_id}")
        except Exception as e:
            logger.error(f"Cloud sync error for workspace {workspace_id}: {e}")
    
    async def _sync_workspace_to_cloud(self, workspace_id: str):
        """Sync workspace state to cloud Scrapybara instances"""
        try:
            # Get active Scrapybara instances for this workspace
            instances = await self.scrapybara.get_workspace_instances(workspace_id)
            
            for instance in instances:
                # Sync workspace files and state
                await self._sync_instance_state(instance, workspace_id)
                
        except Exception as e:
            logger.error(f"Failed to sync workspace {workspace_id} to cloud: {e}")
    
    async def _sync_instance_state(self, instance, workspace_id: str):
        """Sync state to a specific Scrapybara instance"""
        # Implementation depends on Scrapybara instance capabilities
        # This is a placeholder for the actual sync logic
        pass


class CollaborativeWorkspaceManager:
    """Main manager for collaborative workspaces"""
    
    def __init__(self, scrapybara_integration=None, storage_path: str = "data/workspaces"):
        self.local_storage = LocalStorageManager(storage_path)
        self.cloud_sync = CloudSyncManager(scrapybara_integration) if scrapybara_integration else None
        self.active_workspaces: Dict[str, CollaborativeWorkspace] = {}
        self.workspace_locks: Dict[str, asyncio.Lock] = {}
        
        # Event callbacks for real-time collaboration
        self.event_callbacks: Dict[str, List[Callable]] = {
            'workspace_created': [],
            'user_joined': [],
            'user_left': [],
            'resource_shared': [],
            'resource_updated': [],
            'session_started': [],
            'session_ended': []
        }
    
    def register_event_callback(self, event_type: str, callback: Callable):
        """Register callback for workspace events"""
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to registered callbacks"""
        if event_type in self.event_callbacks:
            for callback in self.event_callbacks[event_type]:
                try:
                    await callback(data)
                except Exception as e:
                    logger.error(f"Event callback error for {event_type}: {e}")
    
    async def create_workspace(
        self,
        name: str,
        owner_id: str,
        workspace_type: WorkspaceType = WorkspaceType.LOCAL,
        collaboration_mode: CollaborationMode = CollaborationMode.SOLO,
        description: str = "",
        settings: Optional[Dict[str, Any]] = None
    ) -> CollaborativeWorkspace:
        """Create a new collaborative workspace"""
        
        workspace_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Create owner user
        owner = WorkspaceUser(
            user_id=owner_id,
            username=f"user_{owner_id}",  # TODO: Get actual username
            role=WorkspaceRole.OWNER,
            joined_at=now,
            last_active=now,
            permissions={
                'read': True,
                'write': True,
                'admin': True,
                'invite': True,
                'delete': True
            }
        )
        
        workspace = CollaborativeWorkspace(
            workspace_id=workspace_id,
            name=name,
            description=description,
            workspace_type=workspace_type,
            collaboration_mode=collaboration_mode,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
            users={owner_id: owner},
            settings=settings or {}
        )
        
        # Save to storage
        await self.local_storage.save_workspace(workspace)
        
        # Cache in memory
        self.active_workspaces[workspace_id] = workspace
        self.workspace_locks[workspace_id] = asyncio.Lock()
        
        # Enable cloud sync if needed
        if workspace_type in [WorkspaceType.CLOUD, WorkspaceType.HYBRID] and self.cloud_sync:
            await self.cloud_sync.enable_cloud_sync(workspace_id)
        
        # Emit event
        await self._emit_event('workspace_created', {
            'workspace_id': workspace_id,
            'name': name,
            'owner_id': owner_id,
            'type': workspace_type.value
        })
        
        return workspace
    
    async def get_workspace(self, workspace_id: str) -> Optional[CollaborativeWorkspace]:
        """Get workspace by ID"""
        # Check memory cache first
        if workspace_id in self.active_workspaces:
            return self.active_workspaces[workspace_id]
        
        # Load from storage
        workspace = await self.local_storage.load_workspace(workspace_id)
        if workspace:
            self.active_workspaces[workspace_id] = workspace
            if workspace_id not in self.workspace_locks:
                self.workspace_locks[workspace_id] = asyncio.Lock()
        
        return workspace
    
    async def add_user_to_workspace(
        self,
        workspace_id: str,
        user_id: str,
        username: str,
        role: WorkspaceRole = WorkspaceRole.COLLABORATOR,
        inviter_id: Optional[str] = None
    ) -> bool:
        """Add user to workspace"""
        
        workspace = await self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        # Check permissions
        if inviter_id and inviter_id in workspace.users:
            inviter = workspace.users[inviter_id]
            if not inviter.permissions.get('invite', False):
                return False
        
        async with self.workspace_locks[workspace_id]:
            # Create user
            now = datetime.now()
            user = WorkspaceUser(
                user_id=user_id,
                username=username,
                role=role,
                joined_at=now,
                last_active=now,
                permissions=self._get_default_permissions(role)
            )
            
            workspace.users[user_id] = user
            workspace.updated_at = now
            
            # Save changes
            await self.local_storage.save_workspace(workspace)
        
        # Emit event
        await self._emit_event('user_joined', {
            'workspace_id': workspace_id,
            'user_id': user_id,
            'username': username,
            'role': role.value
        })
        
        return True
    
    def _get_default_permissions(self, role: WorkspaceRole) -> Dict[str, bool]:
        """Get default permissions for a role"""
        if role == WorkspaceRole.OWNER:
            return {
                'read': True,
                'write': True,
                'admin': True,
                'invite': True,
                'delete': True
            }
        elif role == WorkspaceRole.COLLABORATOR:
            return {
                'read': True,
                'write': True,
                'admin': False,
                'invite': False,
                'delete': False
            }
        elif role == WorkspaceRole.OBSERVER:
            return {
                'read': True,
                'write': False,
                'admin': False,
                'invite': False,
                'delete': False
            }
        else:  # GUEST
            return {
                'read': True,
                'write': False,
                'admin': False,
                'invite': False,
                'delete': False
            }
    
    async def create_session(
        self,
        workspace_id: str,
        user_id: str
    ) -> Optional[WorkspaceSession]:
        """Create a new session in workspace"""
        
        workspace = await self.get_workspace(workspace_id)
        if not workspace or user_id not in workspace.users:
            return None
        
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session = WorkspaceSession(
            session_id=session_id,
            user_id=user_id,
            workspace_id=workspace_id,
            started_at=now,
            last_activity=now
        )
        
        async with self.workspace_locks[workspace_id]:
            workspace.active_sessions[session_id] = session
            workspace.updated_at = now
        
        # Emit event
        await self._emit_event('session_started', {
            'workspace_id': workspace_id,
            'session_id': session_id,
            'user_id': user_id
        })
        
        return session
    
    async def share_resource(
        self,
        workspace_id: str,
        owner_id: str,
        resource_type: str,
        name: str,
        content: Any,
        description: str = "",
        permissions: Optional[Dict[str, List[str]]] = None
    ) -> Optional[SharedResource]:
        """Share a resource in the workspace"""
        
        workspace = await self.get_workspace(workspace_id)
        if not workspace or owner_id not in workspace.users:
            return None
        
        resource_id = str(uuid.uuid4())
        now = datetime.now()
        
        resource = SharedResource(
            resource_id=resource_id,
            resource_type=resource_type,
            name=name,
            description=description,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
            permissions=permissions or {},
            content=content
        )
        
        async with self.workspace_locks[workspace_id]:
            workspace.shared_resources[resource_id] = resource
            workspace.updated_at = now
            
            # Save changes
            await self.local_storage.save_workspace(workspace)
        
        # Emit event
        await self._emit_event('resource_shared', {
            'workspace_id': workspace_id,
            'resource_id': resource_id,
            'resource_type': resource_type,
            'name': name,
            'owner_id': owner_id
        })
        
        return resource
    
    async def get_user_workspaces(self, user_id: str) -> List[CollaborativeWorkspace]:
        """Get all workspaces for a user"""
        workspaces = []
        
        # This is a simplified implementation
        # In production, you'd want to query the database more efficiently
        try:
            async with aiosqlite.connect(self.local_storage.db_path) as db:
                cursor = await db.execute("""
                    SELECT DISTINCT w.workspace_id FROM workspaces w
                    JOIN workspace_users wu ON w.workspace_id = wu.workspace_id
                    WHERE wu.user_id = ?
                """, (user_id,))
                
                for row in await cursor.fetchall():
                    workspace = await self.get_workspace(row[0])
                    if workspace:
                        workspaces.append(workspace)
        
        except Exception as e:
            logger.error(f"Failed to get workspaces for user {user_id}: {e}")
        
        return workspaces
    
    async def cleanup_inactive_sessions(self, max_age_hours: int = 24):
        """Clean up inactive sessions"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for workspace in self.active_workspaces.values():
            async with self.workspace_locks[workspace.workspace_id]:
                sessions_to_remove = []
                for session_id, session in workspace.active_sessions.items():
                    if session.last_activity < cutoff_time:
                        sessions_to_remove.append(session_id)
                
                for session_id in sessions_to_remove:
                    del workspace.active_sessions[session_id]
                    
                    # Emit event
                    await self._emit_event('session_ended', {
                        'workspace_id': workspace.workspace_id,
                        'session_id': session_id,
                        'reason': 'inactive'
                    })


# Export main classes
__all__ = [
    'CollaborativeWorkspaceManager',
    'CollaborativeWorkspace', 
    'WorkspaceUser',
    'WorkspaceSession',
    'SharedResource',
    'WorkspaceType',
    'CollaborationMode',
    'WorkspaceRole',
    'LocalStorageManager',
    'CloudSyncManager'
]
