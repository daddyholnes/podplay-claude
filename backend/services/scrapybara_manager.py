"""
Scrapybara Manager Service
Manages cloud VM instances and development environments using Scrapybara
"""

import asyncio
import json
import logging
import aiohttp
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ScrapybaraInstance:
    """Represents a single Scrapybara cloud VM instance"""
    
    def __init__(self, instance_id: str, config: Dict[str, Any]):
        self.instance_id = instance_id
        self.config = config
        self.status = 'creating'
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.environment_type = config.get('environment', 'general')
        self.tech_stack = config.get('tech_stack', [])
        self.user_id = config.get('user_id')
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to dictionary"""
        return {
            'instance_id': self.instance_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'environment_type': self.environment_type,
            'tech_stack': self.tech_stack,
            'user_id': self.user_id,
            'uptime_minutes': int((datetime.now() - self.created_at).total_seconds() / 60)
        }

class ScrapybaraManager:
    """Manages Scrapybara cloud VM instances for instant development environments"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get('scrapybara_api_key')
        self.base_url = config.get('scrapybara_base_url', 'https://api.scrapybara.com/v1')
        self.instances = {}  # Track active instances
        self.environment_templates = self._initialize_templates()
        
        # Session for HTTP requests
        self.session = None
        
        logger.info("Scrapybara Manager initialized")
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.api_key}'},
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize environment templates for different development scenarios"""
        return {
            'python_dev': {
                'name': 'Python Development',
                'description': 'Full Python development environment with common packages',
                'image': 'python:3.11-slim',
                'packages': ['pip', 'poetry', 'black', 'flake8', 'pytest'],
                'ports': [8000, 5000, 3000],
                'environment_vars': {
                    'PYTHONPATH': '/workspace',
                    'PIP_DISABLE_PIP_VERSION_CHECK': '1'
                }
            },
            'node_dev': {
                'name': 'Node.js Development', 
                'description': 'Node.js environment with npm, yarn, and common tools',
                'image': 'node:18-alpine',
                'packages': ['npm', 'yarn', 'nodemon', 'pm2'],
                'ports': [3000, 8080, 5000],
                'environment_vars': {
                    'NODE_ENV': 'development',
                    'NPM_CONFIG_LOGLEVEL': 'warn'
                }
            },
            'fullstack_js': {
                'name': 'Full-Stack JavaScript',
                'description': 'Complete JavaScript stack with React, Node.js, and databases',
                'image': 'node:18',
                'packages': ['npm', 'yarn', 'create-react-app', 'express-generator'],
                'ports': [3000, 8080, 5000, 5432],
                'services': ['postgresql', 'redis'],
                'environment_vars': {
                    'NODE_ENV': 'development'
                }
            },
            'ai_ml': {
                'name': 'AI/ML Development',
                'description': 'Machine learning environment with Python, Jupyter, and ML libraries',
                'image': 'jupyter/tensorflow-notebook',
                'packages': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'],
                'ports': [8888, 6006, 8080],
                'environment_vars': {
                    'JUPYTER_ENABLE_LAB': 'yes'
                }
            },
            'web_dev': {
                'name': 'Web Development',
                'description': 'Modern web development with multiple framework support',
                'image': 'node:18',
                'packages': ['npm', 'yarn', 'vite', 'webpack', 'tailwindcss'],
                'ports': [3000, 5173, 8080],
                'environment_vars': {
                    'NODE_ENV': 'development'
                }
            },
            'sanctuary_dev': {
                'name': 'Podplay Sanctuary',
                'description': 'Specialized environment for Podplay Sanctuary development',
                'image': 'node:18',
                'packages': ['npm', 'yarn', 'python3', 'pip'],
                'ports': [3000, 5000, 8080],
                'services': ['postgresql', 'redis'],
                'environment_vars': {
                    'NODE_ENV': 'development',
                    'SANCTUARY_MODE': 'development'
                },
                'custom_setup': [
                    'pip install flask socketio anthropic openai google-generativeai mem0',
                    'npm install -g create-react-app'
                ]
            }
        }
    
    async def create_instance(self, user_id: str, environment_type: str = 'python_dev',
                            custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Scrapybara instance"""
        try:
            if not self.session:
                raise ValueError("ScrapybaraManager must be used as async context manager")
            
            # Get template
            if environment_type not in self.environment_templates:
                environment_type = 'python_dev'  # Default fallback
            
            template = self.environment_templates[environment_type].copy()
            
            # Apply custom configuration
            if custom_config:
                template.update(custom_config)
            
            # Generate instance ID
            instance_id = f"sanctuary-{user_id[:8]}-{str(uuid.uuid4())[:8]}"
            
            # Prepare creation payload
            payload = {
                'instance_id': instance_id,
                'image': template['image'],
                'environment_type': environment_type,
                'ports': template.get('ports', []),
                'environment_vars': template.get('environment_vars', {}),
                'packages': template.get('packages', []),
                'services': template.get('services', []),
                'user_metadata': {
                    'user_id': user_id,
                    'created_via': 'podplay_sanctuary',
                    'template': environment_type
                }
            }
            
            # Add custom setup commands
            if 'custom_setup' in template:
                payload['setup_commands'] = template['custom_setup']
            
            # Make API request to create instance
            async with self.session.post(f'{self.base_url}/instances', json=payload) as response:
                if response.status == 201:
                    response_data = await response.json()
                    
                    # Create local instance tracking
                    instance = ScrapybaraInstance(instance_id, {
                        'user_id': user_id,
                        'environment': environment_type,
                        'tech_stack': template.get('packages', []),
                        'template': template
                    })
                    
                    self.instances[instance_id] = instance
                    
                    result = {
                        'instance_id': instance_id,
                        'status': 'creating',
                        'environment_type': environment_type,
                        'template_name': template['name'],
                        'access_url': response_data.get('access_url'),
                        'ssh_connection': response_data.get('ssh_connection'),
                        'ports': template.get('ports', []),
                        'estimated_ready_time': '2-5 minutes',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    logger.info(f"Created Scrapybara instance {instance_id} for user {user_id}")
                    return result
                    
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create instance: {response.status} - {error_text}")
                    raise Exception(f"Failed to create instance: {error_text}")
                    
        except Exception as e:
            logger.error(f"Error creating Scrapybara instance: {str(e)}")
            # Return fallback response for development
            return await self._create_fallback_instance(user_id, environment_type)
    
    async def _create_fallback_instance(self, user_id: str, environment_type: str) -> Dict[str, Any]:
        """Create a fallback instance response when Scrapybara API is unavailable"""
        instance_id = f"fallback-{user_id[:8]}-{str(uuid.uuid4())[:8]}"
        template = self.environment_templates.get(environment_type, self.environment_templates['python_dev'])
        
        # Create mock instance for development
        instance = ScrapybaraInstance(instance_id, {
            'user_id': user_id,
            'environment': environment_type,
            'tech_stack': template.get('packages', []),
            'template': template
        })
        instance.status = 'ready'  # Mock as ready
        
        self.instances[instance_id] = instance
        
        return {
            'instance_id': instance_id,
            'status': 'ready',
            'environment_type': environment_type,
            'template_name': template['name'],
            'access_url': f'https://mock-vm-{instance_id}.scrapybara.dev',
            'ssh_connection': f'ssh developer@{instance_id}.scrapybara.dev',
            'ports': template.get('ports', []),
            'note': 'Mock instance for development - Scrapybara integration will be activated in production',
            'created_at': datetime.now().isoformat()
        }
    
    async def get_instance_status(self, instance_id: str) -> Dict[str, Any]:
        """Get status of a specific instance"""
        try:
            if instance_id not in self.instances:
                return {'error': 'Instance not found'}
            
            instance = self.instances[instance_id]
            
            if self.session:
                # Try to get real status from API
                async with self.session.get(f'{self.base_url}/instances/{instance_id}') as response:
                    if response.status == 200:
                        api_data = await response.json()
                        instance.status = api_data.get('status', instance.status)
                        
                        return {
                            **instance.to_dict(),
                            'api_status': api_data.get('status'),
                            'resource_usage': api_data.get('resource_usage', {}),
                            'access_url': api_data.get('access_url'),
                            'ssh_connection': api_data.get('ssh_connection')
                        }
            
            # Return local instance data
            return instance.to_dict()
            
        except Exception as e:
            logger.error(f"Error getting instance status: {str(e)}")
            return {'error': 'Failed to get instance status'}
    
    async def list_user_instances(self, user_id: str) -> List[Dict[str, Any]]:
        """List all instances for a user"""
        try:
            user_instances = [
                instance.to_dict() 
                for instance in self.instances.values() 
                if instance.user_id == user_id
            ]
            
            # Sort by creation time (most recent first)
            user_instances.sort(key=lambda x: x['created_at'], reverse=True)
            
            return user_instances
            
        except Exception as e:
            logger.error(f"Error listing user instances: {str(e)}")
            return []
    
    async def stop_instance(self, instance_id: str, user_id: str) -> Dict[str, Any]:
        """Stop a running instance"""
        try:
            if instance_id not in self.instances:
                return {'error': 'Instance not found'}
            
            instance = self.instances[instance_id]
            
            # Verify ownership
            if instance.user_id != user_id:
                return {'error': 'Permission denied'}
            
            if self.session:
                # Try to stop via API
                async with self.session.post(f'{self.base_url}/instances/{instance_id}/stop') as response:
                    if response.status == 200:
                        instance.status = 'stopped'
                        logger.info(f"Stopped instance {instance_id}")
                        return {'status': 'stopped', 'instance_id': instance_id}
            
            # Mock stop for development
            instance.status = 'stopped'
            return {'status': 'stopped', 'instance_id': instance_id, 'note': 'Mock stop - real API integration pending'}
            
        except Exception as e:
            logger.error(f"Error stopping instance: {str(e)}")
            return {'error': 'Failed to stop instance'}
    
    async def delete_instance(self, instance_id: str, user_id: str) -> Dict[str, Any]:
        """Delete an instance permanently"""
        try:
            if instance_id not in self.instances:
                return {'error': 'Instance not found'}
            
            instance = self.instances[instance_id]
            
            # Verify ownership
            if instance.user_id != user_id:
                return {'error': 'Permission denied'}
            
            if self.session:
                # Try to delete via API
                async with self.session.delete(f'{self.base_url}/instances/{instance_id}') as response:
                    if response.status == 204:
                        del self.instances[instance_id]
                        logger.info(f"Deleted instance {instance_id}")
                        return {'status': 'deleted', 'instance_id': instance_id}
            
            # Mock delete for development
            del self.instances[instance_id]
            return {'status': 'deleted', 'instance_id': instance_id, 'note': 'Mock delete - real API integration pending'}
            
        except Exception as e:
            logger.error(f"Error deleting instance: {str(e)}")
            return {'error': 'Failed to delete instance'}
    
    async def connect_to_instance(self, instance_id: str, user_id: str, 
                                connection_type: str = 'web') -> Dict[str, Any]:
        """Get connection details for an instance"""
        try:
            if instance_id not in self.instances:
                return {'error': 'Instance not found'}
            
            instance = self.instances[instance_id]
            
            # Verify ownership
            if instance.user_id != user_id:
                return {'error': 'Permission denied'}
            
            # Update last activity
            instance.last_activity = datetime.now()
            
            # Generate connection details
            connection_details = {
                'instance_id': instance_id,
                'connection_type': connection_type,
                'status': instance.status
            }
            
            if connection_type == 'web':
                connection_details.update({
                    'access_url': f'https://vm-{instance_id}.scrapybara.dev',
                    'embedded_url': f'https://vm-{instance_id}.scrapybara.dev/embed',
                    'ports': instance.config.get('template', {}).get('ports', [])
                })
            elif connection_type == 'ssh':
                connection_details.update({
                    'ssh_host': f'{instance_id}.scrapybara.dev',
                    'ssh_user': 'developer',
                    'ssh_port': 22,
                    'ssh_command': f'ssh developer@{instance_id}.scrapybara.dev'
                })
            elif connection_type == 'vscode':
                connection_details.update({
                    'vscode_url': f'vscode://vscode-remote/ssh-remote+developer@{instance_id}.scrapybara.dev/workspace',
                    'remote_ssh_config': f'Host {instance_id}\n  HostName {instance_id}.scrapybara.dev\n  User developer'
                })
            
            return connection_details
            
        except Exception as e:
            logger.error(f"Error getting connection details: {str(e)}")
            return {'error': 'Failed to get connection details'}
    
    def get_environment_templates(self) -> Dict[str, Any]:
        """Get available environment templates"""
        return {
            template_id: {
                'id': template_id,
                'name': template['name'],
                'description': template['description'],
                'image': template['image'],
                'packages': template.get('packages', []),
                'ports': template.get('ports', []),
                'services': template.get('services', [])
            }
            for template_id, template in self.environment_templates.items()
        }
    
    async def get_instance_logs(self, instance_id: str, user_id: str, lines: int = 100) -> Dict[str, Any]:
        """Get logs from an instance"""
        try:
            if instance_id not in self.instances:
                return {'error': 'Instance not found'}
            
            instance = self.instances[instance_id]
            
            # Verify ownership
            if instance.user_id != user_id:
                return {'error': 'Permission denied'}
            
            if self.session:
                # Try to get logs via API
                async with self.session.get(f'{self.base_url}/instances/{instance_id}/logs?lines={lines}') as response:
                    if response.status == 200:
                        logs_data = await response.json()
                        return {
                            'instance_id': instance_id,
                            'logs': logs_data.get('logs', []),
                            'timestamp': datetime.now().isoformat()
                        }
            
            # Mock logs for development
            mock_logs = [
                f"[{datetime.now().isoformat()}] Instance {instance_id} initialized",
                f"[{datetime.now().isoformat()}] Environment: {instance.environment_type}",
                f"[{datetime.now().isoformat()}] Status: {instance.status}",
                f"[{datetime.now().isoformat()}] Ready for development"
            ]
            
            return {
                'instance_id': instance_id,
                'logs': mock_logs,
                'timestamp': datetime.now().isoformat(),
                'note': 'Mock logs - real API integration pending'
            }
            
        except Exception as e:
            logger.error(f"Error getting instance logs: {str(e)}")
            return {'error': 'Failed to get instance logs'}
    
    async def cleanup_old_instances(self, hours: int = 24):
        """Clean up old unused instances"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            instances_to_cleanup = [
                instance_id for instance_id, instance in self.instances.items()
                if instance.last_activity < cutoff_time and instance.status != 'stopped'
            ]
            
            for instance_id in instances_to_cleanup:
                instance = self.instances[instance_id]
                await self.stop_instance(instance_id, instance.user_id)
                logger.info(f"Auto-stopped inactive instance {instance_id}")
            
            return len(instances_to_cleanup)
            
        except Exception as e:
            logger.error(f"Error cleaning up instances: {str(e)}")
            return 0
