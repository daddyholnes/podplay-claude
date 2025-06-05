# backend/api/mama_bear_orchestration_api.py
"""
🐻 Mama Bear Orchestration API
RESTful endpoints and WebSocket handlers for agent coordination
"""

from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room
import asyncio
import json
from datetime import datetime
import logging
from enum import Enum
from dataclasses import is_dataclass, asdict
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

# Blueprint for REST endpoints
orchestration_bp = Blueprint('orchestration', __name__)

def serialize_for_json(obj: Any) -> Any:
    """
    Recursively serialize complex objects for JSON output.
    Handles enums, dataclasses, datetime objects, and nested structures.
    """
    if obj is None:
        return None
    elif isinstance(obj, Enum):
        # Convert enum to its string value
        return obj.value
    elif is_dataclass(obj) and not isinstance(obj, type):
        # Convert dataclass instance to dictionary and recursively serialize its contents
        return {k: serialize_for_json(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, datetime):
        # Convert datetime to ISO format string
        return obj.isoformat()
    elif isinstance(obj, dict):
        # Recursively serialize dictionary values
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        # Recursively serialize list/tuple items
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool)):
        # Basic types - return as-is
        return obj
    else:
        # For any other type, try to convert to string as fallback
        try:
            return str(obj)
        except Exception:
            return f"<{type(obj).__name__}: serialization failed>"

def get_orchestrator():
    """Safely get orchestrator from app context"""
    return current_app.config.get('MAMA_BEAR_ORCHESTRATOR')

@orchestration_bp.route('/api/mama-bear/chat', methods=['POST'])
def intelligent_chat():
    """
    🐻 Main chat endpoint with intelligent agent routing
    Automatically determines which agents to involve based on the request
    """
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        
        # Get orchestrator from app
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Process the request with intelligent routing (run async in sync context)
        result = asyncio.run(orchestrator.process_user_request(
            message=message,
            user_id=user_id,
            page_context=page_context
        ))
        
        # Debug logging
        logger.info(f"Orchestrator result type: {type(result)}")
        logger.info(f"Orchestrator result: {result}")
        
        # Serialize the result to handle enums and complex objects
        try:
            serialized_result = serialize_for_json(result)
            logger.info(f"Serialization successful: {type(serialized_result)}")
        except Exception as serialize_error:
            logger.error(f"Serialization failed: {serialize_error}")
            logger.error(f"Failed object: {result}")
            raise
        
        return jsonify({
            'success': True,
            'response': serialized_result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in intelligent_chat: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "🐻 I'm having a moment! Let me gather myself and try again."
        }), 500

