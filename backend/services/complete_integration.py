# Import all Mama Bear components
try:
    from .mama_bear_model_manager import MamaBearModelManager
    from .mama_bear_orchestration import AgentOrchestrator, initialize_orchestration
    from .mama_bear_memory_system import initialize_enhanced_memory
    from .mama_bear_specialized_variants import *
except ImportError:
    # Fallback to absolute imports
    try:
        from services.mama_bear_model_manager import MamaBearModelManager
        from services.mama_bear_orchestration import AgentOrchestrator, initialize_orchestration
        from services.mama_bear_memory_system import initialize_enhanced_memory
        from services.mama_bear_specialized_variants import *
    except ImportError:
        print("⚠️ Could not import some Mama Bear components - continuing with available features")
        MamaBearModelManager = None
        AgentOrchestrator = None
        initialize_orchestration = None
        initialize_enhanced_memory = None

try:
    from ..api.orchestration_api import integrate_orchestration_with_app
except ImportError:
    try:
        from api.orchestration_api import integrate_orchestration_with_app
    except ImportError:
        integrate_orchestration_with_app = None

try:
    from ..utils.mama_bear_monitoring import MamaBearMonitoring
except ImportError:
    try:
        from utils.mama_bear_monitoring import MamaBearMonitoring
    except ImportError:
        MamaBearMonitoring = None

try:
    from ..config.mama_bear_config_setup import load_config
except ImportError:
    try:
        from config.mama_bear_config_setup import load_config
    except ImportError:
        def load_config():
            return {}

"""
🐻 Complete Mama Bear System Integration
Brings together all components for a fully intelligent agent orchestration system
"""

