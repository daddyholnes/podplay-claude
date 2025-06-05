"""
Comprehensive Scrapybara Integration for Podplay Sanctuary
Provides computer use agent capabilities with multi-provider model fallback
and seamless integration with Mama Bear orchestration system.
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import time
from contextlib import asynccontextmanager

try:
    from scrapybara import Scrapybara, ScrapybaraClient
    from scrapybara.tools import BashTool, ComputerTool, EditTool
    from scrapybara.openai import OpenAI, UBUNTU_SYSTEM_PROMPT as OPENAI_UBUNTU_PROMPT
    from scrapybara.anthropic import Anthropic, UBUNTU_SYSTEM_PROMPT as ANTHROPIC_UBUNTU_PROMPT
    SCRAPYBARA_AVAILABLE = True
except ImportError:
    # Fallback for when Scrapybara SDK is not installed
    SCRAPYBARA_AVAILABLE = False
    BashTool = ComputerTool = EditTool = None
    OpenAI = Anthropic = None
    OPENAI_UBUNTU_PROMPT = ANTHROPIC_UBUNTU_PROMPT = ""

# Custom Gemini model adapter for Scrapybara compatibility
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None


class ModelProvider(Enum):
    """Supported model providers for fallback chain"""
    SCRAPYBARA_CREDITS = "scrapybara_credits"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class InstanceType(Enum):
    """Scrapybara instance types"""
    UBUNTU = "ubuntu"
    BROWSER = "browser"
    WINDOWS = "windows"


@dataclass
class ScrapybaraConfig:
    """Configuration for Scrapybara integration"""
    api_key: Optional[str] = None
    default_timeout_hours: int = 1
    max_instances: int = 5
    default_instance_type: InstanceType = InstanceType.UBUNTU
    enable_browser_auth: bool = True
    model_fallback_chain: List[ModelProvider] = field(default_factory=lambda: [
        ModelProvider.SCRAPYBARA_CREDITS,
        ModelProvider.GEMINI,
        ModelProvider.ANTHROPIC,
        ModelProvider.OPENAI
    ])


@dataclass
class ModelConfig:
    """Configuration for different model providers"""
    provider: ModelProvider
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    enabled: bool = True


class GeminiScrapybaraAdapter:
    """Custom adapter to make Gemini compatible with Scrapybara Act SDK"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-pro"):
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI package not available. Install with: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model_name = model_name
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name)
        else:
            raise ValueError("Gemini API key required")
    
    async def generate_response(self, messages: List[Dict], tools: List[Any] = None) -> Dict:
        """Generate response compatible with Scrapybara Act SDK format"""
        try:
            # Convert messages to Gemini format
            prompt = self._convert_messages_to_prompt(messages)
            
            # Generate response
            response = await self.model.generate_content_async(prompt)
            
            # Convert back to Scrapybara format
            return {
                'text': response.text,
                'tool_calls': [],  # TODO: Implement tool calling for Gemini
                'usage': {
                    'input_tokens': 0,  # Gemini doesn't provide detailed token counts
                    'output_tokens': 0
                }
            }
        except Exception as e:
            logging.error(f"Gemini generation error: {e}")
            raise
    
    def _convert_messages_to_prompt(self, messages: List[Dict]) -> str:
        """Convert chat messages to Gemini prompt format"""
        prompt_parts = []
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                prompt_parts.append(f"System Instructions: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n\n".join(prompt_parts)


@dataclass
class ScrapybaraInstance:
    """Represents a managed Scrapybara instance"""
    instance_id: str
    instance_type: InstanceType
    instance: Any  # The actual Scrapybara instance
    created_at: float
    timeout_hours: int
    tools: List[Any] = field(default_factory=list)
    auth_states: Dict[str, str] = field(default_factory=dict)
    is_active: bool = True
    
    def get_age_hours(self) -> float:
        """Get instance age in hours"""
        return (time.time() - self.created_at) / 3600
    
    def is_expired(self) -> bool:
        """Check if instance has exceeded timeout"""
        return self.get_age_hours() >= self.timeout_hours


class ScrapybaraManager:
    """Manages Scrapybara instances and provides computer use capabilities"""
    
    def __init__(self, config: ScrapybaraConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize Scrapybara client
        if SCRAPYBARA_AVAILABLE:
            self.client = Scrapybara(api_key=config.api_key)
        else:
            self.client = None
            self.logger.warning("Scrapybara SDK not available")
        
        # Instance management
        self.instances: Dict[str, ScrapybaraInstance] = {}
        self.model_configs: Dict[ModelProvider, ModelConfig] = {}
        
        # Initialize model adapters
        self.gemini_adapter = None
        self._setup_model_configs()
        
    def _setup_model_configs(self):
        """Setup model configurations for fallback chain"""
        # Scrapybara credits (default, no API key needed)
        self.model_configs[ModelProvider.SCRAPYBARA_CREDITS] = ModelConfig(
            provider=ModelProvider.SCRAPYBARA_CREDITS,
            enabled=True
        )
        
        # Gemini
        gemini_api_key = os.getenv('GOOGLE_API_KEY')
        self.model_configs[ModelProvider.GEMINI] = ModelConfig(
            provider=ModelProvider.GEMINI,
            api_key=gemini_api_key,
            model_name="gemini-1.5-pro",
            enabled=GEMINI_AVAILABLE and bool(gemini_api_key)
        )
        
        # Anthropic
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model_configs[ModelProvider.ANTHROPIC] = ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            api_key=anthropic_api_key,
            model_name="claude-3-5-sonnet-20241022",
            enabled=bool(anthropic_api_key)
        )
        
        # OpenAI
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.model_configs[ModelProvider.OPENAI] = ModelConfig(
            provider=ModelProvider.OPENAI,
            api_key=openai_api_key,
            model_name="gpt-4o",
            enabled=bool(openai_api_key)
        )
        
        # Initialize Gemini adapter if available
        if self.model_configs[ModelProvider.GEMINI].enabled:
            try:
                self.gemini_adapter = GeminiScrapybaraAdapter(
                    api_key=gemini_api_key,
                    model_name="gemini-1.5-pro"
                )
            except Exception as e:
                self.logger.warning(f"Failed to initialize Gemini adapter: {e}")
                self.model_configs[ModelProvider.GEMINI].enabled = False
    
    async def create_instance(
        self,
        instance_type: InstanceType = None,
        timeout_hours: int = None,
        instance_id: str = None
    ) -> Optional[ScrapybaraInstance]:
        """Create a new Scrapybara instance"""
        if not SCRAPYBARA_AVAILABLE:
            self.logger.error("Scrapybara SDK not available")
            return None
        
        if len(self.instances) >= self.config.max_instances:
            # Clean up expired instances
            await self.cleanup_expired_instances()
            
            if len(self.instances) >= self.config.max_instances:
                self.logger.error("Maximum instances limit reached")
                return None
        
        instance_type = instance_type or self.config.default_instance_type
        timeout_hours = timeout_hours or self.config.default_timeout_hours
        instance_id = instance_id or f"{instance_type.value}_{int(time.time())}"
        
        try:
            # Create instance based on type
            if instance_type == InstanceType.UBUNTU:
                scrapybara_instance = self.client.start_ubuntu(timeout_hours=timeout_hours)
            elif instance_type == InstanceType.BROWSER:
                scrapybara_instance = self.client.start_browser(timeout_hours=timeout_hours)
            elif instance_type == InstanceType.WINDOWS:
                scrapybara_instance = self.client.start_windows(timeout_hours=timeout_hours)
            else:
                raise ValueError(f"Unsupported instance type: {instance_type}")
            
            # Create tools for the instance
            tools = [
                BashTool(scrapybara_instance),
                ComputerTool(scrapybara_instance),
                EditTool(scrapybara_instance)
            ]
            
            # Initialize browser if needed
            if instance_type in [InstanceType.BROWSER, InstanceType.UBUNTU] and self.config.enable_browser_auth:
                try:
                    scrapybara_instance.browser.start()
                except Exception as e:
                    self.logger.warning(f"Failed to initialize browser: {e}")
            
            # Create managed instance
            managed_instance = ScrapybaraInstance(
                instance_id=instance_id,
                instance_type=instance_type,
                instance=scrapybara_instance,
                created_at=time.time(),
                timeout_hours=timeout_hours,
                tools=tools
            )
            
            self.instances[instance_id] = managed_instance
            self.logger.info(f"Created Scrapybara instance: {instance_id}")
            
            return managed_instance
            
        except Exception as e:
            self.logger.error(f"Failed to create Scrapybara instance: {e}")
            return None
    
    async def get_instance(self, instance_id: str) -> Optional[ScrapybaraInstance]:
        """Get a managed instance by ID"""
        instance = self.instances.get(instance_id)
        if instance and instance.is_expired():
            await self.stop_instance(instance_id)
            return None
        return instance
    
    async def stop_instance(self, instance_id: str) -> bool:
        """Stop and remove an instance"""
        instance = self.instances.get(instance_id)
        if not instance:
            return False
        
        try:
            instance.instance.stop()
            instance.is_active = False
            del self.instances[instance_id]
            self.logger.info(f"Stopped Scrapybara instance: {instance_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop instance {instance_id}: {e}")
            return False
    
    async def cleanup_expired_instances(self):
        """Clean up expired instances"""
        expired_instances = [
            instance_id for instance_id, instance in self.instances.items()
            if instance.is_expired()
        ]
        
        for instance_id in expired_instances:
            await self.stop_instance(instance_id)
    
    def get_available_model(self) -> Optional[Any]:
        """Get the first available model from the fallback chain"""
        for provider in self.config.model_fallback_chain:
            config = self.model_configs.get(provider)
            if config and config.enabled:
                try:
                    if provider == ModelProvider.SCRAPYBARA_CREDITS:
                        if SCRAPYBARA_AVAILABLE:
                            return OpenAI()  # Default Scrapybara model with credits
                    elif provider == ModelProvider.GEMINI:
                        return self.gemini_adapter
                    elif provider == ModelProvider.ANTHROPIC:
                        if SCRAPYBARA_AVAILABLE:
                            return Anthropic(api_key=config.api_key)
                    elif provider == ModelProvider.OPENAI:
                        if SCRAPYBARA_AVAILABLE:
                            return OpenAI(api_key=config.api_key)
                except Exception as e:
                    self.logger.warning(f"Failed to initialize {provider.value} model: {e}")
                    continue
        
        self.logger.error("No available models in fallback chain")
        return None
    
    def get_system_prompt(self, instance_type: InstanceType = None) -> str:
        """Get appropriate system prompt for instance type"""
        instance_type = instance_type or self.config.default_instance_type
        
        if instance_type == InstanceType.UBUNTU:
            return OPENAI_UBUNTU_PROMPT or ANTHROPIC_UBUNTU_PROMPT
        elif instance_type == InstanceType.BROWSER:
            return "You are a computer use agent specialized in browser automation and web interaction."
        elif instance_type == InstanceType.WINDOWS:
            return "You are a computer use agent specialized in Windows desktop automation."
        else:
            return "You are a computer use agent capable of controlling desktop environments."
    
    async def execute_computer_task(
        self,
        task: str,
        instance_id: str = None,
        instance_type: InstanceType = None,
        timeout_hours: int = None,
        on_step: Callable = None,
        schema: Any = None
    ) -> Dict[str, Any]:
        """Execute a computer use task with automatic instance management"""
        
        # Get or create instance
        if instance_id:
            instance = await self.get_instance(instance_id)
            if not instance:
                return {"error": f"Instance {instance_id} not found or expired"}
        else:
            instance = await self.create_instance(
                instance_type=instance_type,
                timeout_hours=timeout_hours
            )
            if not instance:
                return {"error": "Failed to create instance"}
        
        # Get model
        model = self.get_available_model()
        if not model:
            return {"error": "No available models"}
        
        # Get system prompt
        system_prompt = self.get_system_prompt(instance.instance_type)
        
        try:
            # Execute task using Scrapybara Act SDK
            if hasattr(model, 'generate_response'):  # Custom adapter (like Gemini)
                # Handle custom adapters
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task}
                ]
                response = await model.generate_response(messages, tools=instance.tools)
                
                return {
                    "success": True,
                    "text": response.get('text', ''),
                    "messages": messages + [{"role": "assistant", "content": response.get('text', '')}],
                    "usage": response.get('usage', {}),
                    "instance_id": instance.instance_id
                }
            
            else:  # Standard Scrapybara models
                response = self.client.act(
                    model=model,
                    tools=instance.tools,
                    system=system_prompt,
                    prompt=task,
                    on_step=on_step,
                    schema=schema
                )
                
                return {
                    "success": True,
                    "text": response.text,
                    "messages": response.messages,
                    "steps": response.steps,
                    "usage": response.usage,
                    "output": getattr(response, 'output', None),
                    "instance_id": instance.instance_id
                }
                
        except Exception as e:
            self.logger.error(f"Computer task execution failed: {e}")
            return {"error": str(e), "instance_id": instance.instance_id}
    
    async def save_auth_state(self, instance_id: str, name: str = "default") -> Optional[str]:
        """Save browser authentication state"""
        instance = await self.get_instance(instance_id)
        if not instance:
            return None
        
        try:
            auth_state_id = instance.instance.browser.save_auth(name=name).auth_state_id
            instance.auth_states[name] = auth_state_id
            self.logger.info(f"Saved auth state '{name}' for instance {instance_id}")
            return auth_state_id
        except Exception as e:
            self.logger.error(f"Failed to save auth state: {e}")
            return None
    
    async def load_auth_state(self, instance_id: str, auth_state_id: str) -> bool:
        """Load browser authentication state"""
        instance = await self.get_instance(instance_id)
        if not instance:
            return False
        
        try:
            instance.instance.browser.authenticate(auth_state_id=auth_state_id)
            self.logger.info(f"Loaded auth state for instance {instance_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load auth state: {e}")
            return False
    
    def get_instance_status(self, instance_id: str = None) -> Dict[str, Any]:
        """Get status of instances"""
        if instance_id:
            instance = self.instances.get(instance_id)
            if not instance:
                return {"error": "Instance not found"}
            
            return {
                "instance_id": instance.instance_id,
                "type": instance.instance_type.value,
                "age_hours": instance.get_age_hours(),
                "timeout_hours": instance.timeout_hours,
                "is_active": instance.is_active,
                "is_expired": instance.is_expired(),
                "auth_states": list(instance.auth_states.keys())
            }
        else:
            return {
                "total_instances": len(self.instances),
                "max_instances": self.config.max_instances,
                "instances": {
                    instance_id: {
                        "type": instance.instance_type.value,
                        "age_hours": instance.get_age_hours(),
                        "is_active": instance.is_active,
                        "is_expired": instance.is_expired()
                    }
                    for instance_id, instance in self.instances.items()
                }
            }


