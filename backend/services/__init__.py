"""
Service Initialization Module
Initializes and manages all sanctuary services
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from config.settings import get_settings
from .mama_bear_agent import EnhancedMamaBearAgent
from .memory_manager import MemoryManager
from .scrapybara_manager import ScrapybaraManager
from .theme_manager import ThemeManager

logger = logging.getLogger(__name__)

class ServiceManager:
    """Manages all sanctuary services with proper initialization and lifecycle"""
    
    def __init__(self):
        self.settings = get_settings()
        self.services = {}
        self.initialized = False
        
    async def initialize_services(self) -> Dict[str, Any]:
        """Initialize all services with proper configuration"""
        try:
            logger.info("Initializing Podplay Sanctuary services...")
            
            # Initialize Memory Manager
            memory_config = {
                'mem0_api_key': self.settings.mem0_api_key,
                'storage_path': self.settings.storage_path
            }
            self.services['memory'] = MemoryManager(memory_config)
            logger.info("✅ Memory Manager initialized")
            
            # Initialize Theme Manager  
            theme_config = {
                'default_theme': 'sky',
                'storage_path': self.settings.storage_path
            }
            self.services['themes'] = ThemeManager(theme_config)
            logger.info("✅ Theme Manager initialized")
            
            # Initialize Scrapybara Manager
            scrapybara_config = {
                'scrapybara_api_key': self.settings.scrapybara_api_key,
                'scrapybara_base_url': getattr(self.settings, 'scrapybara_base_url', 'https://api.scrapybara.com/v1')
            }
            self.services['scrapybara'] = ScrapybaraManager(scrapybara_config)
            logger.info("✅ Scrapybara Manager initialized")
            
            # Initialize Enhanced Mama Bear Agent
            mama_bear_config = {
                'anthropic_api_key': self.settings.anthropic_api_key,
                'openai_api_key': self.settings.openai_api_key,
                'google_api_key': self.settings.google_api_key,
                'mem0_api_key': self.settings.mem0_api_key,
                'default_model': 'claude-3-5-sonnet-20241022',
                'memory_manager': self.services['memory']
            }
            self.services['mama_bear'] = EnhancedMamaBearAgent(mama_bear_config)
            logger.info("✅ Enhanced Mama Bear Agent initialized")
            
            self.initialized = True
            
            return {
                'status': 'success',
                'services_initialized': list(self.services.keys()),
                'mama_bear_variants': 7,
                'sanctuary_themes': 3,
                'memory_enabled': True,
                'scrapybara_enabled': True,
                'initialization_complete': True
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize services: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'services_initialized': list(self.services.keys())
            }
    
    def get_service(self, service_name: str) -> Optional[Any]:
        """Get a specific service instance"""
        if not self.initialized:
            raise RuntimeError("Services not initialized. Call initialize_services() first.")
        
        return self.services.get(service_name)
    
    def get_all_services(self) -> Dict[str, Any]:
        """Get all initialized services"""
        if not self.initialized:
            raise RuntimeError("Services not initialized. Call initialize_services() first.")
        
        return self.services.copy()
    
    async def shutdown_services(self):
        """Gracefully shutdown all services"""
        logger.info("Shutting down sanctuary services...")
        
        # Close any async resources
        if 'scrapybara' in self.services:
            scrapybara = self.services['scrapybara']
            if hasattr(scrapybara, 'session') and scrapybara.session:
                await scrapybara.session.close()
        
        # Clear services
        self.services.clear()
        self.initialized = False
        
        logger.info("✅ All services shut down")
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get current status of all services"""
        return {
            'initialized': self.initialized,
            'services': {
                name: {
                    'status': 'active' if service else 'inactive',
                    'type': type(service).__name__ if service else None
                }
                for name, service in self.services.items()
            },
            'total_services': len(self.services)
        }

# Global service manager instance
service_manager = ServiceManager()

async def get_mama_bear_agent() -> Optional[EnhancedMamaBearAgent]:
    """Get the Mama Bear Agent service"""
    return service_manager.get_service('mama_bear')

async def get_memory_manager() -> Optional[MemoryManager]:
    """Get the Memory Manager service"""
    return service_manager.get_service('memory')

async def get_scrapybara_manager() -> Optional[ScrapybaraManager]:
    """Get the Scrapybara Manager service"""
    return service_manager.get_service('scrapybara')

async def get_theme_manager() -> Optional[ThemeManager]:
    """Get the Theme Manager service"""
    return service_manager.get_service('themes')

async def initialize_all_services() -> Dict[str, Any]:
    """Initialize all sanctuary services"""
    return await service_manager.initialize_services()

async def shutdown_all_services():
    """Shutdown all sanctuary services"""
    await service_manager.shutdown_services()

def get_service_status() -> Dict[str, Any]:
    """Get status of all services"""
    return service_manager.get_service_status()
