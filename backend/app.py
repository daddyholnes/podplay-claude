"""
🐻 Podplay Sanctuary - Enhanced Mama Bear Flask Application
Neurodivergent-friendly development sanctuary with 7 Mama Bear variants,
3 sensory-friendly themes, and instant cloud development environments
"""

import os
import logging
import asyncio
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json

# Remove Redis dependency - replaced with Mem0-based persistence

# Initialize logging first
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'mama_bear.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PodplaySanctuary")

# Import our sanctuary services
from config.settings import get_settings
from api.mama_bear_orchestration_api import integrate_orchestration_with_app
from services import (
    initialize_all_services, 
    shutdown_all_services,
    get_mama_bear_agent,
    get_memory_manager, 
    get_scrapybara_manager,
    get_theme_manager,
    get_service_status
)

# Import enhanced Mama Bear orchestration with Mem0 integration
try:
    from services.complete_enhanced_integration import integrate_complete_enhanced_system_with_app, CompleteEnhancedIntegration
    from services.mama_bear_model_manager import MamaBearModelManager
    from services.enhanced_scrapybara_integration import EnhancedScrapybaraManager
    from api.enhanced_orchestration_api_fixed import init_enhanced_orchestration_api as integrate_enhanced_orchestration_with_app
    ENHANCED_SYSTEM_AVAILABLE = True
    logger.info("✅ Complete Enhanced System with Mem0 integration available")
except ImportError as e:
    logger.warning(f"Complete Enhanced System not available: {e}")
    ENHANCED_SYSTEM_AVAILABLE = False
    integrate_complete_enhanced_system_with_app = None
    enhanced_integration = None

# Import collaborative workspace system
try:
    from api.collaborative_workspace_api import collaborative_bp, initialize_collaborative_api
    from services.enhanced_collaborative_integration import EnhancedCollaborativeIntegration
    COLLABORATIVE_WORKSPACE_AVAILABLE = True
    logger.info("✅ Collaborative Workspace System available")
except ImportError as e:
    logger.warning(f"Collaborative Workspace System not available: {e}")
    COLLABORATIVE_WORKSPACE_AVAILABLE = False
    collaborative_bp = None
    initialize_collaborative_api = None
    EnhancedCollaborativeIntegration = None

# Import API integration
try:
    from api.mama_bear_orchestration_api import integrate_orchestration_with_app
    API_INTEGRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"API integration not available: {e}")
    API_INTEGRATION_AVAILABLE = False
    integrate_orchestration_with_app = None

# Try to import Mem0 for enhanced memory
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    MemoryClient = None

# Initialize Flask app
app = Flask(__name__)
settings = get_settings()
app.config['SECRET_KEY'] = settings.flask_secret_key
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5001"])

# ========== IMMEDIATE FIX FOR API REGISTRATION ==========
# This ensures the main chat endpoint is always available
logger.info("🔗 Registering fallback API endpoints...")

from flask import Blueprint, current_app

# Create a simple fallback blueprint for core endpoints
fallback_bp = Blueprint('mama_bear_fallback', __name__)

