# backend/api/enhanced_orchestration_api.py
"""
🐻 Enhanced Mama Bear Orchestration API
RESTful endpoints and WebSocket handlers for autonomous agent coordination
with Scout.new-level real-time capabilities
"""

from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room
import asyncio
import json
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Blueprint for REST endpoints
enhanced_orchestration_bp = Blueprint('enhanced_orchestration', __name__)

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/chat', methods=['POST'])
async def autonomous_chat():
    """
    🐻 Autonomous chat endpoint with intelligent agent orchestration
    Provides Scout.new-level autonomous decision making and task execution
    """
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        session_id = data.get('session_id')
        
        # Get enhanced orchestrator from app
        orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Enhanced orchestration system not initialized',
                'fallback': True
            }), 503
        
        # Process the request with autonomous orchestration
        result = await orchestrator.process_autonomous_request(
            message=message,
            user_id=user_id,
            page_context=page_context,
            session_id=session_id
        )
        
        return jsonify({
            'success': True,
            'response': result,
            'autonomous_features': {
                'decision_analysis': result.get('decision_analysis'),
                'workflow_execution': result.get('workflow_execution'),
                'learning_insights': result.get('learning_insights')
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in autonomous_chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "🐻 My autonomous systems are recalibrating! Let me help you the traditional way."
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/session', methods=['POST'])
async def create_autonomous_session():
    """Create a new persistent autonomous session"""
    try:
        data = request.json
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
        session = await session_manager.create_autonomous_session(
            user_id=user_id,
            session_type=session_type,
            initial_context=initial_context
        )
        
        return jsonify({
            'success': True,
            'session': {
                'session_id': session['session_id'],
                'type': session['type'],
                'autonomous_features': session['autonomous_features'],
                'checkpoint_enabled': session['checkpoint_enabled']
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
async def create_session_checkpoint():
    """Create a checkpoint in an autonomous session"""
    try:
        session_id = request.view_args['session_id']
        data = request.json
        checkpoint_name = data.get('name', f'checkpoint_{datetime.now().timestamp()}')
        metadata = data.get('metadata', {})
        
        session_manager = getattr(current_app, 'enhanced_session_manager', None)
        if not session_manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced session manager not initialized'
            }), 503
        
        checkpoint = await session_manager.create_checkpoint(
            session_id=session_id,
            checkpoint_name=checkpoint_name,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'checkpoint': checkpoint,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating checkpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/agents/performance', methods=['GET'])
async def get_agent_performance_metrics():
    """Get detailed performance metrics for autonomous agents"""
    try:
        orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Enhanced orchestration system not initialized'
            }), 503
        
        metrics = await orchestrator.get_performance_metrics()
        
        return jsonify({
            'success': True,
            'performance_metrics': metrics,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/workflow/<workflow_id>/status', methods=['GET'])
async def get_workflow_status():
    """Get status of a running autonomous workflow"""
    try:
        workflow_id = request.view_args['workflow_id']
        
        orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Enhanced orchestration system not initialized'
            }), 503
        
        status = await orchestrator.get_workflow_status(workflow_id)
        
        return jsonify({
            'success': True,
            'workflow_status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_orchestration_bp.route('/api/mama-bear/autonomous/learning/insights', methods=['GET'])
async def get_learning_insights():
    """Get AI learning insights from user interactions"""
    try:
        user_id = request.args.get('user_id')
        
        memory_manager = getattr(current_app, 'enhanced_memory_manager', None)
        if not memory_manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced memory manager not initialized'
            }), 503
        
        insights = await memory_manager.get_learning_insights(user_id)
        
        return jsonify({
            'success': True,
            'learning_insights': insights,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# WebSocket handlers for real-time autonomous communication
def init_enhanced_socketio_handlers(socketio):
    """Initialize enhanced WebSocket handlers for autonomous orchestration"""
    
    @socketio.on('join_autonomous_orchestration')
    def on_join_autonomous_orchestration(data):
        """Join autonomous orchestration room for real-time updates"""
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id')
        
        room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
        join_room(room_name)
        
        emit('joined_autonomous_orchestration', {
            'status': 'Connected to Autonomous Mama Bear System',
            'user_id': user_id,
            'session_id': session_id,
            'autonomous_features': [
                'real_time_decision_analysis',
                'multi_agent_coordination',
                'intelligent_checkpointing',
                'adaptive_learning',
                'proactive_assistance'
            ]
        })
    
    @socketio.on('autonomous_chat_stream')
    async def handle_autonomous_chat_stream(data):
        """Handle streaming autonomous chat with real-time agent coordination"""
        try:
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            session_id = data.get('session_id')
            page_context = data.get('page_context', 'main_chat')
            
            room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
            join_room(room_name)
            
            # Emit decision analysis phase
            emit('autonomous_thinking_phase', {
                'phase': 'decision_analysis',
                'status': '🧠 Analyzing your request with advanced AI reasoning...',
                'timestamp': datetime.now().isoformat()
            }, room=room_name)
            
            # Get enhanced orchestrator
            orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
            if not orchestrator:
                emit('autonomous_error', {
                    'error': 'Enhanced orchestration system not available',
                    'fallback': True
                }, room=room_name)
                return
            
            # Stream the autonomous processing phases
            async for phase_update in orchestrator.process_autonomous_request_stream(
                message=message,
                user_id=user_id,
                session_id=session_id,
                page_context=page_context
            ):
                emit('autonomous_phase_update', {
                    'phase': phase_update['phase'],
                    'data': phase_update['data'],
                    'timestamp': datetime.now().isoformat()
                }, room=room_name)
            
        except Exception as e:
            logger.error(f"Autonomous WebSocket error: {e}")
            emit('autonomous_error', {
                'success': False,
                'error': str(e),
                'fallback_message': "🐻 My autonomous systems encountered an issue, but I'm still here to help!"
            }, room=room_name)
    
    @socketio.on('get_autonomous_system_status')
    async def handle_autonomous_system_status():
        """Get comprehensive autonomous system status"""
        try:
            orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
            memory_manager = getattr(current_app, 'enhanced_memory_manager', None)
            session_manager = getattr(current_app, 'enhanced_session_manager', None)
            
            status = {
                'orchestrator_online': orchestrator is not None,
                'memory_system_online': memory_manager is not None,
                'session_manager_online': session_manager is not None,
                'autonomous_features': {
                    'intelligent_routing': True,
                    'multi_agent_coordination': True,
                    'persistent_sessions': True,
                    'adaptive_learning': True,
                    'proactive_assistance': True
                }
            }
            
            if orchestrator:
                orchestrator_status = await orchestrator.get_system_health()
                status['orchestrator_details'] = orchestrator_status
            
            if memory_manager:
                memory_status = await memory_manager.get_system_health()
                status['memory_details'] = memory_status
            
            emit('autonomous_system_status', {
                'success': True,
                'status': status,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            emit('autonomous_system_error', {
                'success': False,
                'error': str(e)
            })
    
    @socketio.on('start_autonomous_collaboration')
    async def handle_autonomous_collaboration(data):
        """Start an autonomous multi-agent collaboration"""
        try:
            task_description = data.get('task_description', '')
            user_id = data.get('user_id', 'default_user')
            session_id = data.get('session_id')
            collaboration_type = data.get('collaboration_type', 'adaptive')
            
            room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
            
            orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
            if not orchestrator:
                emit('collaboration_error', {
                    'error': 'Enhanced orchestration system not available'
                }, room=room_name)
                return
            
            # Start autonomous collaboration
            collaboration_id = await orchestrator.start_autonomous_collaboration(
                task_description=task_description,
                user_id=user_id,
                session_id=session_id,
                collaboration_type=collaboration_type
            )
            
            emit('autonomous_collaboration_started', {
                'collaboration_id': collaboration_id,
                'status': 'Autonomous agents are coordinating...',
                'features': [
                    'intelligent_agent_selection',
                    'adaptive_task_distribution', 
                    'real_time_progress_tracking',
                    'automatic_result_synthesis'
                ],
                'timestamp': datetime.now().isoformat()
            }, room=room_name)
            
        except Exception as e:
            emit('autonomous_collaboration_error', {
                'success': False,
                'error': str(e)
            })
    
    @socketio.on('request_proactive_assistance')
    async def handle_proactive_assistance_request(data):
        """Request proactive assistance from autonomous agents"""
        try:
            user_id = data.get('user_id', 'default_user')
            session_id = data.get('session_id')
            context = data.get('context', {})
            
            room_name = f'autonomous_{user_id}_{session_id}' if session_id else f'autonomous_{user_id}'
            
            orchestrator = getattr(current_app, 'enhanced_orchestrator', None)
            if not orchestrator:
                emit('proactive_assistance_error', {
                    'error': 'Enhanced orchestration system not available'
                }, room=room_name)
                return
            
            # Enable proactive assistance
            assistance_id = await orchestrator.enable_proactive_assistance(
                user_id=user_id,
                session_id=session_id,
                context=context
            )
            
            emit('proactive_assistance_enabled', {
                'assistance_id': assistance_id,
                'status': 'Proactive assistance activated',
                'features': [
                    'contextual_suggestions',
                    'predictive_problem_solving',
                    'automated_optimization',
                    'intelligent_recommendations'
                ],
                'timestamp': datetime.now().isoformat()
            }, room=room_name)
            
        except Exception as e:
            emit('proactive_assistance_error', {
                'success': False,
                'error': str(e)
            })

# Background autonomous system monitoring
async def autonomous_system_monitor_broadcast(app, socketio):
    """Background task to broadcast autonomous system status updates"""
    
    while True:
        try:
            with app.app_context():
                orchestrator = getattr(app, 'enhanced_orchestrator', None)
                memory_manager = getattr(app, 'enhanced_memory_manager', None)
                
                if orchestrator and memory_manager:
                    # Get comprehensive system metrics
                    orchestrator_metrics = await orchestrator.get_performance_metrics()
                    memory_metrics = await memory_manager.get_system_metrics()
                    
                    # Broadcast to all autonomous clients
                    socketio.emit('autonomous_system_metrics', {
                        'orchestrator_metrics': orchestrator_metrics,
                        'memory_metrics': memory_metrics,
                        'autonomous_capabilities_status': 'optimal',
                        'timestamp': datetime.now().isoformat()
                    }, namespace='/', broadcast=True)
            
            # Wait 45 seconds before next update (less frequent than basic system)
            await asyncio.sleep(45)
            
        except Exception as e:
            logger.error(f"Autonomous system monitor error: {e}")
            await asyncio.sleep(90)  # Wait longer on error

# Enhanced Flask app integration with autonomous capabilities
def integrate_enhanced_orchestration_with_app(app, socketio, enhanced_memory_manager, enhanced_orchestrator, enhanced_session_manager):
    """
    Complete integration of enhanced autonomous orchestration system with Flask app
    """
    
    # Store enhanced components in app
    app.enhanced_memory_manager = enhanced_memory_manager
    app.enhanced_orchestrator = enhanced_orchestrator
    app.enhanced_session_manager = enhanced_session_manager
    
    # Register enhanced blueprint
    app.register_blueprint(enhanced_orchestration_bp)
    
    # Initialize enhanced WebSocket handlers
    init_enhanced_socketio_handlers(socketio)
    
    # Start enhanced background monitoring
    with app.app_context():
        asyncio.create_task(autonomous_system_monitor_broadcast(app, socketio))
    
    # Add enhanced middleware for autonomous context preservation
    @app.before_request
    def before_enhanced_request():
        """Preserve enhanced context across requests with learning capabilities"""
        if hasattr(app, 'enhanced_memory_manager') and request.json:
            user_id = request.json.get('user_id')
            session_id = request.json.get('session_id')
            
            if user_id:
                # Enhanced context tracking with learning
                asyncio.create_task(
                    app.enhanced_memory_manager.track_user_interaction(
                        user_id=user_id,
                        session_id=session_id,
                        interaction_type='api_request',
                        context={
                            'endpoint': request.endpoint,
                            'method': request.method,
                            'timestamp': datetime.now(),
                            'user_agent': request.headers.get('User-Agent')
                        }
                    )
                )
    
    logger.info("🚀 Enhanced Autonomous Mama Bear Orchestration API integrated successfully!")
    logger.info("🐻 Scout.new-level autonomous capabilities now available!")
