#!/usr/bin/env python3
"""
🐻 Test Enhanced Mama Bear Flask Application
Minimal test version focusing on Mem0-based enhanced system integration
"""

import os
import logging
import asyncio
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TestEnhancedApp")

# Import enhanced system components
try:
    from services.complete_enhanced_integration import integrate_complete_enhanced_system_with_app
    from services.mama_bear_model_manager import MamaBearModelManager
    from services.enhanced_scrapybara_integration import EnhancedScrapybaraManager
    ENHANCED_SYSTEM_AVAILABLE = True
    logger.info("✅ Enhanced system components available")
except ImportError as e:
    logger.error(f"❌ Enhanced system not available: {e}")
    ENHANCED_SYSTEM_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/test/health', methods=['GET'])
def test_health():
    """Test health endpoint"""
    return jsonify({
        'success': True,
        'message': 'Test app is running',
        'enhanced_system_available': ENHANCED_SYSTEM_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test/enhanced/chat', methods=['POST'])
def test_enhanced_chat():
    """Test enhanced chat endpoint"""
    try:
        data = request.json or {}
        message = data.get('message', 'Hello, Mama Bear!')
        user_id = data.get('user_id', 'test_user')
        
        # Check if enhanced system is available
        enhanced_integration = getattr(app, 'complete_enhanced_integration', None)
        
        if enhanced_integration and enhanced_integration.is_initialized:
            # Use enhanced system
            import asyncio
            result = asyncio.run(enhanced_integration.process_autonomous_request(
                message=message,
                user_id=user_id,
                session_id=None,
                page_context='test'
            ))
            
            return jsonify({
                'success': True,
                'response': result,
                'enhanced_system_used': True,
                'timestamp': datetime.now().isoformat()
            })
        else:
            # Fallback response
            return jsonify({
                'success': True,
                'response': {
                    'content': f"🐻 Test response: {message}",
                    'variant': 'test',
                    'model': 'test_fallback'
                },
                'enhanced_system_used': False,
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error in test chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test/enhanced/status', methods=['GET'])
def test_enhanced_status():
    """Test enhanced system status"""
    try:
        enhanced_integration = getattr(app, 'complete_enhanced_integration', None)
        
        status = {
            'enhanced_system_available': ENHANCED_SYSTEM_AVAILABLE,
            'enhanced_system_initialized': enhanced_integration is not None and enhanced_integration.is_initialized if enhanced_integration else False,
            'components': {
                'memory_manager': hasattr(app, 'enhanced_memory_manager'),
                'orchestrator': hasattr(app, 'enhanced_orchestrator'),
                'session_manager': hasattr(app, 'enhanced_session_manager')
            }
        }
        
        if enhanced_integration and enhanced_integration.is_initialized:
            import asyncio
            system_status = asyncio.run(enhanced_integration.get_comprehensive_system_status())
            status['detailed_status'] = system_status
            
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

async def initialize_enhanced_system():
    """Initialize the enhanced system"""
    global ENHANCED_SYSTEM_AVAILABLE
    
    if not ENHANCED_SYSTEM_AVAILABLE:
        logger.warning("⚠️ Enhanced system not available")
        return False
        
    try:
        logger.info("🚀 Initializing Enhanced System for Testing...")
        
        # Create model manager and Scrapybara client
        model_manager = MamaBearModelManager()
        
        scrapybara_config = {
            'scrapybara_api_key': os.getenv('SCRAPYBARA_API_KEY'),
            'scrapybara_base_url': os.getenv('SCRAPYBARA_BASE_URL', 'https://api.scrapybara.com/v1'),
            'enable_cua': True,
            'enable_collaboration': True
        }
        scrapybara_client = EnhancedScrapybaraManager(scrapybara_config)
        
        # Integrate with Flask app
        integration_result = await integrate_complete_enhanced_system_with_app(
            app=app,
            socketio=socketio,
            model_manager=model_manager,
            scrapybara_client=scrapybara_client
        )
        
        if integration_result['success']:
            logger.info("✅ Enhanced system integrated successfully!")
            logger.info("🧠 Mem0-based memory system active")
            logger.info("🤖 Autonomous orchestration online")
            return True
        else:
            logger.error(f"❌ Enhanced system integration failed: {integration_result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize enhanced system: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == '__main__':
    async def startup():
        """Start the test app"""
        logger.info("🧪 Starting Enhanced System Test App...")
        
        success = await initialize_enhanced_system()
        if success:
            logger.info("🎉 Enhanced system test app ready!")
        else:
            logger.info("⚠️ Running in basic mode")
    
    # Run startup
    asyncio.run(startup())
    
    # Start the test app
    logger.info("🚀 Starting test server on http://localhost:5002")
    socketio.run(
        app,
        host='0.0.0.0',
        port=5002,
        debug=True
    )
