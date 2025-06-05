# backend/services/mama_bear_model_manager.py
# 🔧 FIXED: Updated get_response method to handle orchestration parameters correctly

async def get_response(self, prompt: str = None, message: str = None, 
                      mama_bear_variant: str = 'research_specialist', 
                      required_capabilities: Optional[List[str]] = None,
                      user_id: str = "default_user", 
                      page_context: str = "main_chat", **kwargs) -> Dict[str, Any]:
    """
    🐻 Orchestration-compatible response method
    Handles both 'prompt' and 'message' parameters for compatibility
    """
    try:
        # Handle parameter flexibility - accept both 'prompt' and 'message'
        actual_message = prompt or message
        if not actual_message:
            return {
                'success': False,
                'error': 'No message or prompt provided',
                'content': '🐻 I need a message to respond to!'
            }
        
        # Map mama_bear_variant to page_context for internal processing
        variant_to_context = {
            'research_specialist': 'main_chat',
            'devops_specialist': 'vm_hub', 
            'scout_commander': 'scout',
            'model_coordinator': 'multi_modal',
            'tool_curator': 'mcp_hub',
            'integration_architect': 'integration',
            'live_api_specialist': 'live_api',
            'lead_developer': 'main_chat'
        }
        
        mapped_context = variant_to_context.get(mama_bear_variant, page_context)
        
        # Call the existing process_message method
        result = await self.process_message(
            message=actual_message,
            page_context=mapped_context,
            user_id=user_id,
            variant_preference=mama_bear_variant,
            required_capabilities=required_capabilities,
            **kwargs
        )
        
        # Return orchestration-compatible format
        if result and isinstance(result, dict):
            return {
                'success': True,
                'response': result.get('content', ''),
                'content': result.get('content', ''),
                'model_used': result.get('metadata', {}).get('model_used', 'unknown'),
                'variant_used': mama_bear_variant,
                'metadata': result.get('metadata', {})
            }
        else:
            return {
                'success': False,
                'error': 'Invalid response from process_message',
                'content': '🐻 I had trouble processing that request.'
            }
            
    except Exception as e:
        self.logger.error(f"Error in get_response: {e}")
        return {
            'success': False,
            'error': str(e),
            'content': f"🐻 I encountered an issue: {str(e)}"
        }

# 🔧 ADDITIONAL FIX: Ensure EnhancedMamaBearAgent has proper logger
class EnhancedMamaBearAgent:
    """Enhanced Mama Bear Agent with intelligent model management"""
    
    def __init__(self, scrapybara_client, memory_manager):
        self.scrapybara = scrapybara_client
        self.memory = memory_manager
        self.model_manager = MamaBearModelManager()
        self.logger = logging.getLogger(__name__)  # 🔧 Added missing logger
        
        # Initialize model manager
        asyncio.create_task(self.model_manager.warm_up_models())
        
        # Import here to avoid circular imports
        try:
            from .mama_bear_specialized_variants import (
                ResearchSpecialist, DevOpsSpecialist, ScoutCommander,
                ModelCoordinator, ToolCurator, IntegrationArchitect, LiveAPISpecialist
            )
            
            self.variants = {
                'main_chat': ResearchSpecialist(),
                'vm_hub': DevOpsSpecialist(),
                'scout': ScoutCommander(),
                'multi_modal': ModelCoordinator(),
                'mcp_hub': ToolCurator(),
                'integration': IntegrationArchitect(),
                'live_api': LiveAPISpecialist()
            }
        except ImportError as e:
            self.logger.warning(f"Could not import specialized variants: {e}")
            self.variants = {}

    # 🔧 Updated process_message to handle variant_preference
    async def process_message(self, message, page_context, user_id, variant_preference=None, **kwargs):
        """Process message with intelligent model selection"""
        try:
            # Use variant preference if provided
            if variant_preference and variant_preference in ['research_specialist', 'devops_specialist', 'scout_commander', 'model_coordinator', 'tool_curator', 'integration_architect', 'live_api_specialist']:
                # Map specialist names to page contexts
                specialist_mapping = {
                    'research_specialist': 'main_chat',
                    'devops_specialist': 'vm_hub',
                    'scout_commander': 'scout',
                    'model_coordinator': 'multi_modal',
                    'tool_curator': 'mcp_hub',
                    'integration_architect': 'integration',
                    'live_api_specialist': 'live_api'
                }
                page_context = specialist_mapping.get(variant_preference, page_context)
            
            # Get appropriate variant
            variant = self.variants.get(page_context, list(self.variants.values())[0] if self.variants else None)
            
            if not variant:
                # Fallback when no variants available
                return {
                    'content': f"🐻 Enhanced Mama Bear processing: {message}. I'm ready to help!",
                    'metadata': {
                        'model_used': 'fallback',
                        'variant_used': 'enhanced_mama_bear',
                        'fallback_response': True
                    }
                }
            
            # Load conversation memory if available
            context = {}
            if hasattr(self.memory, 'get_relevant_context'):
                try:
                    context = await self.memory.get_relevant_context(user_id, message, limit=3)
                except Exception as e:
                    self.logger.warning(f"Could not load context: {e}")
            
            # Prepare messages for the model
            messages = [
                {'role': 'system', 'content': variant.get_system_prompt()},
                {'role': 'user', 'content': message}
            ]
            
            # Add context if available
            if context and isinstance(context, list) and len(context) > 0:
                context_summary = "\n".join([str(c.get('content', '')) for c in context[:2]])
                if context_summary.strip():
                    messages.insert(1, {'role': 'system', 'content': f"Recent context: {context_summary}"})
            
            # Determine if this requires advanced reasoning
            requires_reasoning = any(keyword in message.lower() for keyword in [
                'analyze', 'compare', 'explain', 'research', 'strategy', 'plan', 'design', 'orchestrat'
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
            
            # Save to memory if available
            if hasattr(self.memory, 'save_interaction'):
                try:
                    await self.memory.save_interaction(
                        user_id=user_id, 
                        message=message, 
                        response=response.content,
                        metadata={
                            'agent_id': variant_preference or page_context,
                            'model_used': response.model_used,
                            'processing_time': response.processing_time
                        }
                    )
                except Exception as e:
                    self.logger.warning(f"Could not save interaction: {e}")
            
            # Return enhanced response with metadata
            return {
                'content': response.content,
                'metadata': {
                    'model_used': response.model_used,
                    'billing_account': response.billing_account,
                    'processing_time': response.processing_time,
                    'fallback_count': response.fallback_count,
                    'quota_warnings': response.quota_warnings,
                    'mama_bear_variant': variant.__class__.__name__,
                    'variant_used': variant_preference or page_context
                }
            }
            
        except Exception as e:
            self.logger.error(f"Unexpected error in process_message: {e}")
            return {
                'content': f"🐻 Enhanced Mama Bear processing: {message}. I encountered an issue but I'm working on it!",
                'metadata': {
                    'error': str(e),
                    'fallback_response': True,
                    'variant_used': variant_preference or page_context
                }
            }

    # Keep the existing get_response method with the fixes above
    async def get_response(self, prompt: str = None, message: str = None, 
                          mama_bear_variant: str = 'research_specialist', 
                          required_capabilities: Optional[List[str]] = None,
                          user_id: str = "default_user", 
                          page_context: str = "main_chat", **kwargs) -> Dict[str, Any]:
        """Orchestration-compatible response method - see implementation above"""
        # Implementation as shown above
        pass