@orchestration_bp.route('/api/mama-bear/agents/status', methods=['GET'])
def get_agents_status():
    """Get status of all agents"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        status = asyncio.run(orchestrator.get_system_status())
        
        # Serialize the status to handle enums and complex objects
        serialized_status = serialize_for_json(status)
        
        return jsonify({
            'success': True,
            'status': serialized_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/agents/<agent_id>/direct', methods=['POST'])
def direct_agent_communication(agent_id):
    """Communicate directly with a specific agent"""
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Get the specific agent
        agent = orchestrator.agents.get(agent_id) if orchestrator.agents else None
        if not agent:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_id} not found'
            }), 404
        
        # Direct communication with agent
        result = asyncio.run(agent.handle_request(message, user_id))
        
        # Serialize the result to handle enums and complex objects
        serialized_result = serialize_for_json(result)
        
        return jsonify({
            'success': True,
            'response': serialized_result,
            'agent_id': agent_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/workflow/analyze', methods=['POST'])
def analyze_workflow():
    """Analyze a request and suggest workflow approach"""
    try:
        data = request.json or {}
        request_text = data.get('request', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        workflow_intelligence = getattr(orchestrator, 'workflow_intelligence', None)
        if not workflow_intelligence:
            return jsonify({
                'success': False,
                'error': 'Workflow intelligence not available'
            }), 500
        
        # Analyze the workflow
        analysis = asyncio.run(workflow_intelligence.analyze_request(request_text, user_id))
        
        # Serialize the analysis to handle enums and complex objects
        serialized_analysis = serialize_for_json(analysis)
        
        return jsonify({
            'success': True,
            'analysis': serialized_analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/memory/search', methods=['POST'])
def search_memory():
    """Search user memories"""
    try:
        data = request.json or {}
        query = data.get('query', '')
        user_id = data.get('user_id', 'default_user')
        limit = data.get('limit', 10)
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        memory_manager = getattr(orchestrator, 'memory_manager', None)
        if not memory_manager:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 500
        
        # Search memories
        memories = asyncio.run(memory_manager.search_memories(query, user_id, limit))
        
        # Serialize memories to handle enums and complex objects
        serialized_memories = serialize_for_json(memories)
        
        return jsonify({
            'success': True,
            'memories': serialized_memories,
            'total_found': len(serialized_memories) if isinstance(serialized_memories, list) else 0,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/context', methods=['GET'])
def get_global_context():
    """Get current global context"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        context_awareness = getattr(orchestrator, 'context_awareness', None)
        global_context = getattr(context_awareness, 'global_context', {}) if context_awareness else {}
        
        return jsonify({
            'success': True,
            'context': global_context,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/context', methods=['POST'])
def update_global_context():
    """Update global context"""
    try:
        data = request.json or {}
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({
                'success': False,
                'error': 'Key is required'
            }), 400
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        context_awareness = getattr(orchestrator, 'context_awareness', None)
        if context_awareness and hasattr(context_awareness, 'update_global_context'):
            asyncio.run(context_awareness.update_global_context(key, value))
        
        return jsonify({
            'success': True,
            'message': f'Context updated: {key}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/user/profile', methods=['GET'])
def get_user_profile():
    """Get user profile and preferences"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        memory_manager = getattr(orchestrator, 'memory_manager', None)
        if not memory_manager:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 500
        
        # Get user profile
        profile = asyncio.run(memory_manager.get_user_profile(user_id))
        
        # Get decision patterns
        patterns = asyncio.run(memory_manager.analyze_decision_patterns(user_id))
        
        # Serialize profile and patterns to handle complex objects
        serialized_profile = serialize_for_json(profile)
        serialized_patterns = serialize_for_json(patterns)
        
        return jsonify({
            'success': True,
            'profile': serialized_profile,
            'patterns': serialized_patterns,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/system/stats', methods=['GET'])
def get_system_stats():
    """Get comprehensive system statistics"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Get memory stats
        memory_manager = getattr(orchestrator, 'memory_manager', None)
        memory_stats = asyncio.run(memory_manager.get_memory_stats()) if memory_manager else {}
        
        # Get agent stats
        agent_stats = {}
        agents = getattr(orchestrator, 'agents', {})
        for agent_id, agent in agents.items():
            agent_stats[agent_id] = {
                'name': getattr(agent, 'name', agent_id),
                'personality': getattr(agent, 'personality', 'unknown'),
                'active': True,
                'specialties': getattr(agent, 'specialties', [])
            }
        
        # Get workflow stats
        workflow_stats = {
            'total_requests_processed': getattr(orchestrator, 'total_requests', 0),
            'active_collaborations': len(getattr(orchestrator, 'active_tasks', {}))
        }
        
        return jsonify({
            'success': True,
            'stats': {
                'memory': memory_stats,
                'agents': agent_stats,
                'workflow': workflow_stats,
                'system_uptime': datetime.now().isoformat()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# WebSocket handlers for real-time communication
def setup_orchestration_websockets(socketio):
    """Setup WebSocket handlers for orchestration"""
    
    @socketio.on('join_mama_bear')
    def on_join_mama_bear(data):
        """Join Mama Bear room for real-time updates"""
        data = data or {}
        user_id = data.get('user_id', 'default_user')
        room = f"mama_bear_{user_id}"
        join_room(room)
        emit('joined_mama_bear', {'room': room, 'status': 'connected'})
        logger.info(f"🐻 User {user_id} joined Mama Bear room")
    
    @socketio.on('leave_mama_bear')
    def on_leave_mama_bear(data):
        """Leave Mama Bear room"""
        data = data or {}
        user_id = data.get('user_id', 'default_user')
        room = f"mama_bear_{user_id}"
        leave_room(room)
        emit('left_mama_bear', {'room': room, 'status': 'disconnected'})
    
    @socketio.on('mama_bear_chat')
    async def on_mama_bear_chat(data):
        """Handle real-time chat with Mama Bear"""
        try:
            data = data or {}
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            page_context = data.get('page_context', 'main_chat')
            room = f"mama_bear_{user_id}"
            
            # Get orchestrator
            orchestrator = get_orchestrator()
            if not orchestrator:
                emit('mama_bear_error', {
                    'success': False,
                    'error': 'Orchestrator not available'
                })
                return
            
            # Emit thinking status
            socketio.emit('mama_bear_thinking', {
                'status': 'processing',
                'message': '🐻 Let me think about this...'
            }, to=room)
            
            # Process the request
            result = await orchestrator.process_user_request(
                message=message,
                user_id=user_id,
                page_context=page_context
            )
            
            # Serialize the result to handle enums and complex objects
            serialized_result = serialize_for_json(result)
            
            # Emit response
            socketio.emit('mama_bear_response', {
                'success': True,
                'response': serialized_result,
                'timestamp': datetime.now().isoformat()
            }, to=room)
            
        except Exception as e:
            logger.error(f"Error in mama_bear_chat: {e}")
            socketio.emit('mama_bear_error', {
                'success': False,
                'error': str(e),
                'fallback_message': "🐻 I'm having a moment! Let me gather myself and try again."
            }, to=room)
    
    @socketio.on('mama_bear_agent_direct')
    async def on_direct_agent_chat(data):
        """Direct communication with specific agent"""
        try:
            data = data or {}
            agent_id = data.get('agent_id')
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            room = f"mama_bear_{user_id}"
            
            orchestrator = get_orchestrator()
            if not orchestrator:
                socketio.emit('agent_error', {
                    'error': 'Orchestrator not available'
                }, to=room)
                return
                
            agents = getattr(orchestrator, 'agents', {})
            agent = agents.get(agent_id) if agents else None
            
            if not agent:
                socketio.emit('agent_error', {
                    'error': f'Agent {agent_id} not found'
                }, to=room)
                return
            
            # Direct communication
            result = await agent.handle_request(message, user_id)
            
            # Serialize the result to handle enums and complex objects
            serialized_result = serialize_for_json(result)
            
            socketio.emit('agent_response', {
                'agent_id': agent_id,
                'response': serialized_result,
                'timestamp': datetime.now().isoformat()
            }, to=room)
            
        except Exception as e:
            logger.error(f"Error in direct agent chat: {e}")
            socketio.emit('agent_error', {
                'error': str(e)
            }, to=room)

def integrate_orchestration_with_app(app, socketio):
    """Integrate orchestration API with Flask app"""
    
    # Register blueprint
    app.register_blueprint(orchestration_bp)
    
    # Setup WebSocket handlers
    setup_orchestration_websockets(socketio)
    
    logger.info("🐻 Mama Bear Orchestration API integrated successfully")
