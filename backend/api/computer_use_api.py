"""
Flask API for Scrapybara Computer Use Integration
Provides REST endpoints for autonomous computer use operations
"""

from flask import Flask, request, jsonify, Blueprint
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room
import asyncio
import logging
import json
from typing import Dict, Any, Optional
import os
from functools import wraps

from services.enhanced_scrapybara_orchestration import (
    create_enhanced_orchestrator,
    execute_predefined_workflow,
    AUTONOMOUS_WORKFLOWS,
    InstanceType
)


# Create Blueprint for computer use API
computer_use_bp = Blueprint('computer_use', __name__, url_prefix='/api/computer-use')

# Global orchestrator instance
orchestrator = None


def init_computer_use_api(app: Flask, socketio: Optional[SocketIO] = None, mama_bear_orchestrator=None):
    """Initialize computer use API with Flask app"""
    global orchestrator
    
    # Create enhanced orchestrator
    orchestrator = create_enhanced_orchestrator(
        mama_bear_orchestrator=mama_bear_orchestrator,
        scrapybara_api_key=os.getenv('SCRAPYBARA_API_KEY'),
        max_instances=int(os.getenv('SCRAPYBARA_MAX_INSTANCES', '3')),
        timeout_hours=int(os.getenv('SCRAPYBARA_TIMEOUT_HOURS', '2'))
    )
    
    # Register blueprint
    app.register_blueprint(computer_use_bp)
    
    # Register WebSocket handlers if SocketIO available
    if socketio:
        register_websocket_handlers(socketio)
    
    logging.info("Computer Use API initialized")


def async_route(f):
    """Decorator to handle async routes in Flask"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Run async function in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(f(*args, **kwargs))
        except Exception as e:
            logging.error(f"Async route error: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            loop.close()
    
    return decorated_function


@computer_use_bp.route('/status', methods=['GET'])
def get_system_status():
    """Get system status and capabilities"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    status = orchestrator.get_system_status()
    return jsonify(status)


