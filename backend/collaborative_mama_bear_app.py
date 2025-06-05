"""
🐻 Mama Bear Collaborative Flask Application
Complete Flask app with collaborative workspaces, Scrapybara cloud integration,
and real-time multi-user capabilities
"""

import asyncio
import logging
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Import our collaborative components
from services.enhanced_collaborative_integration import EnhancedCollaborativeIntegration
from api.collaborative_workspace_api import (
    collaborative_bp,
    initialize_collaborative_api
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CollaborativeMamaBearApp:
    """Main Flask application for collaborative Mama Bear system"""
    
    def __init__(self, config=None):
        self.app = Flask(__name__)
        self.socketio = SocketIO(
            self.app,
            cors_allowed_origins="*",
            async_mode='threading'
        )
        
        # Enable CORS
        CORS(self.app)
        
        # Configuration
        self.config = config or {}
        self._configure_app()
        
        # Core components
        self.collaborative_integration = None
        self.collaborative_api = None
        
        # Initialize components
        asyncio.create_task(self._initialize_components())
        
        # Register routes and handlers
        self._register_routes()
        self._register_websocket_handlers()
    
    def _configure_app(self):
        """Configure Flask app"""
        self.app.config.update({
            'SECRET_KEY': os.getenv('SECRET_KEY', 'mama-bear-collaborative-secret'),
            'SCRAPYBARA_API_KEY': os.getenv('SCRAPYBARA_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            **self.config
        })
    
    async def _initialize_components(self):
        """Initialize all collaborative components"""
        try:
            # Initialize collaborative integration
            scrapybara_config = {
                'api_key': self.app.config.get('SCRAPYBARA_API_KEY'),
                'default_timeout_hours': 2,
                'max_instances': 10,
                'enable_browser_auth': True,
                'model_fallback_chain': ['scrapybara_credits', 'gemini', 'anthropic', 'openai'],
                'model_configs': {
                    'gemini': {
                        'api_key': self.app.config.get('GOOGLE_API_KEY'),
                        'model_name': 'gemini-1.5-pro'
                    },
                    'anthropic': {
                        'api_key': self.app.config.get('ANTHROPIC_API_KEY'),
                        'model_name': 'claude-3-5-sonnet-20241022'
                    },
                    'openai': {
                        'api_key': self.app.config.get('OPENAI_API_KEY'),
                        'model_name': 'gpt-4o'
                    }
                }
            }
            
            self.collaborative_integration = EnhancedCollaborativeIntegration(
                storage_path="data/collaborative_workspaces",
                scrapybara_config=scrapybara_config
            )
            
            await self.collaborative_integration.initialize()
            
            # Initialize collaborative API
            self.collaborative_api = initialize_collaborative_api(
                self.collaborative_integration.workspace_manager,
                self.socketio
            )
            
            # Store components in app config for access
            self.app.config['collaborative_integration'] = self.collaborative_integration
            self.app.config['collaborative_api'] = self.collaborative_api
            
            logger.info("Collaborative Mama Bear app initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize collaborative components: {e}")
            raise
    
    def _register_routes(self):
        """Register all Flask routes"""
        
        # Register collaborative workspace blueprint
        self.app.register_blueprint(collaborative_bp)
        
        # Health check endpoint
        @self.app.route('/health')
        def health_check():
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'features': {
                    'collaborative_workspaces': True,
                    'scrapybara_integration': True,
                    'real_time_collaboration': True,
                    'cloud_sync': True
                }
            })
        
        # Enhanced autonomous chat with collaborative context
        @self.app.route('/api/collaborative/chat', methods=['POST'])
        async def collaborative_chat():
            try:
                data = request.json
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid JSON payload'
                    }), 400
                
                session_id = data.get('session_id')
                message = data.get('message', '')
                use_scrapybara = data.get('use_scrapybara', False)
                task_type = data.get('task_type', 'autonomous_chat')
                
                if not session_id or not message:
                    return jsonify({
                        'success': False,
                        'error': 'session_id and message are required'
                    }), 400
                
                # Execute collaborative task
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                result = await integration.execute_collaborative_mama_bear_task(
                    session_id=session_id,
                    message=message,
                    task_type=task_type,
                    use_scrapybara=use_scrapybara
                )
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Collaborative chat error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
        
        # Create collaborative workspace with Scrapybara
        @self.app.route('/api/collaborative/workspaces/create', methods=['POST'])
        async def create_collaborative_workspace():
            try:
                data = request.json
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid JSON payload'
                    }), 400
                
                name = data.get('name', '')
                owner_id = data.get('owner_id', '')
                workspace_type = data.get('type', 'hybrid')
                enable_scrapybara = data.get('enable_scrapybara', True)
                settings = data.get('settings', {})
                
                if not name or not owner_id:
                    return jsonify({
                        'success': False,
                        'error': 'name and owner_id are required'
                    }), 400
                
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                result = await integration.create_collaborative_workspace(
                    name=name,
                    owner_id=owner_id,
                    workspace_type=workspace_type,
                    enable_scrapybara=enable_scrapybara,
                    settings=settings
                )
                
                status_code = 201 if result['success'] else 400
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Create collaborative workspace error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
        
        # Join collaborative session
        @self.app.route('/api/collaborative/sessions/join', methods=['POST'])
        async def join_collaborative_session():
            try:
                data = request.json
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid JSON payload'
                    }), 400
                
                workspace_id = data.get('workspace_id', '')
                user_id = data.get('user_id', '')
                username = data.get('username', '')
                
                if not all([workspace_id, user_id, username]):
                    return jsonify({
                        'success': False,
                        'error': 'workspace_id, user_id, and username are required'
                    }), 400
                
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                result = await integration.join_collaborative_session(
                    workspace_id=workspace_id,
                    user_id=user_id,
                    username=username
                )
                
                status_code = 200 if result['success'] else 400
                return jsonify(result), status_code
                
            except Exception as e:
                logger.error(f"Join collaborative session error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
        
        # Share Mama Bear session
        @self.app.route('/api/collaborative/sessions/<session_id>/share', methods=['POST'])
        async def share_mama_bear_session(session_id: str):
            try:
                data = request.json
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid JSON payload'
                    }), 400
                
                target_user_id = data.get('target_user_id', '')
                permissions = data.get('permissions', ['read', 'execute'])
                
                if not target_user_id:
                    return jsonify({
                        'success': False,
                        'error': 'target_user_id is required'
                    }), 400
                
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                result = await integration.share_mama_bear_session(
                    session_id=session_id,
                    target_user_id=target_user_id,
                    permissions=permissions
                )
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Share session error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
        
        # Get workspace status
        @self.app.route('/api/collaborative/workspaces/<workspace_id>/status', methods=['GET'])
        async def get_workspace_status(workspace_id: str):
            try:
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                result = await integration.get_workspace_status(workspace_id)
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Get workspace status error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
        
        # Scrapybara integration endpoints
        @self.app.route('/api/collaborative/scrapybara/instances', methods=['GET'])
        async def get_scrapybara_instances():
            try:
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                workspace_id = request.args.get('workspace_id')
                if workspace_id and hasattr(integration, 'collaborative_scrapybara'):
                    instances = await integration.collaborative_scrapybara.get_workspace_instances(workspace_id)
                elif hasattr(integration, 'scrapybara'):
                    # Get all instances
                    instances = await integration.scrapybara.list_instances()
                else:
                    instances = []
                
                return jsonify({
                    'success': True,
                    'instances': instances
                })
                
            except Exception as e:
                logger.error(f"Get Scrapybara instances error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
        
        @self.app.route('/api/collaborative/scrapybara/execute', methods=['POST'])
        async def execute_scrapybara_task():
            try:
                data = request.json
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid JSON payload'
                    }), 400
                
                workspace_id = data.get('workspace_id')
                user_id = data.get('user_id')
                task = data.get('task', {})
                instance_id = data.get('instance_id')
                
                if not all([workspace_id, user_id, task]):
                    return jsonify({
                        'success': False,
                        'error': 'workspace_id, user_id, and task are required'
                    }), 400
                
                integration = self.app.config.get('collaborative_integration')
                if not integration:
                    return jsonify({
                        'success': False,
                        'error': 'Integration not initialized'
                    }), 500
                
                if not hasattr(integration, 'collaborative_scrapybara'):
                    return jsonify({
                        'success': False,
                        'error': 'Scrapybara integration not available'
                    }), 500
                
                result = await integration.collaborative_scrapybara.execute_collaborative_task(
                    workspace_id=workspace_id,
                    user_id=user_id,
                    task=task,
                    instance_id=instance_id
                )
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Execute Scrapybara task error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Internal server error'
                }), 500
    
    def _register_websocket_handlers(self):
        """Register WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            from flask import session
            session_id = session.get('sid') or 'anonymous'
            logger.info(f"Client connected: {session_id}")
            emit('connected', {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            from flask import session
            session_id = session.get('sid') or 'anonymous'
            logger.info(f"Client disconnected: {session_id}")
        
        @self.socketio.on('collaborative_chat')
        async def handle_collaborative_chat(data):
            """Handle collaborative chat messages"""
            try:
                session_id = data.get('session_id')
                message = data.get('message')
                use_scrapybara = data.get('use_scrapybara', False)
                
                if session_id and message:
                    # Execute collaborative task
                    integration = self.app.config.get('collaborative_integration')
                    if integration:
                        result = await integration.execute_collaborative_mama_bear_task(
                            session_id=session_id,
                            message=message,
                            use_scrapybara=use_scrapybara
                        )
                        
                        # Emit response to the specific session
                        emit('collaborative_response', result)
                        
                        # Also broadcast to workspace if successful
                        if result.get('success') and hasattr(integration, 'active_collaborative_sessions'):
                            session_info = integration.active_collaborative_sessions.get(session_id)
                            if session_info:
                                workspace_id = session_info['workspace_id']
                                emit('workspace_activity', {
                                    'type': 'mama_bear_response',
                                    'workspace_id': workspace_id,
                                    'user_id': session_info['user_id'],
                                    'data': result,
                                    'timestamp': datetime.now().isoformat()
                                }, to=f"workspace_{workspace_id}")
                    else:
                        emit('error', {'error': 'Integration not initialized'})
                
            except Exception as e:
                logger.error(f"Collaborative chat WebSocket error: {e}")
                emit('error', {'error': str(e)})
        
        @self.socketio.on('scrapybara_command')
        async def handle_scrapybara_command(data):
            """Handle direct Scrapybara commands"""
            try:
                workspace_id = data.get('workspace_id')
                user_id = data.get('user_id')
                command = data.get('command')
                instance_id = data.get('instance_id')
                
                if all([workspace_id, user_id, command]):
                    integration = self.app.config.get('collaborative_integration')
                    if integration and hasattr(integration, 'collaborative_scrapybara'):
                        result = await integration.collaborative_scrapybara.execute_collaborative_task(
                            workspace_id=workspace_id,
                            user_id=user_id,
                            task={
                                'type': 'direct_command',
                                'command': command
                            },
                            instance_id=instance_id
                        )
                        
                        emit('scrapybara_result', result)
                        
                        # Broadcast to workspace
                        emit('workspace_activity', {
                            'type': 'scrapybara_command',
                            'workspace_id': workspace_id,
                            'user_id': user_id,
                            'command': command,
                            'result': result,
                            'timestamp': datetime.now().isoformat()
                        }, to=f"workspace_{workspace_id}")
                    else:
                        emit('error', {'error': 'Scrapybara integration not available'})
                
            except Exception as e:
                logger.error(f"Scrapybara command WebSocket error: {e}")
                emit('error', {'error': str(e)})
        
        @self.socketio.on('request_screen_share')
        async def handle_screen_share_request(data):
            """Handle screen sharing requests for Scrapybara instances"""
            try:
                workspace_id = data.get('workspace_id')
                instance_id = data.get('instance_id')
                user_id = data.get('user_id')
                
                if all([workspace_id, instance_id, user_id]):
                    integration = self.app.config.get('collaborative_integration')
                    if integration and hasattr(integration, 'scrapybara'):
                        # Get instance screenshot
                        screenshot = await integration.scrapybara.take_screenshot(instance_id)
                        
                        if screenshot:
                            emit('screen_share_data', {
                                'workspace_id': workspace_id,
                                'instance_id': instance_id,
                                'screenshot': screenshot,
                                'timestamp': datetime.now().isoformat()
                            })
                            
                            # Broadcast to workspace
                            emit('workspace_activity', {
                                'type': 'screen_share',
                                'workspace_id': workspace_id,
                                'user_id': user_id,
                                'instance_id': instance_id,
                                'timestamp': datetime.now().isoformat()
                            }, to=f"workspace_{workspace_id}")
                    else:
                        emit('error', {'error': 'Screenshot capability not available'})
                
            except Exception as e:
                logger.error(f"Screen share WebSocket error: {e}")
                emit('error', {'error': str(e)})
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the Flask application"""
        logger.info(f"Starting Collaborative Mama Bear app on {host}:{port}")
        self.socketio.run(
            self.app,
            host=host,
            port=port,
            debug=debug,
            allow_unsafe_werkzeug=True
        )
    
    async def shutdown(self):
        """Shutdown the application gracefully"""
        if self.collaborative_integration:
            await self.collaborative_integration.shutdown()


# Factory function to create app
def create_app(config=None):
    """Factory function to create Flask app"""
    return CollaborativeMamaBearApp(config)


# Main execution
if __name__ == '__main__':
    import sys
    
    # Configuration
    config = {
        'DEBUG': '--debug' in sys.argv,
        'HOST': os.getenv('HOST', '0.0.0.0'),
        'PORT': int(os.getenv('PORT', 5000))
    }
    
    # Create and run app
    app = create_app(config)
    app.run(
        host=config['HOST'],
        port=config['PORT'],
        debug=config['DEBUG']
    )
