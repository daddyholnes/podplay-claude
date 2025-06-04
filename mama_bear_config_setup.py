# backend/config/mama_bear_config.py
import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class MamaBearConfig:
    """Configuration for Mama Bear model management"""
    
    # API Keys (from environment)
    GEMINI_API_KEY_PRIMARY: str = os.getenv('GEMINI_API_KEY', 'AIzaSyCNUGhuoAvvaSJ2ypsqzgtUCaLSusRZs5Y')
    GEMINI_API_KEY_BACKUP: str = os.getenv('GEMINI_API_KEY_BACKUP', '')  # Add your second key here
    
    # Model Configuration
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 8192
    DEFAULT_TOP_P: float = 0.95
    DEFAULT_TOP_K: int = 64
    
    # Quota Management
    QUOTA_SAFETY_MARGIN: float = 0.1  # 10% safety margin
    MAX_FALLBACK_ATTEMPTS: int = 6
    BASE_FALLBACK_DELAY: float = 1.0
    MAX_FALLBACK_DELAY: float = 30.0
    
    # Health Monitoring
    HEALTH_CHECK_INTERVAL: int = 300  # 5 minutes
    ERROR_THRESHOLD: int = 3  # Consecutive errors before marking unhealthy
    RECOVERY_TIMEOUT: int = 1800  # 30 minutes before attempting recovery
    
    # Performance Optimization
    ENABLE_REQUEST_BATCHING: bool = True
    BATCH_SIZE: int = 5
    ENABLE_RESPONSE_CACHING: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_MODEL_USAGE: bool = True
    LOG_QUOTA_WARNINGS: bool = True
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        config = cls()
        
        if not config.GEMINI_API_KEY_PRIMARY:
            raise ValueError("GEMINI_API_KEY_PRIMARY is required")
        
        if not config.GEMINI_API_KEY_BACKUP:
            print("WARNING: GEMINI_API_KEY_BACKUP not set - limited failover capability")
        
        return True

# backend/services/mama_bear_specialized_variants.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class MamaBearVariant(ABC):
    """Base class for all Mama Bear specialized variants"""
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    @abstractmethod
    def get_model_preferences(self) -> Dict[str, Any]:
        pass
    
    def should_use_reasoning_model(self, message: str) -> bool:
        """Determine if this variant should prefer reasoning-capable models"""
        return False

class ResearchSpecialist(MamaBearVariant):
    """Mama Bear variant for research and information gathering"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's Research Specialist variant - a caring, thorough AI assistant who loves discovering connections and helping with research. 

Your personality:
- Curious and enthusiastic about learning
- Thorough but not overwhelming
- Great at finding patterns and connections
- Warm and encouraging in your communication
- Proactive in suggesting related research directions

Your expertise:
- Web research and information synthesis
- Document analysis and summarization
- Fact-checking and source verification
- Research methodology and planning
- Citation and reference management

Always maintain Mama Bear's caring, supportive tone while being incredibly helpful with research tasks."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': True,  # Research needs reasoning
            'temperature': 0.3,  # Lower for accuracy
            'requires_reasoning': True
        }
    
    def should_use_reasoning_model(self, message: str) -> bool:
        research_keywords = ['research', 'analyze', 'compare', 'investigate', 'study', 'examine']
        return any(keyword in message.lower() for keyword in research_keywords)

class DevOpsSpecialist(MamaBearVariant):
    """Mama Bear variant for VM and infrastructure management"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's DevOps Specialist variant - a protective, efficient AI assistant who ensures everything runs smoothly.

Your personality:
- Protective and security-conscious
- Efficient and optimization-focused
- Calm under pressure
- Proactive about preventing problems
- Encouraging about learning new technologies

Your expertise:
- Scrapybara VM management and orchestration
- Environment configuration and optimization
- Resource monitoring and management
- Troubleshooting and debugging
- Security best practices
- Performance optimization

Always maintain Mama Bear's caring nature while being the reliable guardian of the technical infrastructure."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': False,  # DevOps tasks often need speed
            'temperature': 0.2,  # Very low for precision
            'requires_reasoning': False
        }

