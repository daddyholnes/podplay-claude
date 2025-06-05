# backend/services/mama_bear_orchestration.py
# 🔧 FIXES: Update all get_response calls to use consistent parameters

# Fix #1: In _analyze_request method around line 140
async def _analyze_request(self, message: str, page_context: str) -> Dict[str, Any]:
    """Analyze user request to determine optimal agent strategy"""
    
    # Use the research specialist to analyze the request
    analysis_prompt = f"""
    Analyze this user request and determine the optimal agent strategy:
    
    Request: "{message}"
    Context: {page_context}
    
    Classify as:
    1. simple_response - One agent can handle this (specify which agent)
    2. collaborative - Multiple agents need to work together (specify agents and roles)
    3. plan_and_execute - Needs planning phase then execution (specify planning steps)
    
    Consider:
    - Complexity of the request
    - Required capabilities (coding, research, deployment, etc.)
    - Time sensitivity
    - Resource requirements
    
    Return a JSON strategy object.
    """
    
    # 🔧 FIXED: Updated parameter names to match get_response signature
    result = await self.model_manager.get_response(
        prompt=analysis_prompt,  # ✅ Using 'prompt' parameter
        mama_bear_variant='research_specialist',
        required_capabilities=['chat', 'code'],
        user_id='system',
        page_context='orchestration_analysis'
    )
    
    if result.get('success', False):
        try:
            # Parse the strategy from the response
            strategy = self._extract_strategy_from_response(result.get('response', ''))
            return strategy
        except Exception as e:
            logger.warning(f"Failed to parse strategy response: {e}")
            # Fallback to simple routing based on page context
            return self._fallback_strategy(page_context)
    else:
        logger.warning(f"Strategy analysis failed: {result.get('error', 'Unknown error')}")
        return self._fallback_strategy(page_context)

# Fix #2: In MamaBearAgent.handle_request method around line 280
class MamaBearAgent:
    """Base class for all Mama Bear agents"""
    
    async def handle_request(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle a direct user request"""
        
        self.state = AgentState.THINKING
        self.last_activity = datetime.now()
        
        try:
            # Get context
            context = await self.orchestrator.context_awareness.get_agent_context(self.id)
            
            # Get system prompt from variant
            system_prompt = self.variant.get_system_prompt() if self.variant else "You are a helpful Mama Bear assistant."
            
            # Build full prompt
            full_prompt = f"""
            {system_prompt}
            
            Current context:
            - User: {user_id}
            - Previous conversation: {context.conversation_history[-3:] if context.conversation_history else 'None'}
            - Available tools: {context.available_tools}
            - Project context: {context.project_context}
            
            User request: {message}
            
            Please respond as this Mama Bear specialist.
            """
            
            # 🔧 FIXED: Updated to use get_response with correct parameters
            result = await self.orchestrator.model_manager.get_response(
                prompt=full_prompt,
                mama_bear_variant=self.id.split('_')[0] if '_' in self.id else self.id,
                required_capabilities=['chat'],
                user_id=user_id,
                page_context='agent_direct'
            )
            
            self.state = AgentState.IDLE
            
            if result.get('success', False):
                # Save interaction to memory
                if hasattr(self.orchestrator.memory, 'save_interaction'):
                    try:
                        await self.orchestrator.memory.save_interaction(
                            user_id=user_id,
                            message=message,
                            response=result.get('response', ''),
                            metadata={
                                'agent_id': self.id,
                                'model_used': result.get('model_used', 'unknown')
                            }
                        )
                    except Exception as e:
                        logger.warning(f"Failed to save interaction: {e}")
                
                return {
                    'success': True,
                    'content': result.get('response', result.get('content', '')),
                    'agent_id': self.id,
                    'model_used': result.get('model_used', 'unknown'),
                    'metadata': result.get('metadata', {})
                }
            else:
                return {
                    'success': False,
                    'content': "I'm having trouble accessing my models right now. Let me try a different approach!",
                    'error': result.get('error'),
                    'agent_id': self.id
                }
                
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Agent {self.id} error: {e}")
            return {
                'success': False,
                'content': "I encountered an error, but I'm working on fixing it! 🐻",
                'error': str(e),
                'agent_id': self.id
            }

# Fix #3: In LeadDeveloperAgent.create_plan method
class LeadDeveloperAgent(MamaBearAgent):
    """Special agent that coordinates other agents and handles complex planning"""
    
    async def create_plan(self, request: str, user_id: str) -> Dict[str, Any]:
        """Create a detailed plan for complex requests"""
        
        planning_prompt = f"""
        As the Lead Developer Mama Bear, create a detailed plan for this request:
        
        Request: "{request}"
        User: {user_id}
        
        Break this down into:
        1. Requirements analysis
        2. Task decomposition
        3. Agent assignments
        4. Dependencies
        5. Estimated timeline
        6. Resource requirements
        
        Format as a structured plan that can be executed step by step.
        """
        
        # 🔧 FIXED: Updated to use get_response with correct parameters
        result = await self.orchestrator.model_manager.get_response(
            prompt=planning_prompt,
            mama_bear_variant='lead_developer',
            required_capabilities=['chat', 'code', 'planning'],
            user_id=user_id,
            page_context='planning'
        )
        
        if result.get('success', False):
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': result.get('response', result.get('content', '')),
                'status': 'pending_approval',
                'created_by': self.id,
                'user_id': user_id
            }
        else:
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': "I'll help you with this step by step!",
                'status': 'simple',
                'created_by': self.id,
                'user_id': user_id
            }

# Fix #4: In _synthesize_collaboration_results method
async def _synthesize_collaboration_results(self, collaboration_id: str, results: List[Dict], original_message: str) -> Dict[str, Any]:
    """Combine results from multiple agents into a coherent response"""
    
    synthesis_prompt = f"""
    Combine these results from different Mama Bear specialists into a coherent response:
    
    Original request: "{original_message}"
    
    Results:
    {json.dumps(results, indent=2)}
    
    Create a unified response that:
    1. Addresses the original request completely
    2. Integrates insights from all specialists
    3. Provides clear next steps if applicable
    4. Maintains Mama Bear's caring, supportive tone
    
    Return a natural, conversational response.
    """
    
    # 🔧 FIXED: Updated to use get_response with correct parameters
    result = await self.model_manager.get_response(
        prompt=synthesis_prompt,
        mama_bear_variant='research_specialist',  # Use research specialist for synthesis
        required_capabilities=['chat', 'synthesis'],
        user_id='system',
        page_context='collaboration_synthesis'
    )
    
    return {
        'type': 'collaborative_response',
        'content': result.get('response', result.get('content', '')) if result.get('success') else "I've gathered information from my specialists and I'm ready to help!",
        'collaboration_id': collaboration_id,
        'participating_agents': [r.get('agent_id') for r in results if isinstance(r, dict)],
        'model_used': result.get('model_used'),
        'metadata': {
            'collaboration_results': results,
            'synthesis_successful': result.get('success', False)
        }
    }