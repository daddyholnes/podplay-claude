"""
Enhanced Mama Bear Agent Service
Provides 7 specialized AI agent variants with persistent memory and context switching
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import google.generativeai as genai
from anthropic import Anthropic
import openai
from mem0 import Memory

logger = logging.getLogger(__name__)

class MamaBearVariant:
    """Individual Mama Bear AI variant with specialized personality and capabilities"""
    
    def __init__(self, variant_type: str, config: Dict[str, Any]):
        self.variant_type = variant_type
        self.personality = config.get('personality', '')
        self.expertise = config.get('expertise', [])
        self.system_prompt = self._build_system_prompt()
        self.context_memory = []
        
    def _build_system_prompt(self) -> str:
        """Build specialized system prompt for this variant"""
        base_prompt = f"""You are Mama Bear {self.variant_type.title()}, a specialized AI assistant in the Podplay Sanctuary - a neurodivergent-friendly development platform.

Your personality: {self.personality}
Your expertise: {', '.join(self.expertise)}

Core principles:
- Be patient, understanding, and supportive
- Break down complex concepts into manageable steps
- Provide sensory-friendly guidance (avoid overwhelming information dumps)
- Maintain context across conversations through persistent memory
- Adapt communication style to user's needs and preferences
- Always prioritize user wellbeing and cognitive comfort

