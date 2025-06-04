# backend/config/mama_bear_config_setup.py
"""
🐻 Mama Bear Configuration Setup
Basic configuration loading for Mama Bear system
"""

import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load basic Mama Bear configuration"""
    return {
        'model_providers': {
            'anthropic': {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'models': ['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307']
            },
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'models': ['gpt-4', 'gpt-3.5-turbo']
            },
            'google': {
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'models': ['gemini-pro', 'gemini-pro-vision']
            }
        },
        'scrapybara': {
            'api_key': os.getenv('SCRAPYBARA_API_KEY'),
            'base_url': os.getenv('SCRAPYBARA_BASE_URL', 'https://api.scrapybara.com/v1')
        },
        'mem0': {
            'config': {
                'vector_store': {
                    'provider': 'qdrant',
                    'config': {
                        'host': 'localhost',
                        'port': 6333
                    }
                }
            }
        },
        'features': {
            'enhanced_orchestration': True,
            'scrapybara_integration': True,
            'memory_persistence': True
        }
    }