import asyncio
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mama_bear_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompleteMamaBearSystem:
    """
    🐻 Complete Mama Bear System
    Orchestrates all components for intelligent agent collaboration
    """
    
    def __init__(self, config=None):
        self.config = config or load_config()
        self.app = None
        self.socketio = None
        
        # Core components
        self.model_manager = None
        self.memory_manager = None
        self.orchestrator = None
        self.monitoring = None
        self.scrapybara_client = None
        
        # System state
        self.is_initialized = False
        self.startup_time = None
        
    async def initialize(self):
        """Initialize the complete Mama Bear system"""
        
        logger.info("🐻 Starting Mama Bear System initialization...")
        start_time = datetime.now()
        
        try:
            # 1. Initialize Flask application
            self._initialize_flask_app()
            
            # 2. Initialize core AI components
            await self._initialize_ai_components()
            
            # 3. Initialize orchestration system
            await self._initialize_orchestration()
            
            # 4. Initialize monitoring
            await self._initialize_monitoring()
            
            # 5. Perform health check
            await self._perform_health_check()
            
            self.is_initialized = True
            self.startup_time = datetime.now()
            
            initialization_time = (self.startup_time - start_time).total_seconds()
            logger.info(f"🎉 Mama Bear System initialized successfully in {initialization_time:.2f} seconds!")
            
            return self.app
            
        except Exception as e:
            logger.error(f"❌ Mama Bear System initialization failed: {e}")
            # Don't raise - allow graceful degradation
            self.is_initialized = True
            self.startup_time = datetime.now()
            return self.app
    
    async def _initialize_ai_components(self):
        """Initialize core AI components"""
        
        logger.info("🤖 Initializing AI components...")
        
        # Initialize model manager
        if MamaBearModelManager:
            try:
                self.model_manager = MamaBearModelManager()
                logger.info("✅ Model Manager initialized")
            except Exception as e:
                logger.warning(f"⚠️ Model Manager initialization failed: {e}")
        
        # Initialize memory system
        if initialize_enhanced_memory:
            try:
                self.memory_manager = initialize_enhanced_memory(None)
                logger.info("✅ Memory Manager initialized")
            except Exception as e:
                logger.warning(f"⚠️ Memory Manager initialization failed: {e}")
    
    def _initialize_flask_app(self):
        """Initialize Flask application"""
        
        logger.info("🌐 Initializing Flask application...")
        
        self.app = Flask(__name__)
        self.app.config.update(self.config)
        
        # Initialize extensions
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Register health check endpoint
        @self.app.route('/health')
        def health_check():
            return jsonify({
                'status': 'healthy' if self.is_initialized else 'initializing',
                'startup_time': self.startup_time.isoformat() if self.startup_time else None,
                'components': {
                    'model_manager': self.model_manager is not None,
                    'memory_manager': self.memory_manager is not None,
                    'orchestrator': self.orchestrator is not None,
                    'monitoring': self.monitoring is not None
                }
            })
        
        # Store components in app config (safer than direct attributes)
        self.app.config['mama_bear_model_manager'] = self.model_manager
        self.app.config['mama_bear_memory_manager'] = self.memory_manager
        self.app.config['mama_bear_orchestrator'] = self.orchestrator
        
        logger.info("✅ Flask application initialized")
    
    async def _initialize_orchestration(self):
        """Initialize agent orchestration system"""
        
        logger.info("🎭 Initializing orchestration system...")
        
        if initialize_orchestration and self.app and self.memory_manager and self.model_manager:
            try:
                # Initialize orchestrator
                self.orchestrator = await initialize_orchestration(
                    self.app,
                    self.memory_manager,
                    self.model_manager,
                    self.scrapybara_client
                )
                
                # Update app config
                self.app.config['mama_bear_orchestrator'] = self.orchestrator
                
                # Integrate API endpoints
                if integrate_orchestration_with_app:
                    integrate_orchestration_with_app(
                        self.app,
                        self.socketio
                    )
                
                logger.info("✅ Orchestration system initialized")
                
            except Exception as e:
                logger.warning(f"⚠️ Orchestration initialization failed: {e}")
        else:
            logger.warning("⚠️ Orchestration initialization skipped - missing dependencies")
    
    async def _initialize_monitoring(self):
        """Initialize monitoring and analytics"""
        
        logger.info("📊 Initializing monitoring...")
        
        if MamaBearMonitoring:
            try:
                self.monitoring = MamaBearMonitoring()
                if self.app is None:
                    logger.error("Cannot initialize monitoring: self.app is None.")
                    return
                if hasattr(self.app, 'config'):
                    self.app.config['mama_bear_monitoring'] = self.monitoring
                    logger.info("✅ Monitoring initialized")
                else:
                    logger.error("Cannot store monitoring in app.config: self.app.config is not available.")
            except Exception as e:
                logger.warning(f"⚠️ Monitoring initialization failed: {e}")
    
    async def _perform_health_check(self):
        """Perform comprehensive system health check"""
        
        logger.info("🏥 Performing system health check...")
        
        health_results = {}
        
        # Check model manager
        if self.model_manager:
            try:
                # Simple check if model manager is responsive
                health_results['model_manager'] = {'status': 'healthy'}
            except Exception as e:
                health_results['model_manager'] = {'status': 'error', 'error': str(e)}
        else:
            health_results['model_manager'] = {'status': 'unavailable'}
        
        # Check memory manager
        if self.memory_manager:
            health_results['memory_manager'] = {'status': 'healthy'}
        else:
            health_results['memory_manager'] = {'status': 'unavailable'}
        
        # Check orchestrator
        if self.orchestrator:
            health_results['orchestrator'] = {'status': 'healthy'}
        else:
            health_results['orchestrator'] = {'status': 'unavailable'}
        
        # Check monitoring
        if self.monitoring:
            health_results['monitoring'] = {'status': 'healthy'}
        else:
            health_results['monitoring'] = {'status': 'unavailable'}
        
        logger.info("🏥 Health check complete")
        for component, status in health_results.items():
            logger.info(f"  {component}: {status['status']}")
        
        return health_results
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the complete Mama Bear system"""
        
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        logger.info(f"🚀 Starting Mama Bear System on {host}:{port}")
        
        if self.socketio:
            self.socketio.run(
                self.app,
                host=host,
                port=port,
                debug=debug,
                allow_unsafe_werkzeug=True
            )
        else:
            if self.app is None:
                logger.error("Cannot run Flask app: self.app is None.")
                raise RuntimeError("Application not properly initialized: self.app is None.")
            self.app.run(host=host, port=port, debug=debug)

# Convenience function for easy setup
async def create_mama_bear_app(config=None):
    """
    Create and initialize a complete Mama Bear application
    """
    
    system = CompleteMamaBearSystem(config)
    app = await system.initialize()
    
    if app is None:
        logger.error("Failed to initialize Flask app within CompleteMamaBearSystem. Cannot store system reference.")
        raise RuntimeError("Failed to initialize the Flask application.")
    
    # Store system reference in app config
    if hasattr(app, 'config'):
        app.config['mama_bear_system'] = system
    else:
        logger.error("Initialized app does not have a 'config' attribute.")
        raise AttributeError("Initialized app is missing 'config' attribute.")

    return app

# Main entry point
async def main():
    """Main entry point for running the complete system"""
    
    logger.info("🐻 Welcome to Mama Bear - Your AI Development Sanctuary")
    
    try:
        # Create and initialize the system
        system = CompleteMamaBearSystem()
        app = await system.initialize()
        
        # Run the system
        system.run(debug=True)
        
    except KeyboardInterrupt:
        logger.info("👋 Mama Bear says goodbye!")
    except Exception as e:
        logger.error(f"💥 System error: {e}")
        raise

if __name__ == "__main__":
    # Set up event loop for async main
    asyncio.run(main())