class ScrapybaraOrchestrator:
    """Orchestrates Scrapybara computer use agents with Mama Bear system"""
    
    def __init__(self, config: ScrapybaraConfig = None):
        self.config = config or ScrapybaraConfig()
        self.manager = ScrapybaraManager(self.config)
        self.logger = logging.getLogger(__name__)
        
        # Integration with Mama Bear system
        self.active_workflows: Dict[str, Dict] = {}
        self.task_history: List[Dict] = []
    
    async def execute_autonomous_workflow(
        self,
        workflow_description: str,
        context: Dict[str, Any] = None,
        instance_preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute autonomous workflow with Scout.new-level capabilities"""
        
        workflow_id = f"workflow_{int(time.time())}"
        self.logger.info(f"Starting autonomous workflow: {workflow_id}")
        
        # Parse workflow requirements
        instance_type = self._determine_instance_type(workflow_description, instance_preferences)
        timeout_hours = instance_preferences.get('timeout_hours') if instance_preferences else None
        
        # Create workflow context
        workflow_context = {
            "workflow_id": workflow_id,
            "description": workflow_description,
            "context": context or {},
            "started_at": time.time(),
            "status": "running",
            "steps": []
        }
        
        self.active_workflows[workflow_id] = workflow_context
        
        try:
            # Execute computer task
            def on_step(step):
                workflow_context["steps"].append({
                    "timestamp": time.time(),
                    "text": step.text if hasattr(step, 'text') else str(step),
                    "type": "step"
                })
                self.logger.info(f"Workflow {workflow_id} step: {step.text if hasattr(step, 'text') else str(step)}")
            
            result = await self.manager.execute_computer_task(
                task=workflow_description,
                instance_type=instance_type,
                timeout_hours=timeout_hours,
                on_step=on_step
            )
            
            workflow_context["status"] = "completed" if result.get("success") else "failed"
            workflow_context["result"] = result
            workflow_context["completed_at"] = time.time()
            
            # Store in task history
            self.task_history.append(workflow_context.copy())
            
            # Clean up active workflow
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
            
            return {
                "workflow_id": workflow_id,
                "success": result.get("success", False),
                "result": result,
                "duration": workflow_context["completed_at"] - workflow_context["started_at"]
            }
            
        except Exception as e:
            workflow_context["status"] = "error"
            workflow_context["error"] = str(e)
            workflow_context["completed_at"] = time.time()
            
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            
            return {
                "workflow_id": workflow_id,
                "success": False,
                "error": str(e)
            }
    
    def _determine_instance_type(self, description: str, preferences: Dict = None) -> InstanceType:
        """Determine optimal instance type based on task description"""
        description_lower = description.lower()
        
        # Check preferences first
        if preferences and 'instance_type' in preferences:
            try:
                return InstanceType(preferences['instance_type'])
            except ValueError:
                pass
        
        # Analyze description for instance type hints
        if any(term in description_lower for term in ['browser', 'web', 'website', 'url', 'html']):
            return InstanceType.BROWSER
        elif any(term in description_lower for term in ['windows', 'exe', 'registry', 'powershell']):
            return InstanceType.WINDOWS
        else:
            return InstanceType.UBUNTU  # Default
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get status of active or completed workflow"""
        # Check active workflows
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        
        # Check task history
        for task in self.task_history:
            if task.get("workflow_id") == workflow_id:
                return task
        
        return None
    
    def get_system_capabilities(self) -> Dict[str, Any]:
        """Get comprehensive system capabilities report"""
        return {
            "scrapybara_available": SCRAPYBARA_AVAILABLE,
            "gemini_available": GEMINI_AVAILABLE,
            "model_providers": {
                provider.value: config.enabled 
                for provider, config in self.manager.model_configs.items()
            },
            "instance_types": [t.value for t in InstanceType],
            "max_instances": self.config.max_instances,
            "current_instances": len(self.manager.instances),
            "active_workflows": len(self.active_workflows),
            "total_completed_workflows": len(self.task_history)
        }


# Factory function for easy integration
def create_scrapybara_orchestrator(
    api_key: str = None,
    gemini_api_key: str = None,
    anthropic_api_key: str = None,
    openai_api_key: str = None,
    max_instances: int = 5
) -> ScrapybaraOrchestrator:
    """Create a Scrapybara orchestrator with specified configuration"""
    
    # Set environment variables if provided
    if gemini_api_key:
        os.environ['GOOGLE_API_KEY'] = gemini_api_key
    if anthropic_api_key:
        os.environ['ANTHROPIC_API_KEY'] = anthropic_api_key
    if openai_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key
    
    config = ScrapybaraConfig(
        api_key=api_key,
        max_instances=max_instances
    )
    
    return ScrapybaraOrchestrator(config)


# Example usage and testing
async def main():
    """Example usage of Scrapybara integration"""
    orchestrator = create_scrapybara_orchestrator()
    
    # Check system capabilities
    capabilities = orchestrator.get_system_capabilities()
    print("System Capabilities:", json.dumps(capabilities, indent=2))
    
    # Execute a simple task
    if capabilities["scrapybara_available"]:
        result = await orchestrator.execute_autonomous_workflow(
            "Take a screenshot and describe what you see on the desktop"
        )
        print("Workflow Result:", json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