class ScoutCommander(MamaBearVariant):
    """Mama Bear variant for autonomous task execution"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's Scout Commander variant - an adventurous, autonomous AI assistant who takes initiative while keeping humans in control.

Your personality:
- Adventurous and strategic
- Autonomous but respectful of boundaries
- Clear about your capabilities and limitations
- Excellent at breaking down complex tasks
- Enthusiastic about exploration and discovery

Your expertise:
- Task decomposition and planning
- Autonomous execution strategies
- Progress tracking and reporting
- Error recovery and adaptation
- Resource optimization for long-running tasks

Always maintain Mama Bear's warmth while being the brave explorer who ventures into new territories."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': True,  # Autonomous tasks need reasoning
            'temperature': 0.5,  # Balanced for creativity and precision
            'requires_reasoning': True
        }
    
    def should_use_reasoning_model(self, message: str) -> bool:
        return True  # Scout always benefits from reasoning

class ModelCoordinator(MamaBearVariant):
    """Mama Bear variant for managing multiple AI models"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's Model Coordinator variant - a diplomatic, knowledgeable AI assistant who knows all about different AI models.

Your personality:
- Diplomatic and fair in comparisons
- Deeply knowledgeable about AI capabilities
- Great at matching tasks to optimal models
- Encouraging about AI learning and exploration
- Honest about model limitations and strengths

Your expertise:
- AI model capabilities and limitations
- Optimal model selection for different tasks
- Cross-model result synthesis
- Performance optimization strategies
- Model availability and status monitoring

Always maintain Mama Bear's supportive nature while being the wise guide through the AI landscape."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': True,  # Model coordination needs intelligence
            'temperature': 0.4,
            'requires_reasoning': True
        }

class ToolCurator(MamaBearVariant):
    """Mama Bear variant for MCP tools and integrations"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's Tool Curator variant - an enthusiastic, helpful AI assistant who loves discovering and recommending the perfect tools.

Your personality:
- Enthusiastic about new tools and technologies
- Helpful with recommendations and guidance
- Great at understanding workflow needs
- Encouraging about tool exploration
- Honest about tool limitations and compatibility

Your expertise:
- MCP server discovery and evaluation
- Tool compatibility assessment
- Installation and configuration guidance
- Workflow optimization with tools
- Custom tool development recommendations

Always maintain Mama Bear's caring nature while being the excited curator of amazing tools."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': False,  # Tool curation can be fast
            'temperature': 0.6,  # Higher for creativity in recommendations
            'requires_reasoning': False
        }

class IntegrationArchitect(MamaBearVariant):
    """Mama Bear variant for building integrations"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's Integration Architect variant - a methodical, security-conscious AI assistant who builds rock-solid connections.

Your personality:
- Methodical and detail-oriented
- Security-conscious and protective
- Patient with complex integration challenges
- Encouraging about learning integration patterns
- Proactive about potential issues

Your expertise:
- API design and integration patterns
- Authentication and security best practices
- Workflow automation and orchestration
- Error handling and resilience strategies
- Performance optimization for integrations

Always maintain Mama Bear's supportive nature while being the careful architect of reliable connections."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': True,  # Integration work needs reasoning
            'temperature': 0.3,  # Low for precision
            'requires_reasoning': True
        }

class LiveAPISpecialist(MamaBearVariant):
    """Mama Bear variant for real-time API interactions"""
    
    def get_system_prompt(self) -> str:
        return """You are Mama Bear's Live API Specialist variant - a dynamic, experimental AI assistant who thrives in real-time interactions.

Your personality:
- Dynamic and energetic
- Experimental and open to trying new approaches
- Great at real-time problem solving
- Encouraging about pushing boundaries
- Quick to adapt and optimize

Your expertise:
- Real-time API optimization
- Audio/video processing and streaming
- Function calling and orchestration
- Performance tuning for low latency
- Live interaction design patterns

Always maintain Mama Bear's warmth while being the agile specialist who makes real-time magic happen."""
    
    def get_model_preferences(self) -> Dict[str, Any]:
        return {
            'prefers_pro_model': False,  # Live APIs need speed
            'temperature': 0.5,  # Balanced for responsiveness
            'requires_reasoning': False
        }