You are part of a sanctuary environment designed to eliminate context switching and provide seamless development support."""

        variant_specific = {
            'architect': "Focus on system design, scalability, and technical architecture. Help structure complex projects into manageable components.",
            'designer': "Emphasize visual design, user experience, and accessibility. Create beautiful, intuitive interfaces with sensory-friendly themes.",
            'guide': "Provide patient, step-by-step guidance. Excel at breaking down complex topics and teaching new concepts.",
            'connector': "Specialize in integrations, APIs, and real-time systems. Bridge different technologies seamlessly.",
            'multimedia': "Handle rich media, file processing, and multi-modal interactions. Make complex media tasks simple.",
            'scout': "Research new technologies, explore possibilities, and provide innovative solutions. Always curious and forward-thinking.",
            'guardian': "Focus on security, reliability, and production readiness. Ensure safe, robust implementations."
        }
        
        return base_prompt + "\n\n" + variant_specific.get(self.variant_type, '')

class EnhancedMamaBearAgent:
    """Enhanced Mama Bear Agent with 7 specialized variants and persistent memory"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory = Memory()
        self.active_variant = 'architect'  # Default variant
        
        # Initialize AI clients
        self.anthropic = Anthropic(api_key=config.get('anthropic_api_key'))
        self.openai_client = openai.OpenAI(api_key=config.get('openai_api_key'))
        genai.configure(api_key=config.get('google_api_key'))
        
        # Initialize variants
        self.variants = self._initialize_variants()
        
        # Conversation context
        self.conversation_id = None
        self.user_preferences = {}
        
        logger.info("Enhanced Mama Bear Agent initialized with 7 variants")
    
    def _initialize_variants(self) -> Dict[str, MamaBearVariant]:
        """Initialize all 7 Mama Bear variants"""
        variant_configs = {
            'architect': {
                'personality': 'Systematic, methodical, focuses on structure and scalability',
                'expertise': ['Backend design', 'Service architecture', 'System integration', 'Database design']
            },
            'designer': {
                'personality': 'Creative, aesthetic-focused, emphasizes user experience',
                'expertise': ['UI/UX design', 'Theme systems', 'Visual accessibility', 'Component libraries']
            },
            'guide': {
                'personality': 'Patient, educational, breaks down complex concepts',
                'expertise': ['Documentation', 'User guidance', 'Feature explanation', 'Learning paths']
            },
            'connector': {
                'personality': 'Integration-focused, handles communication between systems',
                'expertise': ['APIs', 'WebSockets', 'Real-time systems', 'Service integration']
            },
            'multimedia': {
                'personality': 'Handles rich media, audio/video processing',
                'expertise': ['File handling', 'Media processing', 'Multi-modal interfaces', 'Streaming']
            },
            'scout': {
                'personality': 'Research-oriented, explores new technologies',
                'expertise': ['Technology research', 'Integration testing', 'Innovation', 'Trend analysis']
            },
            'guardian': {
                'personality': 'Security and reliability focused, ensures safe operations',
                'expertise': ['Security', 'Error handling', 'Production readiness', 'Performance optimization']
            }
        }
        
        return {
            variant_type: MamaBearVariant(variant_type, config)
            for variant_type, config in variant_configs.items()
        }
    
    async def switch_variant(self, variant_type: str, user_id: str) -> Dict[str, Any]:
        """Switch to a different Mama Bear variant with context preservation"""
        if variant_type not in self.variants:
            raise ValueError(f"Unknown variant: {variant_type}")
        
        # Save current context to memory
        if self.active_variant:
            await self._save_context_to_memory(user_id, self.active_variant)
        
        # Switch variant
        old_variant = self.active_variant
        self.active_variant = variant_type
        
        # Load context for new variant
        context = await self._load_context_from_memory(user_id, variant_type)
        
        logger.info(f"Switched from {old_variant} to {variant_type} for user {user_id}")
        
        return {
            'previous_variant': old_variant,
            'current_variant': variant_type,
            'personality': self.variants[variant_type].personality,
            'expertise': self.variants[variant_type].expertise,
            'context_preserved': len(context) > 0
        }
    
    async def chat(self, message: str, user_id: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Main chat interface with the active Mama Bear variant"""
        try:
            # Get current variant
            current_variant = self.variants[self.active_variant]
            
            # Load conversation history from memory
            conversation_history = await self._get_conversation_history(user_id)
            
            # Prepare enhanced prompt with context
            enhanced_prompt = await self._build_enhanced_prompt(
                message, current_variant, conversation_history, context
            )
            
            # Select best model for the task
            model_choice = await self._select_optimal_model(message, current_variant.expertise)
            
            # Generate response
            response = await self._generate_response(enhanced_prompt, model_choice)
            
            # Save to memory
            await self._save_interaction_to_memory(user_id, message, response)
            
            return {
                'response': response,
                'variant': self.active_variant,
                'model_used': model_choice,
                'context_used': len(conversation_history),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Chat error with variant {self.active_variant}: {str(e)}")
            return {
                'error': 'I encountered an issue processing your request. Let me try a different approach.',
                'variant': self.active_variant,
                'fallback': True
            }
    
    async def _build_enhanced_prompt(self, message: str, variant: MamaBearVariant, 
                                   history: List[Dict], context: Optional[Dict]) -> str:
        """Build enhanced prompt with context and memory"""
        prompt_parts = [
            variant.system_prompt,
            "\n--- Recent Conversation History ---"
        ]
        
        # Add recent conversation history
        for interaction in history[-5:]:  # Last 5 interactions
            prompt_parts.append(f"User: {interaction.get('user_message', '')}")
            prompt_parts.append(f"Assistant: {interaction.get('assistant_response', '')}")
        
        # Add current context if provided
        if context:
            prompt_parts.append(f"\n--- Current Context ---")
            prompt_parts.append(json.dumps(context, indent=2))
        
        # Add current user message
        prompt_parts.extend([
            "\n--- Current User Message ---",
            message,
            "\nProvide a helpful, supportive response as Mama Bear. Consider the conversation history and current context."
        ])
        
        return "\n".join(prompt_parts)
    
    async def _select_optimal_model(self, message: str, expertise: List[str]) -> str:
        """Select the best AI model based on the task and variant expertise"""
        # Simple heuristics for model selection
        if any(keyword in message.lower() for keyword in ['code', 'debug', 'implement', 'function']):
            return 'claude-3-5-sonnet-20241022'  # Best for coding
        elif any(keyword in message.lower() for keyword in ['creative', 'design', 'idea', 'brainstorm']):
            return 'gemini-1.5-pro'  # Good for creative tasks
        elif 'Backend design' in expertise or 'System integration' in expertise:
            return 'claude-3-5-sonnet-20241022'  # Architecture tasks
        else:
            return 'claude-3-5-haiku-20241022'  # General conversation
    
    async def _generate_response(self, prompt: str, model: str) -> str:
        """Generate response using the selected model"""
        try:
            if model.startswith('claude'):
                response = self.anthropic.messages.create(
                    model=model,
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif model.startswith('gpt'):
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000
                )
                return response.choices[0].message.content
            
            elif model.startswith('gemini'):
                model_instance = genai.GenerativeModel(model)
                response = model_instance.generate_content(prompt)
                try:
                    return response.text
                except ValueError:
                    logger.warning(f"Gemini response for model {model} did not contain direct text. Parts: {response.parts if hasattr(response, 'parts') else 'N/A'}")
                    if response.candidates and hasattr(response.candidates[0], 'content') and response.candidates[0].content and hasattr(response.candidates[0].content, 'parts') and response.candidates[0].content.parts:
                        return "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, "text"))
                    logger.warning(f"Could not extract text from Gemini response for model {model}.")
                    return "" # Or raise an error / return specific message
            
            else:
                # Fallback to Claude
                response = self.anthropic.messages.create(
                    model='claude-3-5-haiku-20241022',
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
                
        except Exception as e:
            logger.error(f"Error generating response with {model}: {str(e)}")
            return "I'm having trouble generating a response right now. Could you try rephrasing your question?"
    
    async def _get_conversation_history(self, user_id: str) -> List[Dict]:
        """Retrieve conversation history from memory"""
        try:
            memories = self.memory.search(f"user:{user_id} conversation", limit=10)
            return [memory.get('data', {}) for memory in memories]
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {str(e)}")
            return []
    
    async def _save_interaction_to_memory(self, user_id: str, user_message: str, assistant_response: str):
        """Save interaction to persistent memory"""
        try:
            interaction_data = {
                'user_message': user_message,
                'assistant_response': assistant_response,
                'variant': self.active_variant,
                'timestamp': datetime.now().isoformat()
            }
            
            self.memory.add(
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": assistant_response}
                ],
                user_id=user_id,
                metadata={
                    "variant": self.active_variant,
                    "interaction_type": "chat",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error saving interaction to memory: {str(e)}")
    
    async def _save_context_to_memory(self, user_id: str, variant: str):
        """Save current context when switching variants"""
        try:
            context_data = {
                'variant': variant,
                'timestamp': datetime.now().isoformat(),
                'conversation_state': 'paused'
            }
            
            self.memory.add(
                messages=[{"role": "system", "content": f"Context saved for variant {variant}"}],
                user_id=user_id,
                metadata=context_data
            )
            
        except Exception as e:
            logger.error(f"Error saving context to memory: {str(e)}")
    
    async def _load_context_from_memory(self, user_id: str, variant: str) -> List[Dict]:
        """Load context for a specific variant"""
        try:
            memories = self.memory.search(
                f"user:{user_id} variant:{variant}",
                limit=5
            )
            return [memory.get('data', {}) for memory in memories]
        except Exception as e:
            logger.error(f"Error loading context from memory: {str(e)}")
            return []
    
    def get_variant_info(self, variant_type: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a specific variant or all variants"""
        if variant_type:
            if variant_type not in self.variants:
                return {'error': f'Unknown variant: {variant_type}'}
            
            variant = self.variants[variant_type]
            return {
                'type': variant_type,
                'personality': variant.personality,
                'expertise': variant.expertise,
                'active': variant_type == self.active_variant
            }
        else:
            return {
                'variants': {
                    vtype: {
                        'personality': variant.personality,
                        'expertise': variant.expertise,
                        'active': vtype == self.active_variant
                    }
                    for vtype, variant in self.variants.items()
                },
                'active_variant': self.active_variant
            }
    
    async def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user preferences and interaction patterns"""
        try:
            memories = self.memory.search(f"user:{user_id}", limit=50)
            
            # Analyze interaction patterns
            variant_usage = {}
            total_interactions = len(memories)
            
            for memory in memories:
                metadata = memory.get('metadata', {})
                variant = metadata.get('variant', 'unknown')
                variant_usage[variant] = variant_usage.get(variant, 0) + 1
            
            return {
                'total_interactions': total_interactions,
                'variant_preferences': variant_usage,
                'most_used_variant': max(variant_usage, key=variant_usage.get) if variant_usage else None,
                'interaction_history_available': total_interactions > 0
            }
            
        except Exception as e:
            logger.error(f"Error getting user insights: {str(e)}")
            return {'error': 'Unable to retrieve user insights'}
