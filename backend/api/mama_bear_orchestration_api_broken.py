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

logger = logging.getLogger(__name__)

# Blueprint for REST endpoints
orchestration_bp = Blueprint('orchestration', __name__)

@orchestration_bp.route('/api/mama-bear/chat', methods=['POST'])
async def intelligent_chat():
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
        orchestrator = getattr(current_app, 'mama_bear_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Process the request with intelligent routing
        result = await orchestrator.process_user_request(
            message=message,
            user_id=user_id,
            page_context=page_context
        )
        
        return jsonify({
            'success': True,
            'response': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in intelligent_chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "🐻 I'm having a moment! Let me gather myself and try again."
        }), 500

@orchestration_bp.route('/api/mama-bear/agents/status', methods=['GET'])
async def get_agents_status():
    """Get status of all agents"""
    try:
        orchestrator = current_app.mama_bear_orchestrator
        status = await orchestrator.get_system_status()
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/agents/<agent_id>/direct', methods=['POST'])
async def direct_agent_communication():
    """Communicate directly with a specific agent"""
    try:
        agent_id = request.view_args['agent_id']
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = current_app.mama_bear_orchestrator
        
        # Get the specific agent
        agent = orchestrator.agents.get(agent_id)
        if not agent:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_id} not found'
            }), 404
        
        # Direct communication with agent
        result = await agent.handle_request(message, user_id)
        
        return jsonify({
            'success': True,
            'response': result,
            'agent_id': agent_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/workflow/analyze', methods=['POST'])
async def analyze_workflow():
    """Analyze a request and suggest workflow approach"""
    try:
        data = request.json
        request_text = data.get('request', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = current_app.mama_bear_orchestrator
        workflow_intelligence = orchestrator.workflow_intelligence
        
        # Analyze the workflow
        analysis = await workflow_intelligence.analyze_request(request_text, user_id)
        
        return jsonify({
            'success': True,
            'analysis': {
                'workflow_type': analysis.workflow_type.value,
                'confidence': analysis.confidence,
                'recommended_agents': analysis.recommended_agents,
                'estimated_complexity': analysis.estimated_complexity,
                'estimated_duration': analysis.estimated_duration,
                'resource_requirements': analysis.resource_requirements
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/memory/search', methods=['POST'])
async def search_memory():
    """Search user memories"""
    try:
        data = request.json
        query = data.get('query', '')
        user_id = data.get('user_id', 'default_user')
        limit = data.get('limit', 10)
        
        orchestrator = current_app.mama_bear_orchestrator
        memory_manager = orchestrator.memory_manager
        
        # Search memories
        memories = await memory_manager.search_memories(query, user_id, limit)
        
        # Convert memories to serializable format
        memory_data = []
        for memory in memories:
            memory_data.append({
                'id': memory.id,
                'type': memory.type.value,
                'content': memory.content,
                'importance': memory.importance.value,
                'tags': memory.tags,
                'created_at': memory.created_at.isoformat(),
                'access_count': memory.access_count
            })
        
        return jsonify({
            'success': True,
            'memories': memory_data,
            'total_found': len(memory_data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/context', methods=['GET'])
async def get_global_context():
    """Get current global context"""
    try:
        orchestrator = current_app.mama_bear_orchestrator
        
        return jsonify({
            'success': True,
            'context': orchestrator.context_awareness.global_context,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/context', methods=['POST'])
async def update_global_context():
    """Update global context"""
    try:
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({
                'success': False,
                'error': 'Key is required'
            }), 400
        
        orchestrator = current_app.mama_bear_orchestrator
        await orchestrator.context_awareness.update_global_context(key, value)
        
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
async def get_user_profile():
    """Get user profile and preferences"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        orchestrator = current_app.mama_bear_orchestrator
        memory_manager = orchestrator.memory_manager
        
        # Get user profile
        profile = await memory_manager.get_user_profile(user_id)
        
        # Get decision patterns
        patterns = await memory_manager.analyze_decision_patterns(user_id)
        
        return jsonify({
            'success': True,
            'profile': {
                'user_id': profile.user_id,
                'expertise_level': profile.expertise_level,
                'preferred_agents': profile.preferred_agents,
                'communication_style': profile.communication_style,
                'success_patterns': profile.success_patterns,
                'learning_preferences': profile.learning_preferences,
                'last_updated': profile.last_updated.isoformat()
            },
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/system/stats', methods=['GET'])
async def get_system_stats():
    """Get comprehensive system statistics"""
    try:
        orchestrator = current_app.mama_bear_orchestrator
        
        # Get memory stats
        memory_stats = await orchestrator.memory_manager.get_memory_stats()
        
        # Get agent stats
        agent_stats = {}
        for agent_id, agent in orchestrator.agents.items():
            agent_stats[agent_id] = {
                'name': agent.name,
                'personality': agent.personality,
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
        user_id = data.get('user_id', 'default_user')
        room = f"mama_bear_{user_id}"
        join_room(room)
        emit('joined_mama_bear', {'room': room, 'status': 'connected'})
        logger.info(f"🐻 User {user_id} joined Mama Bear room")
    
    @socketio.on('leave_mama_bear')
    def on_leave_mama_bear(data):
        """Leave Mama Bear room"""
        user_id = data.get('user_id', 'default_user')
        room = f"mama_bear_{user_id}"
        leave_room(room)
        emit('left_mama_bear', {'room': room, 'status': 'disconnected'})
    
    @socketio.on('mama_bear_chat')
    async def on_mama_bear_chat(data):
        """Handle real-time chat with Mama Bear"""
        try:
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            page_context = data.get('page_context', 'main_chat')
            room = f"mama_bear_{user_id}"
            
            # Get orchestrator
            orchestrator = current_app.mama_bear_orchestrator
            
            # Emit thinking status
            emit('mama_bear_thinking', {
                'status': 'processing',
                'message': '🐻 Let me think about this...'
            }, room=room)
            
            # Process the request
            result = await orchestrator.process_user_request(
                message=message,
                user_id=user_id,
                page_context=page_context
            )
            
            # Emit response
            emit('mama_bear_response', {
                'success': True,
                'response': result,
                'timestamp': datetime.now().isoformat()
            }, room=room)
            
        except Exception as e:
            emit('mama_bear_error', {
                'success': False,
                'error': str(e),
                'fallback_message': "🐻 I'm having a moment! Let me gather myself and try again."
            }, room=room)
    
    @socketio.on('mama_bear_agent_direct')
    async def on_direct_agent_chat(data):
        """Direct communication with specific agent"""
        try:
            agent_id = data.get('agent_id')
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            room = f"mama_bear_{user_id}"
            
            orchestrator = current_app.mama_bear_orchestrator
            agent = orchestrator.agents.get(agent_id)
            
            if not agent:
                emit('agent_error', {
                    'error': f'Agent {agent_id} not found'
                }, room=room)
                return
            
            # Direct communication
            result = await agent.handle_request(message, user_id)
            
            emit('agent_response', {
                'agent_id': agent_id,
                'response': result,
                'timestamp': datetime.now().isoformat()
            }, room=room)
            
        except Exception as e:
            emit('agent_error', {
                'error': str(e)
            }, room=room)

def integrate_orchestration_with_app(app, socketio):
    """Integrate orchestration API with Flask app"""
    
    # Register blueprint
    app.register_blueprint(orchestration_bp)
    
    # Setup WebSocket handlers
    setup_orchestration_websockets(socketio)
    
    logger.info("🐻 Mama Bear Orchestration API integrated successfully")
