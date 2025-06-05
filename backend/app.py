"""
🐻 Podplay Sanctuary - Enhanced Mama Bear Flask Application
Neurodivergent-friendly development sanctuary with 7 Mama Bear variants,
3 sensory-friendly themes, and instant cloud development environments
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import redis

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

# Import enhanced Mama Bear orchestration
try:
    from services.mama_bear_orchestration import AgentOrchestrator
    from services.mama_bear_memory_system import EnhancedMemoryManager, initialize_enhanced_memory
    from services.enhanced_scrapybara_integration import EnhancedScrapybaraManager
    from services.complete_integration import CompleteMamaBearSystem
    ENHANCED_ORCHESTRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced orchestration not available: {e}")
    ENHANCED_ORCHESTRATION_AVAILABLE = False
    AgentOrchestrator = None
    EnhancedMemoryManager = None
    EnhancedScrapybaraManager = None
    CompleteMamaBearSystem = None
    initialize_workflow_intelligence = None
    create_collaboration_orchestrator = None
    initialize_enhanced_memory = None

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
    """Initialize all sanctuary services using the service manager"""
    global services_initialized, mama_bear_orchestrator
    
    try:
        logger.info("🚀 Initializing Podplay Sanctuary services...")
        
        # Initialize basic services through the service manager
        await initialize_all_services()
        
        # Initialize enhanced Mama Bear orchestration if available
        if ENHANCED_ORCHESTRATION_AVAILABLE:
            logger.info("🐻 Initializing Enhanced Mama Bear Orchestration...")
            
            # Initialize Mem0 if available
            mem0_client = None
            if MEM0_AVAILABLE and MemoryClient:
                try:
                    mem0_client = MemoryClient()
                    logger.info("✅ Mem0 client initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize Mem0: {e}")
                    mem0_client = None
            
            # Initialize enhanced memory system
            enhanced_memory = None
            if EnhancedMemoryManager:
                try:
                    enhanced_memory = EnhancedMemoryManager(
                        mem0_client=mem0_client,
                        local_storage_path='./mama_bear_memory'
                    )
                    logger.info("✅ Enhanced memory system initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize enhanced memory: {e}")
                    enhanced_memory = None
            
            # Initialize enhanced Scrapybara manager
            enhanced_scrapybara = None
            if EnhancedScrapybaraManager:
                try:
                    scrapybara_config = {
                        'scrapybara_api_key': os.getenv('SCRAPYBARA_API_KEY'),
                        'scrapybara_base_url': os.getenv('SCRAPYBARA_BASE_URL', 'https://api.scrapybara.com/v1'),
                        'enable_cua': True,
                        'enable_collaboration': True
                    }
                    enhanced_scrapybara = EnhancedScrapybaraManager(scrapybara_config)
                    logger.info("✅ Enhanced Scrapybara manager initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize enhanced Scrapybara: {e}")
                    enhanced_scrapybara = get_scrapybara_manager() # Fallback to basic
            
            # Initialize orchestrator with enhanced components
            if AgentOrchestrator:
                # Import and create MamaBearModelManager for orchestration
                from services.mama_bear_model_manager import MamaBearModelManager
                
                mama_bear_orchestrator = AgentOrchestrator(
                    memory_manager=enhanced_memory or get_memory_manager(),
                    model_manager=MamaBearModelManager(),
                    scrapybara_client=enhanced_scrapybara or get_scrapybara_manager()
                )
                
                # Store orchestrator globally and in app context
            globals()['mama_bear_orchestrator'] = mama_bear_orchestrator
            # Store in app config instead of as attribute
            app.config['MAMA_BEAR_ORCHESTRATOR'] = mama_bear_orchestrator
            
            # Initialize enhanced API endpoints
            if API_INTEGRATION_AVAILABLE and integrate_orchestration_with_app:
                integrate_orchestration_with_app(app, socketio)
                logger.info("✅ Enhanced orchestration API endpoints registered")
            else:
                logger.warning("Enhanced API integration not available")
            
            logger.info("✅ Enhanced Mama Bear Orchestration initialized")
        
        services_initialized = True
        
        logger.info("✅ All sanctuary services initialized successfully")
        logger.info("🐻 Enhanced Mama Bear Orchestration ready!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {str(e)}")
        # Don't raise - allow basic services to work
        services_initialized = True
        logger.info("⚠️ Running with basic services only")

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
        
        instance = await scrapybara.create_instance(
            instance_type=instance_type,
            config=project_config
        )
        
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
        
        result = await scrapybara.instance_action(instance_id, action)
        
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
        task_id = await scrapybara.execute_scout_task(
            task_description=task_description,
            files=files,
            user_id=user_id
        )
        
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
        
        status = scrapybara.get_task_status(task_id)
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
        
        theme_mgr.set_user_theme(user_id, theme_name)
        
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
        
        conversations = memory.get_conversation_history(user_id, limit)
        
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
        preferences = memory.get_user_preferences(user_id)
        
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
        
        memory.update_user_preferences(user_id, preferences)
        
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
        response = await mama_bear.process_message(
            message=message,
            page_context=page_context,
            user_id=user_id
        )
        
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