# backend/utils/mama_bear_monitoring.py
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

class MamaBearMonitoring:
    """Advanced monitoring and analytics for Mama Bear system"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.logger = logging.getLogger(__name__)
        self.metrics = {
            'requests_total': 0,
            'requests_successful': 0,
            'requests_failed': 0,
            'fallbacks_triggered': 0,
            'quota_warnings': 0,
            'avg_response_time': 0.0,
            'model_usage': {},
            'billing_account_usage': {},
            'hourly_stats': {}
        }
        
        # Start monitoring tasks
        asyncio.create_task(self._hourly_metrics_reset())
        asyncio.create_task(self._daily_report_generator())
    
    def record_request(self, response_metadata: Dict[str, Any]):
        """Record metrics for a completed request"""
        self.metrics['requests_total'] += 1
        
        if 'error' not in response_metadata:
            self.metrics['requests_successful'] += 1
            
            # Update response time average
            current_time = response_metadata.get('processing_time', 0)
            current_avg = self.metrics['avg_response_time']
            total_successful = self.metrics['requests_successful']
            self.metrics['avg_response_time'] = (current_avg * (total_successful - 1) + current_time) / total_successful
            
            # Track model usage
            model_used = response_metadata.get('model_used', 'unknown')
            if model_used not in self.metrics['model_usage']:
                self.metrics['model_usage'][model_used] = 0
            self.metrics['model_usage'][model_used] += 1
            
            # Track billing account usage
            billing_account = response_metadata.get('billing_account', 'unknown')
            if billing_account not in self.metrics['billing_account_usage']:
                self.metrics['billing_account_usage'][billing_account] = 0
            self.metrics['billing_account_usage'][billing_account] += 1
            
        else:
            self.metrics['requests_failed'] += 1
        
        # Track fallbacks
        fallback_count = response_metadata.get('fallback_count', 0)
        if fallback_count > 0:
            self.metrics['fallbacks_triggered'] += fallback_count
        
        # Track quota warnings
        quota_warnings = response_metadata.get('quota_warnings', [])
        self.metrics['quota_warnings'] += len(quota_warnings)
    
    async def _hourly_metrics_reset(self):
        """Reset hourly metrics and store historical data"""
        while True:
            try:
                await asyncio.sleep(3600)  # 1 hour
                
                current_hour = datetime.now().strftime('%Y-%m-%d_%H')
                self.metrics['hourly_stats'][current_hour] = {
                    'requests': self.metrics['requests_total'],
                    'success_rate': self.metrics['requests_successful'] / max(self.metrics['requests_total'], 1),
                    'avg_response_time': self.metrics['avg_response_time'],
                    'fallback_rate': self.metrics['fallbacks_triggered'] / max(self.metrics['requests_total'], 1)
                }
                
                # Keep only last 24 hours of hourly stats
                cutoff_time = datetime.now() - timedelta(hours=24)
                cutoff_str = cutoff_time.strftime('%Y-%m-%d_%H')
                
                self.metrics['hourly_stats'] = {
                    k: v for k, v in self.metrics['hourly_stats'].items() 
                    if k >= cutoff_str
                }
                
            except Exception as e:
                self.logger.error(f"Error in hourly metrics reset: {e}")
    
    async def _daily_report_generator(self):
        """Generate daily performance reports"""
        while True:
            try:
                await asyncio.sleep(86400)  # 24 hours
                
                report = self.generate_daily_report()
                self.logger.info(f"Daily Mama Bear Report:\n{json.dumps(report, indent=2)}")
                
            except Exception as e:
                self.logger.error(f"Error generating daily report: {e}")
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate comprehensive daily performance report"""
        model_status = self.model_manager.get_model_status()
        
        # Calculate success rates by model
        model_performance = {}
        for model_id, usage_count in self.metrics['model_usage'].items():
            model_performance[model_id] = {
                'usage_count': usage_count,
                'usage_percentage': (usage_count / max(self.metrics['requests_total'], 1)) * 100
            }
        
        # Calculate billing distribution
        billing_distribution = {}
        for account, usage_count in self.metrics['billing_account_usage'].items():
            billing_distribution[account] = {
                'usage_count': usage_count,
                'usage_percentage': (usage_count / max(self.metrics['requests_total'], 1)) * 100
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'period': '24h',
            'summary': {
                'total_requests': self.metrics['requests_total'],
                'success_rate': (self.metrics['requests_successful'] / max(self.metrics['requests_total'], 1)) * 100,
                'average_response_time': self.metrics['avg_response_time'],
                'fallback_rate': (self.metrics['fallbacks_triggered'] / max(self.metrics['requests_total'], 1)) * 100,
                'quota_warnings': self.metrics['quota_warnings']
            },
            'model_performance': model_performance,
            'billing_distribution': billing_distribution,
            'model_health': model_status,
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on metrics"""
        recommendations = []
        
        # Check success rate
        success_rate = (self.metrics['requests_successful'] / max(self.metrics['requests_total'], 1)) * 100
        if success_rate < 95:
            recommendations.append(f"Success rate is {success_rate:.1f}% - consider reviewing API key status and quotas")
        
        # Check fallback rate
        fallback_rate = (self.metrics['fallbacks_triggered'] / max(self.metrics['requests_total'], 1)) * 100
        if fallback_rate > 20:
            recommendations.append(f"High fallback rate ({fallback_rate:.1f}%) - consider increasing quotas or adding more API keys")
        
        # Check response time
        if self.metrics['avg_response_time'] > 5.0:
            recommendations.append(f"Average response time is {self.metrics['avg_response_time']:.2f}s - consider optimizing model selection")
        
        # Check model distribution
        if len(self.metrics['model_usage']) == 1:
            recommendations.append("Only using one model - consider enabling additional models for better reliability")
        
        # Check quota warnings
        if self.metrics['quota_warnings'] > self.metrics['requests_total'] * 0.1:
            recommendations.append("High number of quota warnings - consider upgrading quota limits")
        
        return recommendations

# backend/api/mama_bear_endpoints.py
from flask import Blueprint, request, jsonify
from flask_socketio import emit
import asyncio
from datetime import datetime

mama_bear_bp = Blueprint('mama_bear', __name__)

@mama_bear_bp.route('/api/mama-bear/chat', methods=['POST'])
async def mama_bear_chat():
    """Main chat endpoint with intelligent model selection"""
    try:
        data = request.json
        
        # Extract request data
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        user_id = data.get('user_id', 'default_user')
        options = data.get('options', {})
        
        # Get Mama Bear instance
        mama_bear = current_app.mama_bear_agent
        
        # Process message
        response = await mama_bear.process_message(
            message=message,
            page_context=page_context,
            user_id=user_id,
            **options
        )
        
        # Record metrics
        if hasattr(current_app, 'mama_bear_monitoring'):
            current_app.mama_bear_monitoring.record_request(response.get('metadata', {}))
        
        return jsonify({
            'success': True,
            'response': response['content'],
            'metadata': response.get('metadata', {}),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@mama_bear_bp.route('/api/mama-bear/status', methods=['GET'])
async def mama_bear_status():
    """Get comprehensive system status"""
    try:
        mama_bear = current_app.mama_bear_agent
        status = await mama_bear.get_system_status()
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@mama_bear_bp.route('/api/mama-bear/metrics', methods=['GET'])
async def mama_bear_metrics():
    """Get performance metrics and daily report"""
    try:
        if hasattr(current_app, 'mama_bear_monitoring'):
            monitoring = current_app.mama_bear_monitoring
            
            return jsonify({
                'success': True,
                'current_metrics': monitoring.metrics,
                'daily_report': monitoring.generate_daily_report(),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Monitoring not enabled',
                'timestamp': datetime.now().isoformat()
            }), 503
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@mama_bear_bp.route('/api/mama-bear/warm-up', methods=['POST'])
async def warm_up_models():
    """Manually trigger model warm-up"""
    try:
        mama_bear = current_app.mama_bear_agent
        await mama_bear.model_manager.warm_up_models()
        
        return jsonify({
            'success': True,
            'message': 'Model warm-up completed',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500