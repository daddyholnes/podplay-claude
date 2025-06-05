"""
🐻 Collaborative Workspace API
REST and WebSocket endpoints for multi-user collaborative workspaces
with cloud Scrapybara and local storage integration
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room, disconnect, SocketIO

from services.collaborative_workspace import (
    CollaborativeWorkspaceManager,
    WorkspaceType,
    CollaborationMode,
    WorkspaceRole
)

logger = logging.getLogger(__name__)

# Create collaborative workspace blueprint
collaborative_bp = Blueprint('collaborative', __name__)


class CollaborativeWorkspaceAPI:
    """API handler for collaborative workspace operations"""
    
    def __init__(self, workspace_manager: CollaborativeWorkspaceManager, socketio: SocketIO):
        self.workspace_manager = workspace_manager
        self.socketio = socketio
        self.active_connections: Dict[str, List[str]] = {}  # workspace_id -> [session_ids]
        
        # Register event callbacks for real-time updates
        self._register_workspace_events()
    
    def _register_workspace_events(self):
        """Register callbacks for workspace events to broadcast via WebSocket"""
        
        async def on_user_joined(data):
            await self._broadcast_to_workspace(
                data['workspace_id'],
                'user_joined',
                data
            )
        
        async def on_user_left(data):
            await self._broadcast_to_workspace(
                data['workspace_id'],
                'user_left',
                data
            )
        
        async def on_resource_shared(data):
            await self._broadcast_to_workspace(
                data['workspace_id'],
                'resource_shared',
                data
            )
        
        async def on_resource_updated(data):
            await self._broadcast_to_workspace(
                data['workspace_id'],
                'resource_updated',
                data
            )
        
        self.workspace_manager.register_event_callback('user_joined', on_user_joined)
        self.workspace_manager.register_event_callback('user_left', on_user_left)
        self.workspace_manager.register_event_callback('resource_shared', on_resource_shared)
        self.workspace_manager.register_event_callback('resource_updated', on_resource_updated)
    
    async def _broadcast_to_workspace(self, workspace_id: str, event: str, data: Dict):
        """Broadcast event to all users in a workspace"""
        room = f"workspace_{workspace_id}"
        self.socketio.emit(event, data, to=room)
    
    # REST API Methods
    
    async def create_workspace(self, data: Dict) -> Dict[str, Any]:
        """Create a new collaborative workspace"""
        try:
            name = data.get('name', '')
            owner_id = data.get('owner_id', '')
            workspace_type = WorkspaceType(data.get('type', 'local'))
            collaboration_mode = CollaborationMode(data.get('collaboration_mode', 'solo'))
            description = data.get('description', '')
            settings = data.get('settings', {})
            
            if not name or not owner_id:
                return {
                    'success': False,
                    'error': 'Name and owner_id are required'
                }
            
            workspace = await self.workspace_manager.create_workspace(
                name=name,
                owner_id=owner_id,
                workspace_type=workspace_type,
                collaboration_mode=collaboration_mode,
                description=description,
                settings=settings
            )
            
            return {
                'success': True,
                'workspace': {
                    'workspace_id': workspace.workspace_id,
                    'name': workspace.name,
                    'description': workspace.description,
                    'type': workspace.workspace_type.value,
                    'collaboration_mode': workspace.collaboration_mode.value,
                    'owner_id': workspace.owner_id,
                    'created_at': workspace.created_at.isoformat(),
                    'user_count': len(workspace.users),
                    'settings': workspace.settings
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create workspace: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_workspace(self, workspace_id: str, user_id: str) -> Dict[str, Any]:
        """Get workspace details for a user"""
        try:
            workspace = await self.workspace_manager.get_workspace(workspace_id)
            if not workspace:
                return {
                    'success': False,
                    'error': 'Workspace not found'
                }
            
            # Check if user has access
            if user_id not in workspace.users:
                return {
                    'success': False,
                    'error': 'Access denied'
                }
            
            user = workspace.users[user_id]
            
            return {
                'success': True,
                'workspace': {
                    'workspace_id': workspace.workspace_id,
                    'name': workspace.name,
                    'description': workspace.description,
                    'type': workspace.workspace_type.value,
                    'collaboration_mode': workspace.collaboration_mode.value,
                    'owner_id': workspace.owner_id,
                    'created_at': workspace.created_at.isoformat(),
                    'updated_at': workspace.updated_at.isoformat(),
                    'users': [
                        {
                            'user_id': u.user_id,
                            'username': u.username,
                            'role': u.role.value,
                            'last_active': u.last_active.isoformat()
                        }
                        for u in workspace.users.values()
                    ],
                    'active_sessions': len(workspace.active_sessions),
                    'shared_resources': [
                        {
                            'resource_id': r.resource_id,
                            'type': r.resource_type,
                            'name': r.name,
                            'description': r.description,
                            'owner_id': r.owner_id,
                            'created_at': r.created_at.isoformat(),
                            'updated_at': r.updated_at.isoformat()
                        }
                        for r in workspace.shared_resources.values()
                    ],
                    'user_role': user.role.value,
                    'user_permissions': user.permissions,
                    'settings': workspace.settings
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get workspace {workspace_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def join_workspace(self, workspace_id: str, user_id: str, username: str, invitation_code: Optional[str] = None) -> Dict[str, Any]:
        """Join a workspace"""
        try:
            # TODO: Implement invitation code validation if needed
            
            success = await self.workspace_manager.add_user_to_workspace(
                workspace_id=workspace_id,
                user_id=user_id,
                username=username,
                role=WorkspaceRole.COLLABORATOR
            )
            
            if success:
                return {
                    'success': True,
                    'message': f'Successfully joined workspace {workspace_id}'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to join workspace'
                }
                
        except Exception as e:
            logger.error(f"Failed to join workspace {workspace_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def share_resource(self, data: Dict) -> Dict[str, Any]:
        """Share a resource in the workspace"""
        try:
            workspace_id = data.get('workspace_id', '')
            owner_id = data.get('owner_id', '')
            resource_type = data.get('resource_type', '')
            name = data.get('name', '')
            content = data.get('content')
            description = data.get('description', '')
            permissions = data.get('permissions', {})
            
            if not all([workspace_id, owner_id, resource_type, name]):
                return {
                    'success': False,
                    'error': 'Missing required fields'
                }
            
            resource = await self.workspace_manager.share_resource(
                workspace_id=workspace_id,
                owner_id=owner_id,
                resource_type=resource_type,
                name=name,
                content=content,
                description=description,
                permissions=permissions
            )
            
            if resource:
                return {
                    'success': True,
                    'resource': {
                        'resource_id': resource.resource_id,
                        'type': resource.resource_type,
                        'name': resource.name,
                        'description': resource.description,
                        'owner_id': resource.owner_id,
                        'created_at': resource.created_at.isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to share resource'
                }
                
        except Exception as e:
            logger.error(f"Failed to share resource: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_user_workspaces(self, user_id: str) -> Dict[str, Any]:
        """Get all workspaces for a user"""
        try:
            workspaces = await self.workspace_manager.get_user_workspaces(user_id)
            
            return {
                'success': True,
                'workspaces': [
                    {
                        'workspace_id': w.workspace_id,
                        'name': w.name,
                        'description': w.description,
                        'type': w.workspace_type.value,
                        'collaboration_mode': w.collaboration_mode.value,
                        'owner_id': w.owner_id,
                        'created_at': w.created_at.isoformat(),
                        'user_role': w.users[user_id].role.value if user_id in w.users else 'unknown',
                        'user_count': len(w.users),
                        'active_sessions': len(w.active_sessions)
                    }
                    for w in workspaces
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get workspaces for user {user_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def start_session(self, workspace_id: str, user_id: str) -> Dict[str, Any]:
        """Start a new session in a workspace"""
        try:
            session = await self.workspace_manager.create_session(
                workspace_id=workspace_id,
                user_id=user_id
            )
            
            if session:
                return {
                    'success': True,
                    'session': {
                        'session_id': session.session_id,
                        'workspace_id': session.workspace_id,
                        'user_id': session.user_id,
                        'started_at': session.started_at.isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to start session'
                }
                
        except Exception as e:
            logger.error(f"Failed to start session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    # WebSocket event handlers
    
    def handle_join_workspace_room(self, data: Dict, session_id: str):
        """Handle user joining workspace WebSocket room"""
        workspace_id = data.get('workspace_id')
        user_id = data.get('user_id')
        
        if workspace_id and user_id:
            room = f"workspace_{workspace_id}"
            join_room(room)
            
            # Track connection
            if workspace_id not in self.active_connections:
                self.active_connections[workspace_id] = []
            self.active_connections[workspace_id].append(session_id)
            
            emit('joined_room', {
                'workspace_id': workspace_id,
                'room': room,
                'timestamp': datetime.now().isoformat()
            })
    
    def handle_leave_workspace_room(self, data: Dict, session_id: str):
        """Handle user leaving workspace WebSocket room"""
        workspace_id = data.get('workspace_id')
        
        if workspace_id:
            room = f"workspace_{workspace_id}"
            leave_room(room)
            
            # Remove connection tracking
            if workspace_id in self.active_connections:
                if session_id in self.active_connections[workspace_id]:
                    self.active_connections[workspace_id].remove(session_id)
            
            emit('left_room', {
                'workspace_id': workspace_id,
                'room': room,
                'timestamp': datetime.now().isoformat()
            })
    
    def handle_workspace_activity(self, data: Dict):
        """Handle workspace activity updates"""
        workspace_id = data.get('workspace_id')
        activity_type = data.get('activity_type')
        user_id = data.get('user_id')
        
        if workspace_id and activity_type:
            # Broadcast activity to workspace room
            room = f"workspace_{workspace_id}"
            emit('workspace_activity', {
                'workspace_id': workspace_id,
                'activity_type': activity_type,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'data': data.get('activity_data', {})
            }, to=room)
    
    def handle_share_screen(self, data: Dict):
        """Handle screen sharing in workspace"""
        workspace_id = data.get('workspace_id')
        user_id = data.get('user_id')
        
        if workspace_id and user_id:
            room = f"workspace_{workspace_id}"
            emit('screen_share_started', {
                'workspace_id': workspace_id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            }, to=room)
    
    def handle_cursor_update(self, data: Dict):
        """Handle cursor position updates for collaborative editing"""
        workspace_id = data.get('workspace_id')
        user_id = data.get('user_id')
        cursor_position = data.get('cursor_position')
        
        if workspace_id and user_id and cursor_position:
            room = f"workspace_{workspace_id}"
            emit('cursor_update', {
                'workspace_id': workspace_id,
                'user_id': user_id,
                'cursor_position': cursor_position,
                'timestamp': datetime.now().isoformat()
            }, to=room, include_self=False)


# Initialize API handler (will be set when app starts)
collaborative_api = None


# REST API Routes

@collaborative_bp.route('/api/workspaces', methods=['POST'])
async def create_workspace():
    """Create a new collaborative workspace"""
    if collaborative_api is None:
        logger.error("Collaborative API not initialized")
        return jsonify({'success': False, 'error': 'Service not available. API not initialized.'}), 503
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        result = await collaborative_api.create_workspace(data)
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Create workspace endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@collaborative_bp.route('/api/workspaces/<workspace_id>', methods=['GET'])
async def get_workspace(workspace_id: str):
    """Get workspace details"""
    if collaborative_api is None:
        logger.error("Collaborative API not initialized")
        return jsonify({'success': False, 'error': 'Service not available. API not initialized.'}), 503
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id parameter required'
            }), 400
        
        result = await collaborative_api.get_workspace(workspace_id, user_id)
        status_code = 200 if result['success'] else 404
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Get workspace endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@collaborative_bp.route('/api/workspaces/<workspace_id>/join', methods=['POST'])
async def join_workspace(workspace_id: str):
    """Join a workspace"""
    if collaborative_api is None:
        logger.error("Collaborative API not initialized")
        return jsonify({'success': False, 'error': 'Service not available. API not initialized.'}), 503
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        user_id = data.get('user_id')
        username = data.get('username')
        invitation_code = data.get('invitation_code')
        
        if not user_id or not username:
            return jsonify({
                'success': False,
                'error': 'user_id and username are required'
            }), 400
        
        result = await collaborative_api.join_workspace(
            workspace_id, user_id, username, invitation_code
        )
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Join workspace endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@collaborative_bp.route('/api/workspaces/<workspace_id>/resources', methods=['POST'])
async def share_resource(workspace_id: str):
    """Share a resource in the workspace"""
    if collaborative_api is None:
        logger.error("Collaborative API not initialized")
        return jsonify({'success': False, 'error': 'Service not available. API not initialized.'}), 503
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        data['workspace_id'] = workspace_id
        result = await collaborative_api.share_resource(data)
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Share resource endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@collaborative_bp.route('/api/users/<user_id>/workspaces', methods=['GET'])
async def get_user_workspaces(user_id: str):
    """Get all workspaces for a user"""
    if collaborative_api is None:
        logger.error("Collaborative API not initialized")
        return jsonify({'success': False, 'error': 'Service not available. API not initialized.'}), 503
    try:
        result = await collaborative_api.get_user_workspaces(user_id)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Get user workspaces endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@collaborative_bp.route('/api/workspaces/<workspace_id>/sessions', methods=['POST'])
async def start_session(workspace_id: str):
    """Start a new session in a workspace"""
    if collaborative_api is None:
        logger.error("Collaborative API not initialized")
        return jsonify({'success': False, 'error': 'Service not available. API not initialized.'}), 503
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        result = await collaborative_api.start_session(workspace_id, user_id)
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Start session endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


# WebSocket Event Handlers (to be registered with SocketIO)

def register_websocket_handlers(socketio: SocketIO):
    """Register WebSocket event handlers"""
    
    @socketio.on('join_workspace')
    def handle_join_workspace(data):
        """Handle joining workspace room"""
        from flask import session
        session_id = session.get('sid', 'anonymous')
        if collaborative_api is None:
            emit('error', {'message': 'Collaborative API not initialized'})
            return
        collaborative_api.handle_join_workspace_room(data, session_id)
    
    @socketio.on('leave_workspace')
    def handle_leave_workspace(data):
        """Handle leaving workspace room"""
        from flask import session
        session_id = session.get('sid', 'anonymous')
        if collaborative_api is None:
            emit('error', {'message': 'Collaborative API not initialized'})
            return
        collaborative_api.handle_leave_workspace_room(data, session_id)
    
    @socketio.on('workspace_activity')
    def handle_activity(data):
        """Handle workspace activity"""
        if collaborative_api is None:
            emit('error', {'message': 'Collaborative API not initialized'})
            return
        collaborative_api.handle_workspace_activity(data)
    
    @socketio.on('share_screen')
    def handle_screen_share(data):
        """Handle screen sharing"""
        if collaborative_api is None:
            emit('error', {'message': 'Collaborative API not initialized'})
            return
        collaborative_api.handle_share_screen(data)
    
    @socketio.on('cursor_update')
    def handle_cursor(data):
        """Handle cursor updates"""
        if collaborative_api is None:
            emit('error', {'message': 'Collaborative API not initialized'})
            return
        collaborative_api.handle_cursor_update(data)
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle user disconnect"""
        from flask import session
        session_id = session.get('sid', 'anonymous')
        logger.info(f"User disconnected: {session_id}")


def initialize_collaborative_api(workspace_manager: CollaborativeWorkspaceManager, socketio: SocketIO):
    """Initialize the collaborative API with workspace manager and SocketIO"""
    global collaborative_api
    collaborative_api = CollaborativeWorkspaceAPI(workspace_manager, socketio)
    register_websocket_handlers(socketio)
    return collaborative_api
