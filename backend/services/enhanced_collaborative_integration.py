"""
🐻 Enhanced Collaborative Integration for Mama Bear
Integrates collaborative workspaces with Scrapybara cloud capabilities and local storage
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .collaborative_workspace import (
    CollaborativeWorkspaceManager,
    WorkspaceType,
    CollaborationMode,
    WorkspaceRole
)
from .scrapybara_integration import ScrapybaraManager as ScrapybaraIntegrationManager # Alias for compatibility if needed, or just use ScrapybaraManager
from .enhanced_orchestration_system import EnhancedAgentOrchestrator as EnhancedOrchestrationSystem # Alias for compatibility
from .enhanced_memory_system import EnhancedMemoryManager as EnhancedMemorySystem # Alias for compatibility

logger = logging.getLogger(__name__)


class CollaborativeScrapybaraManager:
    """
    Manages collaborative Scrapybara instances for multi-user workspaces
    Provides cloud computer use capabilities with workspace isolation
    """
    
    def __init__(self, scrapybara_manager: ScrapybaraIntegrationManager):
        self.scrapybara = scrapybara_manager
        self.workspace_instances: Dict[str, List[str]] = {}  # workspace_id -> [instance_ids]
        self.instance_workspaces: Dict[str, str] = {}  # instance_id -> workspace_id
        self.user_instances: Dict[str, List[str]] = {}  # user_id -> [instance_ids]
    
    async def create_workspace_instance(
        self,
        workspace_id: str,
        user_id: str,
        instance_type: str = "ubuntu",
        shared: bool = True
    ) -> Optional[str]:
        """Create a Scrapybara instance for a workspace"""
        try:
            # Create instance with workspace context
            instance_config = {
                'instance_type': instance_type,
                'timeout_hours': 8,  # Longer timeout for collaborative work
                'metadata': {
                    'workspace_id': workspace_id,
                    'created_by': user_id,
                    'shared': shared,
                    'purpose': 'collaborative_workspace'
                }
            }
            
            instance_id = await self.scrapybara.create_instance(**instance_config)
            if instance_id:
                # Track workspace associations
                if workspace_id not in self.workspace_instances:
                    self.workspace_instances[workspace_id] = []
                self.workspace_instances[workspace_id].append(instance_id)
                
                self.instance_workspaces[instance_id] = workspace_id
                
                # Track user associations
                if user_id not in self.user_instances:
                    self.user_instances[user_id] = []
                self.user_instances[user_id].append(instance_id)
                
                logger.info(f"Created workspace instance {instance_id} for workspace {workspace_id}")
                return instance_id
            
        except Exception as e:
            logger.error(f"Failed to create workspace instance: {e}")
        
        return None
    
    async def get_workspace_instances(self, workspace_id: str) -> List[Dict[str, Any]]:
        """Get all active instances for a workspace"""
        instance_ids = self.workspace_instances.get(workspace_id, [])
        instances = []
        
        for instance_id in instance_ids:
            instance_info = await self.scrapybara.get_instance_info(instance_id)
            if instance_info and instance_info.get('is_active', False):
                instances.append({
                    'instance_id': instance_id,
                    'info': instance_info,
                    'workspace_id': workspace_id
                })
        
        return instances
    
    async def share_instance_with_user(
        self,
        instance_id: str,
        user_id: str,
        permissions: List[str] = None
    ) -> bool:
        """Share a Scrapybara instance with another user"""
        try:
            # Add user to instance permissions
            workspace_id = self.instance_workspaces.get(instance_id)
            if not workspace_id:
                return False
            
            # Track user access
            if user_id not in self.user_instances:
                self.user_instances[user_id] = []
            if instance_id not in self.user_instances[user_id]:
                self.user_instances[user_id].append(instance_id)
            
            # TODO: Implement actual Scrapybara permission sharing
            # This would depend on Scrapybara SDK capabilities
            
            logger.info(f"Shared instance {instance_id} with user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to share instance {instance_id} with user {user_id}: {e}")
            return False
    
    async def execute_collaborative_task(
        self,
        workspace_id: str,
        user_id: str,
        task: Dict[str, Any],
        instance_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a task on a collaborative workspace instance"""
        try:
            # Get or create instance for workspace
            if not instance_id:
                instances = await self.get_workspace_instances(workspace_id)
                if instances:
                    instance_id = instances[0]['instance_id']
                else:
                    instance_id = await self.create_workspace_instance(
                        workspace_id, user_id
                    )
            
            if not instance_id:
                return {
                    'success': False,
                    'error': 'No available instance for workspace'
                }
            
            # Add workspace context to task
            task['workspace_context'] = {
                'workspace_id': workspace_id,
                'user_id': user_id,
                'instance_id': instance_id,
                'timestamp': datetime.now().isoformat()
            }
            
            # Execute task through Scrapybara
            result = await self.scrapybara.execute_autonomous_task(
                task_type='collaborative_task',
                parameters=task,
                instance_id=instance_id
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute collaborative task: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def cleanup_workspace_instances(self, workspace_id: str):
        """Clean up all instances for a workspace"""
        instance_ids = self.workspace_instances.get(workspace_id, [])
        
        for instance_id in instance_ids:
            try:
                await self.scrapybara.terminate_instance(instance_id)
            except Exception as e:
                logger.error(f"Failed to cleanup instance {instance_id}: {e}")
        
        # Clear tracking
        if workspace_id in self.workspace_instances:
            del self.workspace_instances[workspace_id]
        
        for instance_id in instance_ids:
            if instance_id in self.instance_workspaces:
                del self.instance_workspaces[instance_id]


class EnhancedCollaborativeIntegration:
    """
    Main integration class that combines all collaborative and cloud capabilities
    """
    
    def __init__(
        self,
        storage_path: str = "data/workspaces",
        scrapybara_config: Optional[Dict] = None
    ):
        # Initialize core components
        self.scrapybara = ScrapybaraIntegrationManager(scrapybara_config or {})
        self.workspace_manager = CollaborativeWorkspaceManager(
            self.scrapybara, storage_path
        )
        self.collaborative_scrapybara = CollaborativeScrapybaraManager(self.scrapybara)
        
        # Enhanced systems (assuming they exist from previous conversation)
        self.memory_system = None  # Will be set by main app
        self.orchestration_system = None  # Will be set by main app
        
        # Integration state
        self.active_collaborative_sessions: Dict[str, Dict] = {}
    
    async def initialize(self):
        """Initialize all components"""
        try:
            await self.scrapybara.initialize()
            logger.info("Enhanced collaborative integration initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize collaborative integration: {e}")
            raise
    
    def set_enhanced_systems(self, memory_system, orchestration_system):
        """Set enhanced memory and orchestration systems"""
        self.memory_system = memory_system
        self.orchestration_system = orchestration_system
    
    async def create_collaborative_workspace(
        self,
        name: str,
        owner_id: str,
        workspace_type: str = "hybrid",
        enable_scrapybara: bool = True,
        settings: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create a new collaborative workspace with optional cloud capabilities"""
        try:
            # Parse workspace type
            ws_type = WorkspaceType.HYBRID if workspace_type == "hybrid" else WorkspaceType(workspace_type)
            
            # Create workspace
            workspace = await self.workspace_manager.create_workspace(
                name=name,
                owner_id=owner_id,
                workspace_type=ws_type,
                collaboration_mode=CollaborationMode.SHARED,
                description=f"Collaborative workspace with {'cloud' if enable_scrapybara else 'local'} capabilities",
                settings=settings or {}
            )
            
            # Create Scrapybara instance if cloud enabled
            instance_id = None
            if enable_scrapybara and ws_type in [WorkspaceType.CLOUD, WorkspaceType.HYBRID]:
                instance_id = await self.collaborative_scrapybara.create_workspace_instance(
                    workspace.workspace_id,
                    owner_id,
                    instance_type="ubuntu",
                    shared=True
                )
            
            return {
                'success': True,
                'workspace': {
                    'workspace_id': workspace.workspace_id,
                    'name': workspace.name,
                    'type': workspace.workspace_type.value,
                    'owner_id': workspace.owner_id,
                    'created_at': workspace.created_at.isoformat(),
                    'scrapybara_instance_id': instance_id,
                    'cloud_enabled': instance_id is not None
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create collaborative workspace: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def join_collaborative_session(
        self,
        workspace_id: str,
        user_id: str,
        username: str
    ) -> Dict[str, Any]:
        """Join a collaborative session in a workspace"""
        try:
            # Add user to workspace if not already a member
            workspace = await self.workspace_manager.get_workspace(workspace_id)
            if not workspace:
                return {
                    'success': False,
                    'error': 'Workspace not found'
                }
            
            if user_id not in workspace.users:
                await self.workspace_manager.add_user_to_workspace(
                    workspace_id, user_id, username, WorkspaceRole.COLLABORATOR
                )
            
            # Create session
            session = await self.workspace_manager.create_session(workspace_id, user_id)
            if not session:
                return {
                    'success': False,
                    'error': 'Failed to create session'
                }
            
            # Get Scrapybara instances if available
            scrapybara_instances = []
            if workspace.workspace_type in [WorkspaceType.CLOUD, WorkspaceType.HYBRID]:
                scrapybara_instances = await self.collaborative_scrapybara.get_workspace_instances(workspace_id)
            
            # Track active session
            self.active_collaborative_sessions[session.session_id] = {
                'workspace_id': workspace_id,
                'user_id': user_id,
                'session': session,
                'scrapybara_instances': [inst['instance_id'] for inst in scrapybara_instances],
                'started_at': datetime.now()
            }
            
            return {
                'success': True,
                'session': {
                    'session_id': session.session_id,
                    'workspace_id': workspace_id,
                    'user_id': user_id,
                    'scrapybara_instances': scrapybara_instances,
                    'workspace_type': workspace.workspace_type.value,
                    'collaboration_mode': workspace.collaboration_mode.value
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to join collaborative session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def execute_collaborative_mama_bear_task(
        self,
        session_id: str,
        message: str,
        task_type: str = "autonomous_chat",
        use_scrapybara: bool = False
    ) -> Dict[str, Any]:
        """Execute a Mama Bear task in collaborative context"""
        try:
            session_info = self.active_collaborative_sessions.get(session_id)
            if not session_info:
                return {
                    'success': False,
                    'error': 'Invalid session'
                }
            
            workspace_id = session_info['workspace_id']
            user_id = session_info['user_id']
            
            # Prepare task context
            task_context = {
                'message': message,
                'user_id': user_id,
                'workspace_id': workspace_id,
                'session_id': session_id,
                'collaborative': True,
                'use_scrapybara': use_scrapybara
            }
            
            if use_scrapybara and session_info['scrapybara_instances']:
                # Execute with Scrapybara cloud capabilities
                result = await self.collaborative_scrapybara.execute_collaborative_task(
                    workspace_id=workspace_id,
                    user_id=user_id,
                    task={
                        'type': task_type,
                        'message': message,
                        'context': task_context
                    },
                    instance_id=session_info['scrapybara_instances'][0]
                )
            else:
                # Execute with local Mama Bear capabilities
                if self.orchestration_system:
                    # Correctly call process_autonomous_request with keyword arguments
                    result = await self.orchestration_system.process_autonomous_request(
                        message=task_context['message'],
                        user_id=task_context['user_id'],
                        session_id=task_context.get('session_id'), # session_id is optional
                        context=task_context # Pass the whole task_context as the context dict
                        # page_context will use its default from the method definition if not in task_context
                    )
                else:
                    # Fallback simple response
                    result = {
                        'success': True,
                        'response': f"Mama Bear local response to: {message}",
                        'type': 'local_mama_bear'
                    }
            
            # Share result as workspace resource
            if result.get('success'):
                await self.workspace_manager.share_resource(
                    workspace_id=workspace_id,
                    owner_id=user_id,
                    resource_type='mama_bear_response',
                    name=f"Response to: {message[:50]}...",
                    content=result,
                    description=f"Mama Bear response from {task_type} task"
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute collaborative Mama Bear task: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def share_mama_bear_session(
        self,
        session_id: str,
        target_user_id: str,
        permissions: List[str] = None
    ) -> Dict[str, Any]:
        """Share a Mama Bear session with another user"""
        try:
            session_info = self.active_collaborative_sessions.get(session_id)
            if not session_info:
                return {
                    'success': False,
                    'error': 'Invalid session'
                }
            
            workspace_id = session_info['workspace_id']
            
            # Add user to workspace
            await self.workspace_manager.add_user_to_workspace(
                workspace_id, target_user_id, f"user_{target_user_id}", WorkspaceRole.COLLABORATOR
            )
            
            # Share Scrapybara instances if available
            for instance_id in session_info['scrapybara_instances']:
                await self.collaborative_scrapybara.share_instance_with_user(
                    instance_id, target_user_id, permissions or ['read', 'execute']
                )
            
            return {
                'success': True,
                'message': f'Session shared with user {target_user_id}'
            }
            
        except Exception as e:
            logger.error(f"Failed to share Mama Bear session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_workspace_status(self, workspace_id: str) -> Dict[str, Any]:
        """Get comprehensive status of a collaborative workspace"""
        try:
            workspace = await self.workspace_manager.get_workspace(workspace_id)
            if not workspace:
                return {
                    'success': False,
                    'error': 'Workspace not found'
                }
            
            # Get active sessions
            active_sessions = []
            for session_id, session_info in self.active_collaborative_sessions.items():
                if session_info['workspace_id'] == workspace_id:
                    active_sessions.append({
                        'session_id': session_id,
                        'user_id': session_info['user_id'],
                        'started_at': session_info['started_at'].isoformat(),
                        'scrapybara_instances': session_info.get('scrapybara_instances', [])
                    })
            
            # Get Scrapybara instances if available
            scrapybara_instances = []
            if hasattr(self, 'collaborative_scrapybara'):
                scrapybara_instances = await self.collaborative_scrapybara.get_workspace_instances(workspace_id)
            
            return {
                'success': True,
                'workspace': {
                    'workspace_id': workspace.workspace_id,
                    'name': workspace.name,
                    'type': workspace.workspace_type.value,
                    'collaboration_mode': workspace.collaboration_mode.value,
                    'owner_id': workspace.owner_id,
                    'user_count': len(workspace.users),
                    'created_at': workspace.created_at.isoformat(),
                    'updated_at': workspace.updated_at.isoformat()
                },
                'active_sessions': active_sessions,
                'scrapybara_instances': scrapybara_instances,
                'shared_resources': len(workspace.shared_resources)
            }
            
        except Exception as e:
            logger.error(f"Failed to get workspace status: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def cleanup_session(self, session_id: str):
        """Clean up a collaborative session"""
        if session_id in self.active_collaborative_sessions:
            session_info = self.active_collaborative_sessions[session_id]
            logger.info(f"Cleaning up session {session_id} for workspace {session_info['workspace_id']}")
            del self.active_collaborative_sessions[session_id]
    
    async def shutdown(self):
        """Shutdown collaborative integration gracefully"""
        try:
            # Clean up active sessions
            for session_id in list(self.active_collaborative_sessions.keys()):
                del self.active_collaborative_sessions[session_id]
            
            # Clean up Scrapybara instances
            if hasattr(self, 'collaborative_scrapybara'):
                for workspace_id in list(self.collaborative_scrapybara.workspace_instances.keys()):
                    await self.collaborative_scrapybara.cleanup_workspace_instances(workspace_id)
            
            # Shutdown orchestration system if available
            if hasattr(self, 'orchestration_system') and self.orchestration_system:
                await self.orchestration_system.shutdown()
            
            logger.info("Collaborative integration shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during collaborative integration shutdown: {e}")

# Export main class
__all__ = ['EnhancedCollaborativeIntegration', 'CollaborativeScrapybaraManager']
