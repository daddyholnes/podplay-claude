# backend/services/mama_bear_model_manager.py
import asyncio
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import google.generativeai as genai
from datetime import datetime, timedelta
import json

class ModelPriority(Enum):
    PRIMARY = 1
    SECONDARY = 2
    FALLBACK = 3

class QuotaStatus(Enum):
    AVAILABLE = "available"
    LIMITED = "limited"
    EXHAUSTED = "exhausted"
    ERROR = "error"

@dataclass
class ModelConfig:
    name: str
    api_key: str
    billing_account: str
    priority: ModelPriority
    requests_per_minute: int = 60
    requests_per_day: int = 1500
    context_window: int = 2000000
    max_output_tokens: int = 8192
    temperature: float = 0.7
    
    # Runtime tracking
    current_requests_minute: int = 0
    current_requests_day: int = 0
    last_request_time: float = 0
    last_minute_reset: float = 0
    last_day_reset: float = 0
    consecutive_errors: int = 0
    is_healthy: bool = True
    last_error: Optional[str] = None

@dataclass
class MamaBearResponse:
    content: str
    model_used: str
    api_key_used: str
    billing_account: str
    processing_time: float
    fallback_count: int = 0
    quota_warnings: List[str] = field(default_factory=list)

class MamaBearModelManager:
    """
    Intelligent model manager for Mama Bear that handles:
    - Quota limits across multiple models and API keys
    - Automatic failover and load balancing
    - Health monitoring and recovery
    - Performance optimization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = self._initialize_models()
        self.request_history = []
        self.global_fallback_delay = 1.0  # Start with 1 second
        self.max_fallback_delay = 30.0
        self.health_check_interval = 300  # 5 minutes
        
        # Start background health monitoring
        asyncio.create_task(self._background_health_monitor())
    
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Initialize all available Gemini 2.5 models with quota settings"""
        return {
            # Account 1 - Primary models
            "gemini-2.5-pro-primary": ModelConfig(
                name="gemini-2.5-pro-preview-05-06",
                api_key="AIzaSyCNUGhuoAvvaSJ2ypsqzgtUCaLSusRZs5Y",  # Your primary key
                billing_account="primary",
                priority=ModelPriority.PRIMARY,
                requests_per_minute=60,
                requests_per_day=1500,
                context_window=2000000,
                max_output_tokens=8192
            ),
            
            "gemini-2.5-flash-04-primary": ModelConfig(
                name="gemini-2.5-flash-preview-04-17",
                api_key="AIzaSyCNUGhuoAvvaSJ2ypsqzgtUCaLSusRZs5Y",
                billing_account="primary", 
                priority=ModelPriority.SECONDARY,
                requests_per_minute=120,  # Flash models typically have higher limits
                requests_per_day=3000,
                context_window=1000000,
                max_output_tokens=8192
            ),
            
            "gemini-2.5-flash-05-primary": ModelConfig(
                name="gemini-2.5-flash-preview-05-20",
                api_key="AIzaSyCNUGhuoAvvaSJ2ypsqzgtUCaLSusRZs5Y",
                billing_account="primary",
                priority=ModelPriority.SECONDARY,
                requests_per_minute=120,
                requests_per_day=3000,
                context_window=1000000,
                max_output_tokens=8192
            ),
            
            # Account 2 - Backup models (you'll need to add your second API key)
            "gemini-2.5-pro-backup": ModelConfig(
                name="gemini-2.5-pro-preview-05-06",
                api_key="YOUR_SECOND_API_KEY_HERE",  # Add your second billing account key
                billing_account="backup",
                priority=ModelPriority.FALLBACK,
                requests_per_minute=60,
                requests_per_day=1500,
                context_window=2000000,
                max_output_tokens=8192
            ),
            
            "gemini-2.5-flash-04-backup": ModelConfig(
                name="gemini-2.5-flash-preview-04-17",
                api_key="YOUR_SECOND_API_KEY_HERE",
                billing_account="backup",
                priority=ModelPriority.FALLBACK,
                requests_per_minute=120,
                requests_per_day=3000,
                context_window=1000000,
                max_output_tokens=8192
            ),
            
            "gemini-2.5-flash-05-backup": ModelConfig(
                name="gemini-2.5-flash-preview-05-20",
                api_key="YOUR_SECOND_API_KEY_HERE",
                billing_account="backup",
                priority=ModelPriority.FALLBACK,
                requests_per_minute=120,
                requests_per_day=3000,
                context_window=1000000,
                max_output_tokens=8192
            )
        }
    
    def _update_quota_counters(self, model_config: ModelConfig):
        """Update request counters for quota management"""
        current_time = time.time()
        
        # Reset minute counter if needed
        if current_time - model_config.last_minute_reset >= 60:
            model_config.current_requests_minute = 0
            model_config.last_minute_reset = current_time
        
        # Reset day counter if needed
        if current_time - model_config.last_day_reset >= 86400:  # 24 hours
            model_config.current_requests_day = 0
            model_config.last_day_reset = current_time
        
        # Increment counters
        model_config.current_requests_minute += 1
        model_config.current_requests_day += 1
        model_config.last_request_time = current_time
    
    def _get_quota_status(self, model_config: ModelConfig) -> QuotaStatus:
        """Check current quota status for a model"""
        # Check if model is healthy
        if not model_config.is_healthy or model_config.consecutive_errors >= 3:
            return QuotaStatus.ERROR
        
        # Check daily quota
        if model_config.current_requests_day >= model_config.requests_per_day * 0.95:
            return QuotaStatus.EXHAUSTED
        elif model_config.current_requests_day >= model_config.requests_per_day * 0.8:
            return QuotaStatus.LIMITED
        
        # Check minute quota
        if model_config.current_requests_minute >= model_config.requests_per_minute * 0.9:
            return QuotaStatus.LIMITED
        
        return QuotaStatus.AVAILABLE
    
    def _select_optimal_model(self, message_context: Dict[str, Any]) -> Optional[ModelConfig]:
        """
        Intelligently select the best model based on:
        - Current quota status
        - Model capabilities
        - Message complexity
        - Priority levels
        """
        available_models = []
        
        # First pass: collect available models by priority
        for model_id, config in self.models.items():
            quota_status = self._get_quota_status(config)
            
            if quota_status == QuotaStatus.AVAILABLE:
                available_models.append((config, 0))  # No penalty
            elif quota_status == QuotaStatus.LIMITED:
                available_models.append((config, 1))  # Small penalty
            # Skip EXHAUSTED and ERROR models
        
        if not available_models:
            self.logger.warning("No models available, will attempt emergency fallback")
            return None
        
        # Sort by priority and penalty
        available_models.sort(key=lambda x: (x[0].priority.value, x[1]))
        
        # Select based on message complexity
        message_length = len(str(message_context.get('message', '')))
        
        # For complex requests, prefer Pro models
        if message_length > 1000 or message_context.get('requires_reasoning', False):
            for config, penalty in available_models:
                if 'pro' in config.name.lower():
                    return config
        
        # For quick responses, prefer Flash models
        if message_length < 500:
            for config, penalty in available_models:
                if 'flash' in config.name.lower():
                    return config
        
        # Default: return the highest priority available model
        return available_models[0][0]
    
    async def _make_api_call(self, model_config: ModelConfig, messages: List[Dict], **kwargs) -> str:
        """Make actual API call with proper error handling"""
        try:
            # Configure the API client
            genai.configure(api_key=model_config.api_key)
            model = genai.GenerativeModel(model_config.name)
            
            # Prepare the message content
            message_content = messages[-1].get('content', '') if messages else ''
            
            # Set generation config
            generation_config = {
                'temperature': kwargs.get('temperature', model_config.temperature),
                'max_output_tokens': kwargs.get('max_tokens', model_config.max_output_tokens),
                'top_p': kwargs.get('top_p', 0.95),
                'top_k': kwargs.get('top_k', 64),
            }
            
            # Make the API call
            response = await model.generate_content_async(
                message_content,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific quota errors
            if any(quota_term in error_msg for quota_term in ['quota', 'limit', 'rate', 'exceeded']):
                self.logger.warning(f"Quota exceeded for {model_config.name}: {e}")
                model_config.current_requests_day = model_config.requests_per_day  # Mark as exhausted
                raise QuotaExceededException(f"Quota exceeded: {e}")
            
            # Handle other API errors
            model_config.consecutive_errors += 1
            if model_config.consecutive_errors >= 3:
                model_config.is_healthy = False
                model_config.last_error = str(e)
            
            raise APIException(f"API call failed: {e}")
    
    async def generate_response(
        self, 
        messages: List[Dict], 
        mama_bear_context: Dict[str, Any],
        **kwargs
    ) -> MamaBearResponse:
        """
        Main method to generate a response with intelligent model selection and failover
        """
        start_time = time.time()
        fallback_count = 0
        quota_warnings = []
        
        # Prepare message context for model selection
        message_context = {
            'message': messages[-1].get('content', '') if messages else '',
            'conversation_length': len(messages),
            'mama_bear_variant': mama_bear_context.get('variant', 'main_chat'),
            'requires_reasoning': kwargs.get('requires_reasoning', False),
            'priority': kwargs.get('priority', 'normal')
        }
        
        while fallback_count < 6:  # Max 6 attempts (all models)
            try:
                # Select optimal model
                selected_model = self._select_optimal_model(message_context)
                
                if not selected_model:
                    # Emergency delay before trying again
                    await asyncio.sleep(min(self.global_fallback_delay * (2 ** fallback_count), self.max_fallback_delay))
                    fallback_count += 1
                    continue
                
                # Update quota counters
                self._update_quota_counters(selected_model)
                
                # Log the attempt
                self.logger.info(f"Attempting request with {selected_model.name} (account: {selected_model.billing_account})")
                
                # Make the API call
                response_content = await self._make_api_call(selected_model, messages, **kwargs)
                
                # Success! Reset error counters
                selected_model.consecutive_errors = 0
                selected_model.is_healthy = True
                
                # Create response object
                processing_time = time.time() - start_time
                
                return MamaBearResponse(
                    content=response_content,
                    model_used=selected_model.name,
                    api_key_used=selected_model.api_key[:20] + "...",  # Partial key for logging
                    billing_account=selected_model.billing_account,
                    processing_time=processing_time,
                    fallback_count=fallback_count,
                    quota_warnings=quota_warnings
                )
                
            except QuotaExceededException as e:
                quota_warnings.append(f"Quota exceeded for {selected_model.name if 'selected_model' in locals() else 'unknown model'}")
                self.logger.warning(f"Quota exceeded, attempting fallback: {e}")
                fallback_count += 1
                
                # Wait before retry
                await asyncio.sleep(min(self.global_fallback_delay * fallback_count, 5.0))
                
            except APIException as e:
                self.logger.error(f"API error, attempting fallback: {e}")
                fallback_count += 1
                
                # Wait before retry
                await asyncio.sleep(min(self.global_fallback_delay * fallback_count, 10.0))
                
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                fallback_count += 1
                await asyncio.sleep(2.0)
        
        # If we get here, all models failed
        raise AllModelsFailedException("All Gemini models are currently unavailable")
    
    async def _background_health_monitor(self):
        """Background task to monitor and recover model health"""
        while True:
            try:
                await asyncio.sleep(self.health_check_interval)
                
                for model_id, config in self.models.items():
                    # Reset error counters for models that have been failing
                    if not config.is_healthy and time.time() - config.last_request_time > 1800:  # 30 minutes
                        config.consecutive_errors = 0
                        config.is_healthy = True
                        config.last_error = None
                        self.logger.info(f"Restored health status for {config.name}")
                
                # Adjust global fallback delay based on recent performance
                recent_requests = [r for r in self.request_history if time.time() - r['timestamp'] < 3600]
                if len(recent_requests) > 0:
                    avg_fallbacks = sum(r['fallback_count'] for r in recent_requests) / len(recent_requests)
                    if avg_fallbacks > 2:
                        self.global_fallback_delay = min(self.global_fallback_delay * 1.1, self.max_fallback_delay)
                    else:
                        self.global_fallback_delay = max(self.global_fallback_delay * 0.9, 1.0)
                
            except Exception as e:
                self.logger.error(f"Health monitor error: {e}")
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current status of all models for monitoring"""
        status = {}
        
        for model_id, config in self.models.items():
            quota_status = self._get_quota_status(config)
            
            status[model_id] = {
                'name': config.name,
                'billing_account': config.billing_account,
                'priority': config.priority.name,
                'quota_status': quota_status.value,
                'requests_today': config.current_requests_day,
                'requests_this_minute': config.current_requests_minute,
                'is_healthy': config.is_healthy,
                'consecutive_errors': config.consecutive_errors,
                'last_error': config.last_error
            }
        
        return status
    
    async def warm_up_models(self):
        """Warm up all models with test requests to check availability"""
        self.logger.info("Starting model warm-up...")
        
        test_message = [{'role': 'user', 'content': 'Hello, this is a test. Please respond with "Ready".'}]
        
        for model_id, config in self.models.items():
            try:
                await self._make_api_call(config, test_message)
                self.logger.info(f"✓ {config.name} is ready")
            except Exception as e:
                self.logger.warning(f"✗ {config.name} failed warm-up: {e}")
                config.is_healthy = False

# Custom exceptions
class QuotaExceededException(Exception):
    pass

class APIException(Exception):
    pass

class AllModelsFailedException(Exception):
    pass


# Integration with existing Mama Bear Agent
class EnhancedMamaBearAgent:
    """Enhanced Mama Bear Agent with intelligent model management"""
    
    def __init__(self, scrapybara_client, memory_manager):
        self.scrapybara = scrapybara_client
        self.memory = memory_manager
        self.model_manager = MamaBearModelManager()
        
        # Initialize model manager
        asyncio.create_task(self.model_manager.warm_up_models())
        
        self.variants = {
            'main_chat': ResearchSpecialist(),
            'vm_hub': DevOpsSpecialist(),
            'scout': ScoutCommander(),
            'multi_modal': ModelCoordinator(),
            'mcp_hub': ToolCurator(),
            'integration': IntegrationArchitect(),
            'live_api': LiveAPISpecialist()
        }
    
    async def process_message(self, message, page_context, user_id, **kwargs):
        """Process message with intelligent model selection"""
        try:
            # Get appropriate variant
            variant = self.variants.get(page_context, self.variants['main_chat'])
            
            # Load conversation memory
            context = await self.memory.get_context(user_id, page_context)
            
            # Prepare messages for the model
            messages = [
                {'role': 'system', 'content': variant.get_system_prompt()},
                {'role': 'user', 'content': message}
            ]
            
            # Add context if available
            if context:
                context_message = f"Previous context: {context}"
                messages.insert(1, {'role': 'system', 'content': context_message})
            
            # Determine if this requires advanced reasoning
            requires_reasoning = any(keyword in message.lower() for keyword in [
                'analyze', 'compare', 'explain', 'research', 'strategy', 'plan', 'design'
            ])
            
            # Generate response using model manager
            mama_bear_context = {
                'variant': page_context,
                'user_id': user_id,
                'session_context': context
            }
            
            response = await self.model_manager.generate_response(
                messages=messages,
                mama_bear_context=mama_bear_context,
                requires_reasoning=requires_reasoning,
                **kwargs
            )
            
            # Save to memory
            await self.memory.save_interaction(user_id, message, response.content)
            
            # Return enhanced response with metadata
            return {
                'content': response.content,
                'metadata': {
                    'model_used': response.model_used,
                    'billing_account': response.billing_account,
                    'processing_time': response.processing_time,
                    'fallback_count': response.fallback_count,
                    'quota_warnings': response.quota_warnings,
                    'mama_bear_variant': variant.__class__.__name__
                }
            }
            
        except AllModelsFailedException:
            # Emergency fallback response
            return {
                'content': "I'm experiencing technical difficulties with my AI models right now. Please try again in a few minutes. I'm working on resolving this! 🐻💙",
                'metadata': {
                    'error': 'all_models_failed',
                    'fallback_response': True
                }
            }
        
        except Exception as e:
            self.logger.error(f"Unexpected error in process_message: {e}")
            return {
                'content': "I encountered an unexpected error. Let me try to help you in a different way! 🐻",
                'metadata': {
                    'error': str(e),
                    'fallback_response': True
                }
            }
    
    async def get_system_status(self):
        """Get comprehensive system status"""
        return {
            'model_status': self.model_manager.get_model_status(),
            'memory_status': await self.memory.get_status(),
            'active_variants': list(self.variants.keys()),
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_response(self, prompt: str, mama_bear_variant: str = 'research_specialist', required_capabilities: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Orchestration-compatible response method
        Maps to the existing process_message method for compatibility
        """
        try:
            # Convert orchestration parameters to process_message format
            result = await self.process_message(
                message=prompt,
                page_context=kwargs.get('page_context', 'orchestration'),
                user_id=kwargs.get('user_id', 'system'),
                variant_preference=mama_bear_variant,
                **kwargs
            )
            
            return {
                'success': True,
                'content': result['content'],
                'model_used': result.get('model', 'unknown'),
                'variant_used': result.get('variant', mama_bear_variant)
            }
            
        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': f"🐻 I encountered an issue: {str(e)}"
            }