@fallback_bp.route('/api/mama-bear/chat', methods=['POST'])
def fallback_chat():
    """Fallback chat endpoint when orchestration isn't available"""
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        
        logger.info(f"📨 Fallback chat request: {message[:50]}...")
        
        # Check if orchestrator is available
        orchestrator = current_app.config.get('MAMA_BEAR_ORCHESTRATOR')
        
        if orchestrator:
            # Use orchestrator if available
            try:
                import asyncio
                result = asyncio.run(orchestrator.process_user_request(
                    message=message,
                    user_id=user_id,
                    page_context=page_context
                ))
                
                logger.info("✅ Used enhanced orchestrator")
                return jsonify({
                    'success': True,
                    'response': result,
                    'orchestrator_used': True,
                    'fallback_used': False,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Orchestrator failed, using fallback: {e}")
        
        # Basic fallback response using simple services
        try:
            from services import service_manager
            if service_manager and service_manager.services.get('mama_bear'):
                mama_bear = service_manager.services['mama_bear']
                
                # Use basic agent if available
                response = f"🐻 Hello! I received your message: '{message}'. I'm currently in basic mode while my enhanced systems come online. How can I help you today?"
                
                logger.info("✅ Used basic mama bear agent")
                return jsonify({
                    'success': True,
                    'response': {
                        'content': response,
                        'variant': 'basic',
                        'model': 'fallback_agent',
                        'timestamp': datetime.now().isoformat()
                    },
                    'orchestrator_used': False,
                    'fallback_used': 'basic_agent',
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            logger.error(f"Basic agent failed: {e}")
        
        # Ultimate fallback - simple response
        logger.info("Using ultimate fallback response")
        return jsonify({
            'success': True,
            'response': {
                'content': f"🐻 Hello! I received your message: '{message}'. I'm currently running in basic mode while the enhanced features are being set up. I'm here and ready to help!",
                'variant': 'basic',
                'model': 'fallback',
                'timestamp': datetime.now().isoformat()
            },
            'orchestrator_used': False,
            'fallback_used': 'simple',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in fallback chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Register the fallback blueprint immediately
app.register_blueprint(fallback_bp)
logger.info("✅ Fallback API endpoints registered")

# ========== END IMMEDIATE FIX ==========

# Register blueprints
# NOTE: Orchestration blueprint registered via integrate_orchestration_with_app()

# Initialize SocketIO
socketio = SocketIO(
    app, 
    cors_allowed_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5001"],
    async_mode='threading'
)

# NOTE: Orchestration blueprint registered conditionally in initialize_services()

# Initialize logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'mama_bear.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PodplaySanctuary")

# Global service status
services_initialized = False
mama_bear_orchestrator = None

async def initialize_sanctuary_services():
    """Initialize all sanctuary services with complete enhanced system"""
    global services_initialized, mama_bear_orchestrator
    
    try:
        logger.info("🚀 Initializing Complete Enhanced Podplay Sanctuary...")
        
        # Initialize basic services through the service manager first
        await initialize_all_services()
        
        # Initialize the complete enhanced system if available
        if ENHANCED_SYSTEM_AVAILABLE:
            logger.info("🌟 Initializing Complete Enhanced System with Mem0...")
            
            # Create model manager and Scrapybara client
            from services.mama_bear_model_manager import MamaBearModelManager
            from services.enhanced_scrapybara_integration import EnhancedScrapybaraManager
            
            model_manager = MamaBearModelManager()
            
            # Create enhanced Scrapybara manager
            scrapybara_config = {
                'scrapybara_api_key': os.getenv('SCRAPYBARA_API_KEY'),
                'scrapybara_base_url': os.getenv('SCRAPYBARA_BASE_URL', 'https://api.scrapybara.com/v1'),
                'enable_cua': True,
                'enable_collaboration': True
            }
            scrapybara_client = EnhancedScrapybaraManager(scrapybara_config)
            
            # Integrate complete enhanced system with Flask app
            integration_result = await integrate_complete_enhanced_system_with_app(
                app=app,
                socketio=socketio,
                model_manager=model_manager,
                scrapybara_client=scrapybara_client
            )
            
            if integration_result['success']:
                # Enhanced system integration is handled by the integration function
                # Components are already stored in the app by integrate_complete_enhanced_system_with_app
                
                # Store orchestrator globally for fallback compatibility  
                mama_bear_orchestrator = getattr(app, 'enhanced_orchestrator', None)
                if mama_bear_orchestrator:
                    app.config['MAMA_BEAR_ORCHESTRATOR'] = mama_bear_orchestrator
                
                logger.info("✅ Complete Enhanced System integrated successfully!")
                logger.info("🧠 Mem0-based persistent memory active")
                logger.info("🤖 Autonomous multi-agent orchestration online")
                logger.info("🎯 Scout.new-level capabilities enabled")
                logger.info("🔄 Redis completely replaced with Mem0 persistence")
                
                # Log available features
                features = integration_result.get('features', [])
                for feature in features:
                    logger.info(f"  ✓ {feature}")
                
                # Start background autonomous services
                enhanced_integration_instance = getattr(app, 'complete_enhanced_integration', None)
                if enhanced_integration_instance:
                    await enhanced_integration_instance.start_autonomous_background_services()
                    logger.info("🌟 Autonomous background services started")
                
            else:
                logger.error("❌ Enhanced system integration failed, falling back to basic services")
                error_details = integration_result.get('error', 'Unknown error')
                logger.error(f"Integration error: {error_details}")
                
                # Fallback to basic API integration if available
                if API_INTEGRATION_AVAILABLE and integrate_orchestration_with_app:
                    try:
                        integrate_orchestration_with_app(app, socketio)
                        logger.info("✅ Basic orchestration API endpoints registered")
                    except Exception as e:
                        logger.error(f"Failed to register basic API endpoints: {e}")
                
        else:
            logger.warning("⚠️ Complete Enhanced System not available - using basic services")
            
            # Fallback to basic API integration if available
            if API_INTEGRATION_AVAILABLE and integrate_orchestration_with_app:
                try:
                    integrate_orchestration_with_app(app, socketio)
                    logger.info("✅ Basic orchestration API endpoints registered")
                except Exception as e:
                    logger.error(f"Failed to register basic API endpoints: {e}")

        services_initialized = True
        
        logger.info("✅ All sanctuary services initialized successfully")
        logger.info("🐻 Mama Bear Sanctuary is ready with Scout.new-level autonomous capabilities!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Don't raise - allow fallback services to work
        services_initialized = True
        logger.info("⚠️ Running with minimal services")

def get_service_instances():
    """Get all service instances"""
    if not services_initialized:
        raise RuntimeError("Services not initialized. Call initialize_sanctuary_services() first.")
    
    # Get services directly from service manager (sync) - Fixed import
    from services import service_manager
    
    return {
        'mama_bear': service_manager.get_service('mama_bear'),
        'memory': service_manager.get_service('memory'),
        'scrapybara': service_manager.get_service('scrapybara'),
        'theme': service_manager.get_service('themes')
    }

# ==============================================================================
# MAMA BEAR ENDPOINTS
# ==============================================================================
# NOTE: Main chat endpoint moved to orchestration_bp blueprint

@app.route('/api/mama-bear/status', methods=['GET'])
def mama_bear_status():
    """Get current Mama Bear system status"""
    try:
        # Get the orchestrator instead of the mama_bear agent
        if hasattr(app, 'config') and 'MAMA_BEAR_ORCHESTRATOR' in app.config:
            orchestrator = app.config['MAMA_BEAR_ORCHESTRATOR']
            if orchestrator:
                # Get status from orchestrator (async method, so we need to handle it)
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                status = loop.run_until_complete(orchestrator.get_system_status())
                loop.close()
                
                return jsonify({
                    'success': True,
                    'status': status
                })
        
        # Fallback: Get basic service status
        services = get_service_instances()
        mama_bear = services['mama_bear']
        
        # Create a basic status response
        status = {
            'mama_bear_agent': {
                'type': type(mama_bear).__name__,
                'available': True,
                'timestamp': datetime.now().isoformat()
            },
            'services': {
                'memory': services.get('memory') is not None,
                'scrapybara': services.get('scrapybara') is not None,
                'themes': services.get('theme') is not None
            }
        }
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting Mama Bear status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# SCRAPYBARA VM ENDPOINTS
# ==============================================================================

@app.route('/api/vm/create', methods=['POST'])
async def create_vm_instance():
    """Create a new Scrapybara VM instance"""
    try:
        services = get_service_instances()
        scrapybara = services['scrapybara']
        
        data = request.json or {}
        project_config = data.get('config', {})
        instance_type = data.get('type', 'ubuntu')
        
        if scrapybara: # Add null check
            instance = await scrapybara.create_instance(
                instance_type=instance_type,
                config=project_config
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Scrapybara service not available'
            }), 503
        
        return jsonify({
            'success': True,
            'instance': instance
        })
        
    except Exception as e:
        logger.error(f"Error creating VM instance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vm/<instance_id>/action', methods=['POST'])
async def vm_action(instance_id):
    """Perform action on VM instance (start, stop, pause, resume)"""
    try:
        services = get_service_instances()
        scrapybara = services['scrapybara']
        
        data = request.json or {}
        action = data.get('action')
        
        if scrapybara: # Add null check
            result = await scrapybara.instance_action(instance_id, action)
        else:
            return jsonify({
                'success': False,
                'error': 'Scrapybara service not available'
            }), 503
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error performing VM action: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# SCOUT AGENT ENDPOINTS  
# ==============================================================================

@app.route('/api/scout/execute', methods=['POST'])
async def execute_scout_task():
    """Execute autonomous Scout task"""
    try:
        services = get_service_instances()
        scrapybara = services['scrapybara']
        
        data = request.json or {}
        task_description = data.get('description', '')
        files = data.get('files', [])
        user_id = data.get('user_id', 'nathan_sanctuary')
        
        # Start Scout task execution
        if scrapybara: # Add null check
            task_id = await scrapybara.execute_scout_task(
                task_description=task_description,
                files=files,
                user_id=user_id
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Scrapybara service not available'
            }), 503
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'status': 'started'
        })
        
    except Exception as e:
        logger.error(f"Error executing Scout task: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scout/task/<task_id>/status', methods=['GET'])
def get_scout_task_status(task_id):
    """Get status of Scout task"""
    try:
        services = get_service_instances()
        scrapybara = services['scrapybara']
        
        if scrapybara: # Add null check
            status = scrapybara.get_task_status(task_id)
        else:
            return jsonify({
                'success': False,
                'error': 'Scrapybara service not available'
            }), 503
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting Scout task status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# THEME AND PREFERENCES ENDPOINTS
# ==============================================================================

@app.route('/api/themes', methods=['GET'])
def get_themes():
    """Get available themes"""
    try:
        # Get theme manager directly from the service manager
        from services import service_manager
        if service_manager and service_manager.services.get('themes'):
            theme_mgr = service_manager.services['themes']
            themes = theme_mgr.get_all_themes()
            return jsonify({
                'success': True,
                'themes': themes
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Theme manager not initialized'
            }), 500
        
    except Exception as e:
        logger.error(f"Error getting themes: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/themes/<theme_name>', methods=['POST'])
def set_user_theme(theme_name):
    """Set user theme preference"""
    try:
        services = get_service_instances()
        theme_mgr = services['theme']
        
        data = request.json or {}
        user_id = data.get('user_id', 'nathan_sanctuary')
        
        if theme_mgr: # Add null check
            theme_mgr.set_user_theme(user_id, theme_name)
        else:
            return jsonify({
                'success': False,
                'error': 'Theme manager not available'
            }), 503
        
        return jsonify({
            'success': True,
            'theme': theme_name
        })
        
    except Exception as e:
        logger.error(f"Error setting theme: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# MEMORY MANAGEMENT ENDPOINTS
# ==============================================================================

@app.route('/api/memory/conversations', methods=['GET'])
def get_user_conversations():
    """Get user conversation history"""
    try:
        services = get_service_instances()
        memory = services['memory']
        
        user_id = request.args.get('user_id', 'nathan_sanctuary')
        limit = int(request.args.get('limit', 50))
        
        if memory: # Add null check
            conversations = memory.get_conversation_history(user_id, limit)
        else:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 503
        
        return jsonify({
            'success': True,
            'conversations': conversations
        })
        
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memory/preferences', methods=['GET'])
def get_user_preferences():
    """Get user preferences"""
    try:
        services = get_service_instances()
        memory = services['memory']
        
        user_id = request.args.get('user_id', 'nathan_sanctuary')
        if memory: # Add null check
            preferences = memory.get_user_preferences(user_id)
        else:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 503
        
        return jsonify({
            'success': True,
            'preferences': preferences
        })
        
    except Exception as e:
        logger.error(f"Error getting preferences: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memory/preferences', methods=['POST'])
def update_user_preferences():
    """Update user preferences"""
    try:
        services = get_service_instances()
        memory = services['memory']
        
        data = request.json or {}
        user_id = data.get('user_id', 'nathan_sanctuary')
        preferences = data.get('preferences', {})
        
        if memory: # Add null check
            memory.update_user_preferences(user_id, preferences)
        else:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 503
        
        return jsonify({
            'success': True,
            'message': 'Preferences updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# SERVICE HEALTH AND STATUS ENDPOINTS
# ==============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        status = get_service_status()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'services': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/service/restart', methods=['POST'])
async def restart_services():
    """Restart all services"""
    try:
        await shutdown_all_services()
        await initialize_sanctuary_services()
        
        return jsonify({
            'success': True,
            'message': 'Services restarted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error restarting services: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# FILE UPLOAD AND MULTIMODAL ENDPOINTS
# ==============================================================================

@app.route('/api/upload', methods=['POST'])
async def upload_file():
    """Handle file uploads for multimodal processing"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
            
        file = request.files['file']
        if not file.filename or file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Save file temporarily
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)
        
        # Process with Mama Bear if needed
        services = get_service_instances()
        mama_bear = services['mama_bear']
        
        # Return file info for further processing
        return jsonify({
            'success': True,
            'file_path': file_path,
            'filename': file.filename,
            'size': os.path.getsize(file_path)
        })
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# WEBSOCKET HANDLERS
# ==============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    emit('connection_established', {
        'status': 'connected',
        'sanctuary_version': '1.0.0',
        'mama_bear_ready': True
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

@socketio.on('mama_bear_message')
async def handle_mama_bear_message(data):
    """Handle real-time Mama Bear messages"""
    try:
        services = get_service_instances()
        mama_bear = services['mama_bear']
        
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        user_id = data.get('user_id', 'nathan_sanctuary')
        
        # Process message with Mama Bear
        if mama_bear: # Add null check
            response = await mama_bear.process_message(
                message=message,
                page_context=page_context,
                user_id=user_id
            )
        else:
            emit('error', {'message': 'Mama Bear agent not available'})
            return
        
        # Emit response back to client
        emit('mama_bear_response', {
            'content': response['content'],
            'variant': response['variant'],
            'model': response['model'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in WebSocket message handler: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('scout_task_update')
def handle_scout_update(data):
    """Handle Scout task progress updates"""
    try:
        task_id = data.get('task_id')
        progress = data.get('progress', {})
        
        # Broadcast progress to all connected clients
        emit('scout_progress', {
            'task_id': task_id,
            'progress': progress,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)
        
    except Exception as e:
        logger.error(f"Error handling Scout update: {str(e)}")

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'sanctuary_message': '🐻 Mama Bear couldn\'t find that path. Try a different route!'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'sanctuary_message': '🐻 Mama Bear encountered an issue. She\'s working to fix it!'
    }), 500

# ==============================================================================
# APPLICATION STARTUP
# ==============================================================================

def create_app():
    """Application factory function"""
    # Initialize services when app is created
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initialize_sanctuary_services())
    
    return app

if __name__ == '__main__':
    # Initialize services
    import asyncio
    
    async def startup():
        """Async startup function"""
        logger.info("🚀 Starting Podplay Sanctuary...")
        await initialize_sanctuary_services()
        logger.info("🐻 Mama Bear is ready to help!")
    
    # Run startup
    asyncio.run(startup())
    
    # Start the Sanctuary
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('BACKEND_PORT', 5001)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )

# ==============================================================================
# ENHANCED AUTONOMOUS MAMA BEAR ENDPOINTS
# ==============================================================================

@app.route('/api/mama-bear/autonomous/chat', methods=['POST'])
def enhanced_autonomous_chat():
    """Enhanced autonomous chat with Scout.new-level capabilities"""
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        session_id = data.get('session_id')
        
        logger.info(f"🚀 Enhanced autonomous chat request: {message[:50]}...")
        
        # Check if complete enhanced integration is available
        complete_integration = getattr(app, 'complete_enhanced_integration', None)
        
        if complete_integration and complete_integration.is_initialized:
            # Use autonomous processing with full enhanced capabilities
            try:
                import asyncio
                result = asyncio.run(complete_integration.process_autonomous_request(
                    message=message,
                    user_id=user_id,
                    session_id=session_id,
                    page_context=page_context
                ))
                
                logger.info("✅ Used complete enhanced autonomous system")
                return jsonify({
                    'success': True,
                    'response': result['response'],
                    'autonomous_features': result.get('autonomous_features', {}),
                    'session_id': result.get('session_id'),
                    'system_health': result.get('system_health', {}),
                    'enhanced_processing': True,
                    'mem0_persistence': True,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Enhanced autonomous system failed, using fallback: {e}")
        
        # Fallback to basic orchestrator if available
        orchestrator = app.config.get('MAMA_BEAR_ORCHESTRATOR')
        if orchestrator:
            try:
                import asyncio
                result = asyncio.run(orchestrator.process_user_request(
                    message=message,
                    user_id=user_id,
                    page_context=page_context
                ))
                
                logger.info("✅ Used basic orchestrator fallback")
                return jsonify({
                    'success': True,
                    'response': result,
                    'enhanced_processing': False,
                    'fallback_used': 'basic_orchestrator',
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Basic orchestrator failed: {e}")
        
        # Ultimate fallback - simple response
        logger.info("Using ultimate fallback for enhanced autonomous chat")
        return jsonify({
            'success': True,
            'response': {
                'content': f"🐻 Hello! I received your message: '{message}'. My enhanced autonomous systems are currently initializing, but I'm here to help! Try the regular chat endpoint for now.",
                'variant': 'enhanced_fallback',
                'model': 'fallback',
                'timestamp': datetime.now().isoformat()
            },
            'enhanced_processing': False,
            'fallback_used': 'simple',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in enhanced autonomous chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'enhanced_processing': False,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mama-bear/autonomous/status', methods=['GET'])
def enhanced_autonomous_status():
    """Get comprehensive autonomous system status with Mem0 integration"""
    try:
        complete_integration = getattr(app, 'complete_enhanced_integration', None)
        
        if complete_integration and complete_integration.is_initialized:
            import asyncio
            status = asyncio.run(complete_integration.get_comprehensive_system_status())
            
            return jsonify({
                'success': True,
                'status': status,
                'enhanced_features': {
                    'mem0_persistence': True,
                    'autonomous_orchestration': True,
                    'scout_level_capabilities': True,
                    'redis_replaced': True
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Enhanced autonomous system not initialized',
                'fallback_available': app.config.get('MAMA_BEAR_ORCHESTRATOR') is not None,
                'enhanced_features': {
                    'mem0_persistence': False,
                    'autonomous_orchestration': False,
                    'scout_level_capabilities': False,
                    'redis_replaced': False
                },
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error getting enhanced autonomous status: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mama-bear/system/features', methods=['GET'])
def get_system_features():
    """Get available system features and capabilities"""
    try:
        complete_integration = getattr(app, 'complete_enhanced_integration', None)
        basic_orchestrator = app.config.get('MAMA_BEAR_ORCHESTRATOR')
        
        features = {
            'basic_chat': True,
            'fallback_responses': True,
            'enhanced_autonomous_system': complete_integration is not None and complete_integration.is_initialized,
            'basic_orchestration': basic_orchestrator is not None,
            'mem0_persistence': False,
            'autonomous_agents': False,
            'intelligent_checkpointing': False,
            'adaptive_learning': False,
            'proactive_assistance': False,
            'redis_replaced': True  # Redis is now completely replaced
        }
        
        if complete_integration and complete_integration.is_initialized:
            features.update({
                'mem0_persistence': True,
                'autonomous_agents': True,
                'intelligent_checkpointing': True,
                'adaptive_learning': True,
                'proactive_assistance': True,
                'multi_agent_coordination': True,
                'workflow_intelligence': True,
                'real_time_collaboration': True,
                'scout_level_capabilities': True,
                'redis_replaced': True
            })
        
        return jsonify({
            'success': True,
            'features': features,
            'recommendations': {
                'primary_endpoint': '/api/mama-bear/autonomous/chat' if features['enhanced_autonomous_system'] else '/api/mama-bear/chat',
                'fallback_endpoint': '/api/mama-bear/chat',
                'status_endpoint': '/api/mama-bear/autonomous/status' if features['enhanced_autonomous_system'] else '/api/mama-bear/status'
            },
            'memory_system': 'Mem0' if features['mem0_persistence'] else 'Basic',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting system features: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
