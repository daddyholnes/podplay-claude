"""
Configuration settings for Podplay Sanctuary
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'sanctuary_mama_bear_secret_2024')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Keys
    GEMINI_API_KEY_PRIMARY = os.getenv('GEMINI_API_KEY_PRIMARY')
    GEMINI_API_KEY_FALLBACK = os.getenv('GEMINI_API_KEY_FALLBACK')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MEM0_API_KEY = os.getenv('MEM0_API_KEY')
    SCRAPYBARA_API_KEY = os.getenv('SCRAPYBARA_API_KEY')
    
    # Storage and paths
    STORAGE_PATH = os.getenv('STORAGE_PATH', './storage')
    
    # API access properties
    @property
    def mem0_api_key(self):
        return self.MEM0_API_KEY
    
    @property
    def anthropic_api_key(self):
        return self.ANTHROPIC_API_KEY
    
    @property
    def openai_api_key(self):
        return self.OPENAI_API_KEY
    
    @property
    def google_api_key(self):
        return self.GEMINI_API_KEY_PRIMARY
    
    @property
    def scrapybara_api_key(self):
        return self.SCRAPYBARA_API_KEY
    
    @property
    def storage_path(self):
        return self.STORAGE_PATH
    
    @property
    def flask_secret_key(self):
        return self.SECRET_KEY
    
    # Mem0 Configuration
    MEM0_USER_ID = os.getenv('MEM0_USER_ID', 'nathan_sanctuary')
    MEM0_MEMORY_ENABLED = os.getenv('MEM0_MEMORY_ENABLED', 'True').lower() == 'true'
    MEM0_RAG_ENABLED = os.getenv('MEM0_RAG_ENABLED', 'True').lower() == 'true'
    MEM0_CONTEXT_WINDOW = int(os.getenv('MEM0_CONTEXT_WINDOW', 100))
    
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
    PRIMARY_SERVICE_ACCOUNT_PROJECT_ID = os.getenv('PRIMARY_SERVICE_ACCOUNT_PROJECT_ID')
    FALLBACK_SERVICE_ACCOUNT_PROJECT_ID = os.getenv('FALLBACK_SERVICE_ACCOUNT_PROJECT_ID')
    
    # Mama Bear Configuration
    MAMA_BEAR_DEFAULT_TEMPERATURE = float(os.getenv('MAMA_BEAR_DEFAULT_TEMPERATURE', 0.7))
    MAMA_BEAR_MAX_TOKENS = int(os.getenv('MAMA_BEAR_MAX_TOKENS', 8192))
    MAMA_BEAR_QUOTA_SAFETY_MARGIN = float(os.getenv('MAMA_BEAR_QUOTA_SAFETY_MARGIN', 0.1))
    MAMA_BEAR_MAX_FALLBACK_ATTEMPTS = int(os.getenv('MAMA_BEAR_MAX_FALLBACK_ATTEMPTS', 6))
    
    # Performance Settings
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 300))
    COMPRESSION_ENABLED = os.getenv('COMPRESSION_ENABLED', 'True').lower() == 'true'
    
    # Learning Settings
    LEARNING_ENABLED = os.getenv('LEARNING_ENABLED', 'True').lower() == 'true'
    LEARNING_RETENTION_DAYS = int(os.getenv('LEARNING_RETENTION_DAYS', 365))
    ADAPTIVE_RECOMMENDATIONS = os.getenv('ADAPTIVE_RECOMMENDATIONS', 'True').lower() == 'true'
    CONTEXT_MEMORY_SIZE = int(os.getenv('CONTEXT_MEMORY_SIZE', 1000))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'mama_bear.log')
    LOG_MAX_SIZE = os.getenv('LOG_MAX_SIZE', '10MB')
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Frontend Configuration
    FRONTEND_PORT = int(os.getenv('FRONTEND_PORT', 3000))
    BACKEND_PORT = int(os.getenv('BACKEND_PORT', 5001))
    VITE_API_BASE_URL = os.getenv('VITE_API_BASE_URL', 'http://localhost:5001')
    
    # MCP Configuration
    MCP_AGENT_ENABLED = os.getenv('MCP_AGENT_ENABLED', 'True').lower() == 'true'
    BROWSER_MCP_AGENT_ENABLED = os.getenv('BROWSER_MCP_AGENT_ENABLED', 'True').lower() == 'true'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    HOT_RELOAD = True
    DEBUG_TOOLBAR = True
    MOCK_DATA_ENABLED = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    HOT_RELOAD = False
    DEBUG_TOOLBAR = False
    MOCK_DATA_ENABLED = False

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)

def get_settings():
    """Get settings instance for easy access"""
    config = get_config()
    return config()
