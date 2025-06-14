# backend/services/complete_enhanced_integration.py
"""
🐻 Complete Enhanced Integration System
Integrates all enhanced components - replaces Redis with Mem0 for 
Scout.new-level autonomous agent capabilities with persistent sessions
"""

import asyncio
import logging
from datetime import datetime
import os
from typing import Dict, Any, Optional
import json
from flask import request # Import flask.request
from .enhanced_session_manager import SessionType # Import SessionType

from .enhanced_memory_system import EnhancedMemoryManager
from .enhanced_orchestration_system import EnhancedAgentOrchestrator
from .enhanced_session_manager import EnhancedSessionManager
from .mama_bear_model_manager import MamaBearModelManager

logger = logging.getLogger(__name__)

class CompleteEnhancedIntegration:
    """
    Complete integration of all enhanced Mama Bear systems with Mem0-based persistence
    and autonomous agent capabilities
    """
    
    def __init__(self):
        self.memory_manager = None
        self.orchestrator = None
        self.session_manager = None
        self.model_manager = None
        self.scrapybara_client = None
        self.is_initialized = False
        self.autonomous_features_enabled = False
        
        # System health monitoring
        self.system_health = {
            'memory_system': False,
            'orchestration_system': False,
            'session_management': False,
            'model_management': False,
            'autonomous_capabilities': False
        }
    
    async def initialize_complete_system(self, model_manager, scrapybara_client):
        """Initialize the complete enhanced system with all components"""
        
        try:
            logger.info("🚀 Initializing Complete Enhanced Mama Bear System...")
            
            # Store external dependencies
            self.model_manager = model_manager
            self.scrapybara_client = scrapybara_client
            
            # Initialize Enhanced Memory System with Mem0
            await self._initialize_enhanced_memory_system()
            
            # Initialize Enhanced Session Manager
            await self._initialize_enhanced_session_manager()
            
            # Initialize Enhanced Orchestration System
            await self._initialize_enhanced_orchestration_system()
            
            # Enable autonomous features
            await self._enable_autonomous_features()
            
            # Setup system health monitoring
            await self._setup_system_health_monitoring()
            
            # Start background processes
            await self._start_background_processes()
            
            self.is_initialized = True
            logger.info("✅ Complete Enhanced Mama Bear System initialized successfully!")
            
            return {
                'success': True,
                'components': {
                    'memory_manager': self.memory_manager,
                    'orchestrator': self.orchestrator,
                    'session_manager': self.session_manager
                },
                'autonomous_features': self.autonomous_features_enabled,
                'system_health': self.system_health
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize complete enhanced system: {e}")
            raise
    
    async def _initialize_enhanced_memory_system(self):
        """Initialize the enhanced memory system with Mem0 integration"""
        
        logger.info("🧠 Initializing Enhanced Memory System...")
        
        # Create Mem0 client
        mem0_client = None
        try:
            from mem0 import MemoryClient
            mem0_api_key = os.getenv('MEM0_API_KEY', 'm0-tBwWs1ygkxcbEiVvX6iXdwiJ42epw8a3wyoEUlpg')
            mem0_client = MemoryClient(api_key=mem0_api_key)
            logger.info("✅ Mem0 client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize Mem0 client: {e}")
        
        # Initialize enhanced memory manager
        self.memory_manager = EnhancedMemoryManager(
            mem0_client=mem0_client,
            local_storage_path="/home/woody/Documents/podplay-claude/backend/mama_bear_memory"
        )
        
        # Give it a moment to complete async initialization
        await asyncio.sleep(0.1)
        
        self.system_health['memory_system'] = True
        logger.info("✅ Enhanced Memory System initialized with Mem0 integration")
    
    async def _initialize_enhanced_session_manager(self):
        """Initialize the enhanced session manager"""
        
        
        logger.info("🔄 Initializing Enhanced Session Manager...")
        
        # Prepare config for session manager
        session_config = {
            "MEM0_API_KEY": os.getenv('MEM0_API_KEY', 'm0-tBwWs1ygkxcbEiVvX6iXdwiJ42epw8a3wyoEUlpg'),
            "storage_path": "/home/woody/Documents/podplay-claude/backend/mama_bear_memory/sessions",
            "auto_checkpoint_interval": 300,  # 5 minutes
            "max_runtime_hours": 24
        }
        
        self.session_manager = EnhancedSessionManager(config=session_config)
        
        # Give it a moment for any async initialization
        await asyncio.sleep(0.1)
        
        self.system_health['session_management'] = True
        logger.info("✅ Enhanced Session Manager initialized with Mem0 persistence")
    
    async def _initialize_enhanced_orchestration_system(self):
        """Initialize the enhanced orchestration system"""
        
        logger.info("🎭 Initializing Enhanced Orchestration System...")
        
        self.orchestrator = EnhancedAgentOrchestrator(
            memory_manager=self.memory_manager,
            model_manager=self.model_manager,
            scrapybara_client=self.scrapybara_client
        )
        
        # Initialize workflow intelligence systems
        await self.orchestrator.initialize_workflow_systems()
        
        self.system_health['orchestration_system'] = True
        self.system_health['model_management'] = True
        logger.info("✅ Enhanced Orchestration System initialized with specialized agents")
    
    async def _enable_autonomous_features(self):
        """Enable advanced autonomous agent features"""
        
        logger.info("🤖 Enabling Autonomous Features...")
        
        # Enable proactive agent behaviors
        if self.orchestrator:
            await self.orchestrator.enable_proactive_behaviors()
        
        # Setup intelligent checkpointing
        if self.session_manager:
            await self.session_manager.enable_intelligent_checkpointing()
        
        # Enable adaptive learning (assuming it's a method on memory_manager)
        if self.memory_manager:
            await self.memory_manager.enable_adaptive_learning()
        
        # Setup multi-agent collaboration
        if self.orchestrator:
            await self.orchestrator.enable_advanced_collaboration()
        
        self.autonomous_features_enabled = True
        self.system_health['autonomous_capabilities'] = True
        logger.info("✅ Autonomous features enabled - Scout.new-level capabilities active")
    
    async def _setup_system_health_monitoring(self):
        """Setup comprehensive system health monitoring"""
        
        logger.info("❤️ Setting up System Health Monitoring...")
        
        # Create monitoring tasks for each component
        asyncio.create_task(self._monitor_memory_system_health())
        asyncio.create_task(self._monitor_orchestration_health())
        asyncio.create_task(self._monitor_session_health())
        asyncio.create_task(self._monitor_autonomous_features())
        
        logger.info("✅ System health monitoring active")
    
    async def _start_background_processes(self):
        """Start all background processes for autonomous operation"""
        
        logger.info("⚙️ Starting Background Processes...")
        
        # Memory system background tasks (using actual method names that exist)
        if self.memory_manager:
            if hasattr(self.memory_manager, '_pattern_analysis_loop'):
                asyncio.create_task(self.memory_manager._pattern_analysis_loop())
            if hasattr(self.memory_manager, '_memory_consolidation_loop'):
                asyncio.create_task(self.memory_manager._memory_consolidation_loop())
        
        # Orchestration background tasks
        if self.orchestrator:
            if hasattr(self.orchestrator, '_monitor_system_health'):
                asyncio.create_task(self.orchestrator._monitor_system_health())
        
        # Session management background tasks
        if self.session_manager:
            if hasattr(self.session_manager, 'cleanup_expired_sessions'): # Corrected to public method
                asyncio.create_task(self.session_manager.cleanup_expired_sessions())
        
        logger.info("✅ Background processes started for autonomous operation")
    
    async def process_autonomous_request(self, message: str, user_id: str, session_id: Optional[str] = None, page_context: str = 'main_chat') -> Dict[str, Any]:
        """
        Process a user request with full autonomous capabilities
        """
        
        if not self.is_initialized:
            raise RuntimeError("Complete enhanced system not initialized")
        
        try:
            # Create or get session
            if not session_id:
                if self.session_manager: # Add null check for session_manager
                    session = await self.session_manager.create_session( # Corrected method name
                        user_id=user_id,
                        session_type=SessionType.CHAT, # Use the Enum member
                        metadata={'page_context': page_context} # Use metadata instead of initial_context
                    )
                    session_id = session.session_id # Access session_id from object
                else:
                    raise RuntimeError("Session manager not initialized for autonomous session creation.")

            # Get enhanced context from memory system
            context = {}
            if self.memory_manager: # Add null check for memory_manager
                context = await self.memory_manager.get_enhanced_context(
                    user_id=user_id,
                    session_id=session_id,
                    include_patterns=True,
                    include_learning_insights=True
                )
            
            # Process with enhanced orchestration
            result = {}
            if self.orchestrator: # Add null check for orchestrator
                result = await self.orchestrator.process_autonomous_request(
                    message=message,
                    user_id=user_id,
                    session_id=session_id,
                    context=context,
                    page_context=page_context
                )
            
            # Save interaction with enhanced metadata
            if self.memory_manager: # Add null check for memory_manager
                await self.memory_manager.save_enhanced_interaction(
                    user_id=user_id,
                    session_id=session_id,
                    message=message,
                    response=result,
                    metadata={
                        'autonomous_processing': True,
                        'decision_analysis': result.get('decision_analysis'),
                        'agents_involved': result.get('agents_involved', []),
                        'learning_opportunity': result.get('learning_opportunity'),
                        'page_context': page_context
                    }
                )
            
            # Create checkpoint if significant interaction
            if self.session_manager and result.get('create_checkpoint', False): # Add null check for session_manager
                await self.session_manager.create_intelligent_checkpoint(
                    session_id=session_id,
                    description=f"autonomous_interaction_{datetime.now().timestamp()}", # Corrected argument name
                    state_data={ # Pass metadata as state_data if it's a checkpoint state
                        'interaction_significance': result.get('significance_score', 0.5),
                        'user_request': message[:100],
                        'agents_involved': result.get('agents_involved', [])
                    }
                )
            
            return {
                'success': True,
                'response': result,
                'session_id': session_id,
                'autonomous_features': {
                    'decision_analysis_performed': True,
                    'multi_agent_coordination': len(result.get('agents_involved', [])) > 1,
                    'learning_applied': result.get('learning_applied', False),
                    'proactive_suggestions': result.get('proactive_suggestions', [])
                },
                'system_health': self.system_health
            }
            
        except Exception as e:
            logger.error(f"Error in autonomous request processing: {e}")
            
            # Fallback processing
            fallback_result = await self._process_fallback_request(message, user_id, session_id)
            return {
                'success': False,
                'response': fallback_result,
                'error': str(e),
                'fallback_used': True
            }
    
    async def _process_fallback_request(self, message: str, user_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Fallback processing when autonomous systems fail"""
        
        try:
            # Basic response using model manager
            result = {}
            if self.model_manager: # Add null check for model_manager
                result = await self.model_manager.get_response(
                    prompt=f"User request: {message}\n\nPlease provide a helpful response as Mama Bear.",
                    mama_bear_variant='main_chat',
                    required_capabilities=['chat']
                )
            
                return {
                    'content': result.get('response', "🐻 I'm having some technical difficulties, but I'm here to help!"),
                    'fallback_mode': True,
                    'model_used': result.get('model_used')
                }
            else:
                return {
                    'content': "🐻 My core model manager is not available. Please check the backend setup.",
                    'fallback_mode': True,
                    'error': "Model manager not initialized"
                }

            
        except Exception as e:
            logger.error(f"Fallback processing also failed: {e}")
            return {
                'content': "🐻 I'm experiencing some technical issues right now, but I'm working on fixing them! Please try again in a moment.",
                'fallback_mode': True,
                'error': str(e)
            }
    
    async def get_comprehensive_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all enhanced systems"""
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'system_initialized': self.is_initialized,
            'autonomous_features_enabled': self.autonomous_features_enabled,
            'component_health': self.system_health.copy()
        }
        
        if self.is_initialized:
            # Get detailed component statuses
            if self.memory_manager and hasattr(self.memory_manager, 'get_system_health'): # Add hasattr check
                status['memory_system'] = await self.memory_manager.get_system_health()
            else:
                status['memory_system'] = {'status': 'unavailable', 'message': 'Memory manager not initialized or missing get_system_health'}
            
            if self.orchestrator and hasattr(self.orchestrator, 'get_system_health'): # Add hasattr check
                status['orchestration_system'] = await self.orchestrator.get_system_health()
            else:
                status['orchestration_system'] = {'status': 'unavailable', 'message': 'Orchestration manager not initialized or missing get_system_health'}
            
            if self.session_manager and hasattr(self.session_manager, 'get_system_health'): # Add hasattr check
                status['session_management'] = await self.session_manager.get_system_health()
            else:
                status['session_management'] = {'status': 'unavailable', 'message': 'Session manager not initialized or missing get_system_health'}
        
        return status
    
    # Health monitoring methods
    async def _monitor_memory_system_health(self):
        """Monitor memory system health"""
        while True:
            try:
                if self.memory_manager:
                    # Simple health check - just verify the object exists and has basic attributes
                    health = hasattr(self.memory_manager, 'mem0_client') and self.memory_manager.mem0_client is not None
                    self.system_health['memory_system'] = health
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Memory system health check failed: {e}")
                self.system_health['memory_system'] = False
                await asyncio.sleep(30)
    
    async def _monitor_orchestration_health(self):
        """Monitor orchestration system health"""
        while True:
            try:
                if self.orchestrator:
                    # Simple health check - verify orchestrator has required components
                    health = (hasattr(self.orchestrator, 'agents') and 
                             hasattr(self.orchestrator, 'memory') and
                             hasattr(self.orchestrator, 'model_manager'))
                    self.system_health['orchestration_system'] = health
                
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Orchestration system health check failed: {e}")
                self.system_health['orchestration_system'] = False
                await asyncio.sleep(30)
    
    async def _monitor_session_health(self):
        """Monitor session management health"""
        while True:
            try:
                if self.session_manager:
                    # Simple health check - verify session manager has memory client  
                    health = hasattr(self.session_manager, 'memory') and self.session_manager.memory is not None
                    self.system_health['session_management'] = health
                
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Session management health check failed: {e}")
                self.system_health['session_management'] = False
                await asyncio.sleep(30)
    
    async def _monitor_autonomous_features(self):
        """Monitor autonomous features health"""
        while True:
            try:
                # Check if all autonomous features are functioning
                autonomous_health = (
                    self.system_health['memory_system'] and
                    self.system_health['orchestration_system'] and
                    self.system_health['session_management'] and
                    self.autonomous_features_enabled
                )
                
                self.system_health['autonomous_capabilities'] = autonomous_health
                
                await asyncio.sleep(90)  # Check every 1.5 minutes
                
            except Exception as e:
                logger.error(f"Autonomous features health check failed: {e}")
                self.system_health['autonomous_capabilities'] = False
                await asyncio.sleep(45)

# Global integration instance
enhanced_integration = CompleteEnhancedIntegration()

# Flask app integration function
async def integrate_complete_enhanced_system_with_app(app, socketio, model_manager, scrapybara_client):
    """
    Complete integration of enhanced system with Flask app
    Replaces Redis with Mem0 and enables Scout.new-level autonomous capabilities
    """
    
    try:
        logger.info("🚀 Starting Complete Enhanced System Integration...")
        
        # Initialize the complete enhanced system
        initialization_result = await enhanced_integration.initialize_complete_system(
            model_manager=model_manager,
            scrapybara_client=scrapybara_client
        )
        
        if not initialization_result['success']:
            raise RuntimeError("Failed to initialize enhanced system")
        
        # Store components in Flask app
        app.enhanced_memory_manager = enhanced_integration.memory_manager
        app.enhanced_orchestrator = enhanced_integration.orchestrator
        app.enhanced_session_manager = enhanced_integration.session_manager
        app.complete_enhanced_integration = enhanced_integration
        
        # Import and register enhanced API
        from api.enhanced_orchestration_api import integrate_enhanced_orchestration_with_app
        integrate_enhanced_orchestration_with_app(
            app=app,
            socketio=socketio,
            enhanced_memory_manager=enhanced_integration.memory_manager,
            enhanced_orchestrator=enhanced_integration.orchestrator,
            enhanced_session_manager=enhanced_integration.session_manager
        )
        
        # Add enhanced middleware for comprehensive tracking
        @app.before_request
        def enhanced_before_request():
            """Enhanced request tracking with Mem0 integration"""
            if hasattr(app, 'complete_enhanced_integration') and request.json:
                user_id = request.json.get('user_id')
                session_id = request.json.get('session_id')
                
                if user_id:
                    # Track with enhanced context
                    asyncio.create_task(
                        app.enhanced_memory_manager.track_user_activity(
                            user_id=user_id,
                            session_id=session_id,
                            activity_type='api_request',
                            context={
                                'endpoint': request.endpoint,
                                'method': request.method,
                                'timestamp': datetime.now(),
                                'enhanced_tracking': True
                            }
                        )
                    )
        
        logger.info("✅ Complete Enhanced System Integration successful!")
        logger.info("🎯 Scout.new-level autonomous capabilities now active!")
        logger.info("🧠 Mem0-based persistent sessions enabled!")
        logger.info("🤖 Multi-agent autonomous orchestration online!")
        
        return {
            'success': True,
            'message': 'Complete Enhanced Mama Bear System with Scout.new-level capabilities is now active!',
            'features': [
                'Mem0-based persistent memory',
                'Autonomous multi-agent orchestration',
                'Intelligent session checkpointing',
                'Adaptive learning capabilities',
                'Proactive assistance',
                'Real-time agent coordination',
                'Advanced workflow intelligence'
            ],
            'system_health': enhanced_integration.system_health
        }
        
    except Exception as e:
        logger.error(f"❌ Complete Enhanced System Integration failed: {e}")
        raise

# Utility function for testing the complete system
async def test_complete_enhanced_system():
    """Test the complete enhanced system integration"""
    
    logger.info("🧪 Testing Complete Enhanced System...")
    
    try:
        # Test autonomous request processing
        test_result = await enhanced_integration.process_autonomous_request(
            message="Test autonomous processing capabilities",
            user_id="test_user",
            page_context="test_context"
        )
        
        logger.info(f"✅ Test result: {test_result['success']}")
        
        # Test system status
        status = await enhanced_integration.get_comprehensive_system_status()
        logger.info(f"📊 System Status: {status['component_health']}")
        
        return {
            'test_passed': test_result['success'],
            'system_status': status,
            'autonomous_features_working': test_result.get('autonomous_features', {})
        }
        
    except Exception as e:
        logger.error(f"❌ System test failed: {e}")
        return {
            'test_passed': False,
            'error': str(e)
        }
