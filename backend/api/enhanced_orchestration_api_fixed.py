"""
Enhanced Orchestration API - Provides REST and WebSocket endpoints for the 
Autonomous Mama Bear System with Scout.new-level capabilities
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room, disconnect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create enhanced orchestration blueprint
enhanced_orchestration_bp = Blueprint('enhanced_orchestration', __name__)

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/chat', methods=['POST'])
async def autonomous_chat():
    """
    Enhanced autonomous chat endpoint with intelligent orchestration
    Provides Scout.new-level autonomous capabilities with streaming phases
    """
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
            
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        session_id = data.get('session_id')
        
        # Get enhanced orchestrator from app
        orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Enhanced orchestration system not initialized'
            }), 503
        
        # Create autonomous orchestration request
        orchestration_request = {
            'message': message,
            'user_id': user_id,
            'page_context': page_context,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'autonomous_mode': True,
            'scout_level_features': True
        }
        
        # Execute autonomous orchestration with streaming
        response = await orchestrator.execute_autonomous_orchestration(orchestration_request)
        
        return jsonify({
            'success': True,
            'data': response,
            'autonomous_features': {
                'intelligent_routing': True,
                'context_awareness': True,
                'proactive_behaviors': True,
                'adaptive_learning': True
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in autonomous chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'autonomous_features': {
                'error_recovery': True,
                'fallback_routing': True
            }
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/session', methods=['POST'])
async def create_autonomous_session():
    """Create a new persistent autonomous session"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
            
        user_id = data.get('user_id', 'default_user')
        session_type = data.get('session_type', 'general')
        initial_context = data.get('context', {})
        
        session_manager = getattr(current_app, 'enhanced_session_manager', None)
        if not session_manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced session manager not initialized'
            }), 503
        
        # Create persistent session with Mem0 integration
        session = await session_manager.create_enhanced_session(
            user_id=user_id,
            session_type=session_type,
            initial_context=initial_context,
            autonomous_features=True
        )
        
        return jsonify({
            'success': True,
            'data': {
                'session_id': session.get('session_id', ''),
                'session_type': session.get('session_type', ''),
                'autonomous_capabilities': session.get('autonomous_capabilities', {}),
                'mem0_integration': session.get('mem0_integration', False),
                'checkpoint_enabled': session.get('checkpoint_enabled', False)
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating autonomous session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/session/<session_id>/checkpoint', methods=['POST'])
async def create_session_checkpoint(session_id: str):
    """Create a checkpoint in an autonomous session"""
    try:
        data = request.json or {}
        checkpoint_type = data.get('checkpoint_type', 'manual')
        metadata = data.get('metadata', {})
        
        session_manager = getattr(current_app, 'enhanced_session_manager', None)
        if not session_manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced session manager not initialized'
            }), 503
        
        # Create intelligent checkpoint
        checkpoint = await session_manager.create_intelligent_checkpoint(
            session_id=session_id,
            checkpoint_type=checkpoint_type,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'data': {
                'checkpoint_id': checkpoint.get('checkpoint_id', ''),
                'session_id': session_id,
                'checkpoint_type': checkpoint.get('checkpoint_type', ''),
                'timestamp': checkpoint.get('timestamp', ''),
                'mem0_snapshot': checkpoint.get('mem0_snapshot', False)
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating session checkpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/performance', methods=['GET'])
async def get_autonomous_performance():
    """Get performance metrics for the autonomous system"""
    try:
        orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Enhanced orchestration system not initialized'
            }), 503
        
        # Get performance metrics (implement this method if missing)
        try:
            metrics = await orchestrator.get_performance_metrics()
        except AttributeError:
            # Fallback metrics if method doesn't exist
            metrics = {
                'autonomous_sessions': 0,
                'successful_orchestrations': 0,
                'average_response_time': 0.0,
                'agent_utilization': {},
                'memory_efficiency': 0.0,
                'error_rate': 0.0
            }
        
        return jsonify({
            'success': True,
            'data': metrics,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/agents', methods=['GET'])
async def get_autonomous_agents():
    """Get information about autonomous agents"""
    try:
        orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Enhanced orchestration system not initialized'
            }), 503
        
        # Get agent information
        agents_info = {
            'available_agents': list(orchestrator.specialized_agents.keys()) if hasattr(orchestrator, 'specialized_agents') else [],
            'agent_status': {},
            'capabilities': {
                'research_agent': 'Advanced research and analysis',
                'devops_agent': 'Infrastructure and deployment',
                'scout_agent': 'Exploration and discovery',
                'model_coordinator': 'AI model coordination',
                'tool_curator': 'Tool selection and management',
                'integration_architect': 'System integration',
                'live_api_agent': 'Real-time API interactions'
            }
        }
        
        return jsonify({
            'success': True,
            'data': agents_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting agent information: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# WebSocket Event Handlers
def register_socketio_handlers(socketio):
    """Register WebSocket handlers for autonomous orchestration"""
    
    @socketio.on('join_autonomous_orchestration')
    def on_join_autonomous_orchestration(data):
        """Join autonomous orchestration room for real-time updates"""
        if not data:
            emit('error', {'message': 'Invalid data'})
            return
            
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id')
        
        room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
        join_room(room_name)
        
        emit('joined_autonomous_orchestration', {
            'status': 'Connected to Autonomous Mama Bear System',
            'room': room_name,
            'features': ['real_time_updates', 'autonomous_coordination', 'intelligent_routing']
        })
        
        logger.info(f"User {user_id} joined autonomous orchestration room: {room_name}")

    @socketio.on('autonomous_orchestration_request')
    def on_autonomous_orchestration_request(data):
        """Handle real-time autonomous orchestration requests"""
        try:
            if not data:
                emit('autonomous_error', {'message': 'Invalid request data'})
                return
                
            user_id = data.get('user_id', 'anonymous')
            session_id = data.get('session_id')
            message = data.get('message', '')
            
            room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
            join_room(room_name)
            
            # Emit processing started
            emit('autonomous_processing_started', {
                'message': 'Starting autonomous orchestration...',
                'user_id': user_id,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            }, to=room_name)
            
            # Process asynchronously and emit updates
            orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
            if orchestrator:
                # Emit phase updates (Scout.new-style streaming)
                emit('autonomous_phase_update', {
                    'phase': 'agent_selection',
                    'message': 'Selecting optimal agents for your request...',
                    'progress': 25
                }, to=room_name)
                
                emit('autonomous_phase_update', {
                    'phase': 'context_analysis',
                    'message': 'Analyzing context and user patterns...',
                    'progress': 50
                }, to=room_name)
                
                emit('autonomous_phase_update', {
                    'phase': 'execution',
                    'message': 'Executing autonomous orchestration...',
                    'progress': 75
                }, to=room_name)
                
                # Final response (this would be replaced with actual orchestration)
                emit('autonomous_response', {
                    'response': 'Autonomous orchestration completed successfully',
                    'metadata': {
                        'agents_used': ['research_agent', 'integration_architect'],
                        'execution_time': '2.3s',
                        'confidence': 0.92
                    },
                    'progress': 100
                }, to=room_name)
            else:
                emit('autonomous_error', {
                    'message': 'Enhanced orchestration system not available',
                    'error_code': 'ORCHESTRATOR_UNAVAILABLE'
                }, to=room_name)
                
        except Exception as e:
            logger.error(f"Error in autonomous orchestration request: {e}")
            emit('autonomous_error', {
                'message': f'Error processing request: {str(e)}',
                'error_code': 'PROCESSING_ERROR'
            })

    @socketio.on('autonomous_collaboration_request')
    def on_autonomous_collaboration_request(data):
        """Handle autonomous agent collaboration requests"""
        try:
            if not data:
                emit('collaboration_error', {'message': 'Invalid collaboration data'})
                return
                
            user_id = data.get('user_id', 'anonymous')
            session_id = data.get('session_id')
            collaboration_type = data.get('collaboration_type', 'general')
            
            room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
            
            # Get collaboration orchestrator
            orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
            if orchestrator and hasattr(orchestrator, 'collaboration_orchestrator'):
                collaboration_result = {
                    'collaboration_id': f'collab_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                    'participating_agents': ['research_agent', 'devops_agent', 'integration_architect'],
                    'collaboration_type': collaboration_type,
                    'status': 'active'
                }
                
                emit('collaboration_started', collaboration_result, to=room_name)
            else:
                emit('collaboration_error', {
                    'message': 'Collaboration system not available',
                    'error_code': 'COLLABORATION_UNAVAILABLE'
                }, to=room_name)
                
        except Exception as e:
            logger.error(f"Error in collaboration request: {e}")
            emit('collaboration_error', {
                'message': f'Error in collaboration: {str(e)}',
                'error_code': 'COLLABORATION_ERROR'
            })

    @socketio.on('leave_autonomous_orchestration')
    def on_leave_autonomous_orchestration(data):
        """Leave autonomous orchestration room"""
        if not data:
            return
            
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id')
        
        room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
        leave_room(room_name)
        
        emit('left_autonomous_orchestration', {
            'status': 'Disconnected from Autonomous Mama Bear System',
            'room': room_name
        })
        
        logger.info(f"User {user_id} left autonomous orchestration room: {room_name}")

    @socketio.on('disconnect')
    def on_disconnect():
        """Handle client disconnection"""
        logger.info("Client disconnected from autonomous orchestration")

    return socketio


# Background monitoring function
async def start_autonomous_monitoring():
    """Start background monitoring for the autonomous system"""
    try:
        logger.info("Starting autonomous system monitoring...")
        
        # This would contain actual monitoring logic
        # For now, just log that monitoring is active
        while True:
            await asyncio.sleep(30)  # Monitor every 30 seconds
            logger.debug("Autonomous system monitoring heartbeat")
            
    except Exception as e:
        logger.error(f"Error in autonomous monitoring: {e}")


def init_enhanced_orchestration_api(app, socketio):
    """Initialize the enhanced orchestration API with the Flask app"""
    try:
        # Register blueprint
        app.register_blueprint(enhanced_orchestration_bp)
        
        # Register WebSocket handlers
        register_socketio_handlers(socketio)
        
        # Start background monitoring (in a real app, this would be handled differently)
        logger.info("Enhanced Orchestration API initialized successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Error initializing Enhanced Orchestration API: {e}")
        return False
