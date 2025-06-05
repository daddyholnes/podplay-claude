# backend/api/orchestration_api.py
"""
🐻 Mama Bear Orchestration API
RESTful endpoints for enhanced agent coordination
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Blueprint for legacy REST endpoints  
legacy_orchestration_bp = Blueprint('legacy_orchestration', __name__)

@legacy_orchestration_bp.route('/api/mama-bear/orchestration/chat', methods=['POST'])
def enhanced_chat():
    """
    🐻 Enhanced chat endpoint with intelligent agent routing
    """
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        
        # Get orchestrator from app config
        orchestrator = current_app.config.get('MAMA_BEAR_ORCHESTRATOR')
        
        if not orchestrator:
            # Fallback to basic response
            return jsonify({
                'success': True,
                'response': f"Enhanced orchestration not available. Received: {message}",
                'variant_used': 'basic',
                'timestamp': datetime.now().isoformat()
            })
        
        # For now, return a success response (async processing would go here)
        return jsonify({
            'success': True,
            'response': f"🐻 Enhanced Mama Bear processing: {message}",
            'orchestrator_available': True,
            'agents_count': len(orchestrator.agents) if hasattr(orchestrator, 'agents') else 0,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in enhanced_chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@legacy_orchestration_bp.route('/api/mama-bear/orchestration/status', methods=['GET'])
def orchestration_status():
    """Get the current orchestration system status"""
    try:
        orchestrator = current_app.config.get('MAMA_BEAR_ORCHESTRATOR')
        
        if not orchestrator:
            return jsonify({
                'success': True,
                'orchestrator_available': False,
                'message': 'Enhanced orchestration not initialized',
                'timestamp': datetime.now().isoformat()
            })
        
        # Get basic status info
        status = {
            'success': True,
            'orchestrator_available': True,
            'agents_available': len(orchestrator.agents) if hasattr(orchestrator, 'agents') else 0,
            'agent_types': list(orchestrator.agents.keys()) if hasattr(orchestrator, 'agents') else [],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting orchestration status: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@legacy_orchestration_bp.route('/api/mama-bear/orchestration/agents', methods=['GET'])
def list_agents():
    """List all available agents in the orchestration system"""
    try:
        orchestrator = current_app.config.get('MAMA_BEAR_ORCHESTRATOR')
        
        if not orchestrator or not hasattr(orchestrator, 'agents'):
            return jsonify({
                'success': True,
                'agents': [],
                'message': 'No agents available',
                'timestamp': datetime.now().isoformat()
            })
        
        agents_info = []
        for agent_id, agent in orchestrator.agents.items():
            agent_info = {
                'id': agent_id,
                'type': agent_id.split('_')[0],
                'state': agent.state.value if hasattr(agent, 'state') else 'unknown',
                'capabilities': getattr(agent.specialist_variant, 'capabilities', []) if hasattr(agent, 'specialist_variant') else []
            }
            agents_info.append(agent_info)
        
        return jsonify({
            'success': True,
            'agents': agents_info,
            'total_count': len(agents_info),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def integrate_orchestration_with_app(app, socketio):
    """Integrate orchestration API with Flask app"""
    
    # Register blueprint
    app.register_blueprint(legacy_orchestration_bp)
    
    logger.info("🐻 Mama Bear Orchestration API integrated successfully")