@computer_use_bp.route('/execute', methods=['POST'])
@async_route
async def execute_task():
    """Execute autonomous computer use task"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({"error": "Task description required"}), 400
    
    description = data['description']
    context = data.get('context', {})
    force_handler = data.get('force_handler')
    
    try:
        if not orchestrator:  # Double-check orchestrator right before use
            raise ValueError("Orchestrator became unavailable")
            
        result = await orchestrator.execute_autonomous_task(
            description=description,
            context=context,
            force_handler=force_handler
        )
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Task execution error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/workflows', methods=['GET'])
def list_workflows():
    """List available predefined workflows"""
    return jsonify({
        "workflows": list(AUTONOMOUS_WORKFLOWS.keys()),
        "workflow_definitions": AUTONOMOUS_WORKFLOWS
    })


@computer_use_bp.route('/workflows/<workflow_name>', methods=['POST'])
@async_route
async def execute_workflow(workflow_name):
    """Execute predefined workflow"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    if workflow_name not in AUTONOMOUS_WORKFLOWS:
        return jsonify({"error": f"Unknown workflow: {workflow_name}"}), 404
    
    data = request.get_json() or {}
    context = data.get('context', {})
    
    try:
        if not orchestrator:  # Double-check orchestrator right before use
            raise ValueError("Orchestrator became unavailable")
            
        result = await execute_predefined_workflow(
            orchestrator=orchestrator,  # Pass as named argument
            workflow_name=workflow_name, 
            context=context
        )
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Workflow execution error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/multi-step', methods=['POST'])
@async_route
async def execute_multi_step():
    """Execute multi-step workflow"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    data = request.get_json()
    if not data or 'steps' not in data:
        return jsonify({"error": "Workflow steps required"}), 400
    
    steps = data['steps']
    context = data.get('context', {})
    
    if not isinstance(steps, list) or not steps:
        return jsonify({"error": "Steps must be a non-empty list"}), 400
    
    try:
        result = await orchestrator.execute_multi_step_workflow(
            workflow_steps=steps,
            context=context
        )
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Multi-step execution error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/sessions', methods=['POST'])
@async_route
async def create_session():
    """Create persistent computer use session"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    data = request.get_json()
    if not data or 'session_name' not in data:
        return jsonify({"error": "Session name required"}), 400
    
    session_name = data['session_name']
    instance_type_str = data.get('instance_type', 'ubuntu')
    timeout_hours = data.get('timeout_hours', 2)
    
    try:
        instance_type = InstanceType(instance_type_str)
    except ValueError:
        return jsonify({"error": f"Invalid instance type: {instance_type_str}"}), 400
    
    try:
        result = await orchestrator.create_computer_use_session(
            session_name=session_name,
            instance_type=instance_type,
            timeout_hours=timeout_hours
        )
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Session creation error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/sessions/<instance_id>/status', methods=['GET'])
def get_session_status(instance_id):
    """Get session status"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    status = orchestrator.scrapybara.manager.get_instance_status(instance_id)
    return jsonify(status)


@computer_use_bp.route('/sessions/<instance_id>/stop', methods=['POST'])
@async_route
async def stop_session(instance_id):
    """Stop session"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    try:
        success = await orchestrator.scrapybara.manager.stop_instance(instance_id)
        return jsonify({"success": success})
        
    except Exception as e:
        logging.error(f"Session stop error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/sessions/<instance_id>/auth/save', methods=['POST'])
@async_route
async def save_auth_state(instance_id):
    """Save browser authentication state"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    data = request.get_json() or {}
    auth_name = data.get('name', 'default')
    
    try:
        auth_state_id = await orchestrator.save_browser_auth(instance_id, auth_name)
        
        if auth_state_id:
            return jsonify({"auth_state_id": auth_state_id, "name": auth_name})
        else:
            return jsonify({"error": "Failed to save auth state"}), 500
            
    except Exception as e:
        logging.error(f"Auth save error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/sessions/<instance_id>/auth/load', methods=['POST'])
@async_route
async def load_auth_state(instance_id):
    """Load browser authentication state"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    data = request.get_json()
    if not data or 'auth_state_id' not in data:
        return jsonify({"error": "Auth state ID required"}), 400
    
    auth_state_id = data['auth_state_id']
    
    try:
        success = await orchestrator.load_browser_auth(instance_id, auth_state_id)
        return jsonify({"success": success})
        
    except Exception as e:
        logging.error(f"Auth load error: {e}")
        return jsonify({"error": str(e)}), 500


@computer_use_bp.route('/instances', methods=['GET'])
def list_instances():
    """List all active instances"""
    if not orchestrator:
        return jsonify({"error": "Computer use system not initialized"}), 503
    
    status = orchestrator.scrapybara.manager.get_instance_status()
    return jsonify(status)


@computer_use_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if not orchestrator:
        return jsonify({"status": "error", "message": "Computer use system not initialized"}), 503
    
    capabilities = orchestrator.scrapybara.get_system_capabilities()
    
    return jsonify({
        "status": "healthy",
        "scrapybara_available": capabilities["scrapybara_available"],
        "gemini_available": capabilities["gemini_available"],
        "active_instances": capabilities["current_instances"],
        "model_providers": capabilities["model_providers"]
    })


# WebSocket handlers for real-time communication
def register_websocket_handlers(socketio: SocketIO) -> None:
    """Register WebSocket event handlers for computer use API"""
    
    @socketio.on('connect', namespace='/computer-use')
    def handle_connect():
        if not orchestrator:
            disconnect()
            return False
        return True
    
    @socketio.on('join_session', namespace='/computer-use')
    def handle_join_session(data):
        session_id = data.get('session_id')
        if not session_id:
            return False
        join_room(f"session_{session_id}")
        return True
        
    @socketio.on('leave_session', namespace='/computer-use')
    def handle_leave_session(data):
        session_id = data.get('session_id')
        if session_id:
            leave_room(f"session_{session_id}")
        return True
        
    @socketio.on('disconnect', namespace='/computer-use')
    def handle_disconnect():
        pass  # Handle any cleanup needed


# Example Flask app integration
def create_computer_use_app(mama_bear_orchestrator=None):
    """Create Flask app with computer use capabilities"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'computer-use-secret')
    
    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize computer use API
    init_computer_use_api(app, socketio, mama_bear_orchestrator)
    
    @app.route('/')
    def index():
        return jsonify({
            "message": "Podplay Sanctuary Computer Use API",
            "version": "1.0.0",
            "endpoints": {
                "status": "/api/computer-use/status",
                "execute": "/api/computer-use/execute",
                "workflows": "/api/computer-use/workflows",
                "sessions": "/api/computer-use/sessions",
                "health": "/api/computer-use/health"
            }
        })
    
    return app, socketio


if __name__ == "__main__":
    # Example usage
    app, socketio = create_computer_use_app()
    
    # Add some example routes for testing
    @app.route('/test/simple-task')
    def test_simple_task():
        """Test endpoint for simple computer use task"""
        return jsonify({
            "test_task": "Take a screenshot and describe the desktop",
            "endpoint": "/api/computer-use/execute",
            "method": "POST",
            "body": {
                "description": "Take a screenshot and describe the desktop",
                "context": {}
            }
        })
    
    @app.route('/test/workflow')
    def test_workflow():
        """Test endpoint for workflow execution"""
        return jsonify({
            "test_workflow": "research_and_document",
            "endpoint": "/api/computer-use/workflows/research_and_document",
            "method": "POST",
            "body": {
                "context": {
                    "topic": "Python web frameworks",
                    "output_location": "/tmp/research.md"
                }
            }
        })
    
    socketio.run(app, debug=True, port=5001)
