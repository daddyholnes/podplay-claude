"""
Memory Manager Service
Handles persistent memory operations using Mem0 for the Podplay Sanctuary
Enhanced with Scout.new-level session management capabilities
"""

import asyncio
import json
import logging
import re  # Import the re module for regular expressions
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from mem0 import Memory
import uuid

# Import enhanced session management
try:
    from .enhanced_session_manager import (
        EnhancedSessionManager, SessionType, SessionState, 
        create_enhanced_session_manager
    )
    ENHANCED_SESSIONS_AVAILABLE = True
except ImportError:
    ENHANCED_SESSIONS_AVAILABLE = False
    
logger = logging.getLogger(__name__) # Move logger initialization to top

class MemoryManager:
    """Manages persistent memory for the Podplay Sanctuary using Mem0"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory = Memory()
        self.user_sessions = {}  # Track active user sessions
        self.memory_categories = {
            'conversation': 'chat_history',
            'preferences': 'user_preferences', 
            'project': 'project_context',
            'sanctuary': 'sanctuary_state',
            'mama_bear': 'agent_context',
            'scrapybara': 'vm_context',
            'themes': 'theme_preferences'
        }
        
        logger.info("Memory Manager initialized with Mem0")
    
    async def store_conversation(self, user_id: str, conversation_data: Dict[str, Any]) -> str:
        """Store conversation data with metadata"""
        try:
            memory_id = str(uuid.uuid4())
            
            # Prepare conversation for storage
            messages = []
            if 'user_message' in conversation_data:
                messages.append({
                    "role": "user", 
                    "content": conversation_data['user_message']
                })
            if 'assistant_response' in conversation_data:
                messages.append({
                    "role": "assistant", 
                    "content": conversation_data['assistant_response']
                })
            
            # Store with rich metadata
            metadata = {
                "memory_id": memory_id,
                "category": "conversation",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "variant": conversation_data.get('variant', 'unknown'),
                "model_used": conversation_data.get('model_used', 'unknown'),
                "session_id": self._get_or_create_session(user_id),
                "sanctuary_theme": conversation_data.get('theme', 'sky'),
                "interaction_type": conversation_data.get('type', 'chat')
            }
            
            # Add context if provided
            if 'context' in conversation_data:
                metadata['context'] = json.dumps(conversation_data['context'])
            
            self.memory.add(
                messages=messages,
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"Stored conversation memory {memory_id} for user {user_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing conversation: {str(e)}")
            raise
    
    async def store_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> str:
        """Store user preferences and settings"""
        try:
            memory_id = str(uuid.uuid4())
            
            # Create a descriptive message about preferences
            pref_description = f"User preferences updated: {json.dumps(preferences, indent=2)}"
            
            metadata = {
                "memory_id": memory_id,
                "category": "preferences",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "preference_type": "user_settings"
            }
            
            self.memory.add(
                messages=[{"role": "system", "content": pref_description}],
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"Stored user preferences {memory_id} for user {user_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing user preferences: {str(e)}")
            raise
    
    async def store_project_context(self, user_id: str, project_data: Dict[str, Any]) -> str:
        """Store project-related context and state"""
        try:
            memory_id = str(uuid.uuid4())
            
            project_description = f"Project context: {project_data.get('name', 'Unnamed Project')}"
            if 'description' in project_data:
                project_description += f" - {project_data['description']}"
            
            metadata = {
                "memory_id": memory_id,
                "category": "project",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "project_name": project_data.get('name', 'unknown'),
                "project_type": project_data.get('type', 'general'),
                "tech_stack": json.dumps(project_data.get('tech_stack', [])),
                "phase": project_data.get('phase', 'planning')
            }
            
            self.memory.add(
                messages=[{"role": "system", "content": project_description}],
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"Stored project context {memory_id} for user {user_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing project context: {str(e)}")
            raise
    
    async def store_sanctuary_state(self, user_id: str, sanctuary_data: Dict[str, Any]) -> str:
        """Store sanctuary-specific state (themes, layouts, etc.)"""
        try:
            memory_id = str(uuid.uuid4())
            
            state_description = f"Sanctuary state: Theme={sanctuary_data.get('theme', 'sky')}, Layout={sanctuary_data.get('layout', 'default')}"
            
            metadata = {
                "memory_id": memory_id,
                "category": "sanctuary",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "active_theme": sanctuary_data.get('theme', 'sky'),
                "layout_preference": sanctuary_data.get('layout', 'default'),
                "sensory_settings": json.dumps(sanctuary_data.get('sensory_settings', {})),
                "active_page": sanctuary_data.get('active_page', 'main_chat')
            }
            
            self.memory.add(
                messages=[{"role": "system", "content": state_description}],
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"Stored sanctuary state {memory_id} for user {user_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing sanctuary state: {str(e)}")
            raise
    
    async def retrieve_memories(self, user_id: str, category: Optional[str] = None, 
                              limit: int = 10, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve memories with optional filtering"""
        try:
            search_query = f"user:{user_id}"
            
            if category and category in self.memory_categories:
                search_query += f" category:{category}"
            
            if query:
                search_query += f" {query}"
            
            memories = self.memory.search(search_query, limit=limit)
            
            # Process and enrich memories
            processed_memories = []
            for memory in memories:
                if not isinstance(memory, dict):
                    logger.warning(f"Unexpected memory format (not a dict): {memory}. Skipping.")
                    continue

                # Mem0 search results have 'text' and 'metadata' as top-level keys for memory content and associated metadata.
                # 'score' is also a top-level key.
                processed_memory = {
                    'content': memory.get('text', ''),
                    'metadata': memory.get('metadata', {}),
                    'score': memory.get('score', 0.0),
                    'timestamp': memory.get('metadata', {}).get('timestamp'),
                    'category': memory.get('metadata', {}).get('category', 'unknown')
                }
                processed_memories.append(processed_memory)
            
            logger.info(f"Retrieved {len(processed_memories)} memories for user {user_id}")
            return processed_memories
            
        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}")
            return []
    
    async def get_conversation_history(self, user_id: str, limit: int = 20, 
                                     variant: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get conversation history, optionally filtered by Mama Bear variant"""
        try:
            search_query = f"user:{user_id} category:conversation"
            if variant:
                search_query += f" variant:{variant}"
            
            memories = self.memory.search(search_query, limit=limit)
            
            # Process conversation memories
            conversations = []
            # Process conversation memories
            conversations = []
            for memory in memories:
                if not isinstance(memory, dict):
                    logger.warning(f"Unexpected memory format (not a dict) in conversation history: {memory}. Skipping.")
                    continue
                
                metadata = memory.get('metadata', {})
                conversation = {
                    'user_message': '',
                    'assistant_response': '',
                    'timestamp': metadata.get('timestamp'),
                    'variant': metadata.get('variant', 'unknown'),
                    'model_used': metadata.get('model_used', 'unknown'),
                    'theme': metadata.get('sanctuary_theme', 'sky')
                }
                
                # Extract messages from memory content (Mem0 stores messages as a list of dicts)
                messages_list = memory.get('messages', [])
                
                user_message = ""
                assistant_response = ""
                
                for msg in messages_list:
                    if not isinstance(msg, dict):
                        logger.warning(f"Unexpected message format (not a dict): {msg}. Skipping.")
                        continue
                    if msg.get("role") == "user":
                        user_message = msg.get("content", "")
                    elif msg.get("role") == "assistant":
                        assistant_response = msg.get("content", "")

                conversation['user_message'] = user_message
                conversation['assistant_response'] = assistant_response
                
                conversations.append(conversation)
            
            # Sort by timestamp (most recent first)
            conversations.sort(key=lambda x: x.get('timestamp') or '', reverse=True)

            return conversations
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get current user preferences"""
        try:
            memories = self.memory.search(f"user:{user_id} category:preferences", limit=5)
            
            # Merge preferences from most recent memories
            preferences = {
                'theme': 'sky',
                'layout': 'default',
                'mama_bear_variant': 'architect',
                'sensory_settings': {},
                'notification_preferences': {},
                'accessibility_settings': {}
            }
            
            for memory in memories:
                if not isinstance(memory, dict):
                    logger.warning(f"Unexpected memory format (not a dict) in user preferences: {memory}. Skipping.")
                    continue

                metadata = memory.get('metadata', {})
                
                # Mem0 stores messages in a list of dicts. Reconstruct full content from these messages.
                messages_list = memory.get('messages', [])
                memory_content = ""
                for msg_obj in messages_list:
                    if isinstance(msg_obj, dict) and 'content' in msg_obj:
                         memory_content += msg_obj['content'] + " "
                memory_content = memory_content.strip()

                # Try to extract preferences from memory content
                try:
                    if 'preferences updated:' in memory_content.lower():
                        # Use regex to find the JSON string. Mem0's add method wraps dicts in json.dumps
                        # so we need to account for escaped quotes if that's how it's stored in 'content'.
                        # Search for a pattern that looks like a JSON object.
                        json_match = re.search(r'(\{.*\})', memory_content)
                        if json_match:
                            pref_json_str = json_match.group(1)
                            # Attempt to load, if it fails, it might be double-escaped
                            try:
                                extracted_prefs = json.loads(pref_json_str)
                            except json.JSONDecodeError:
                                # If direct load fails, try loading it as a string that might be unescaped later
                                pref_json_str = pref_json_str.replace('\\"', '"') # Unescape quotes
                                extracted_prefs = json.loads(pref_json_str)

                            preferences.update(extracted_prefs)
                        else:
                            logger.warning(f"Could not find valid JSON in preferences memory content for {metadata.get('memory_id', 'unknown')}: {memory_content}")
                except json.JSONDecodeError as json_e:
                    logger.error(f"JSON decode error in get_user_preferences for memory {metadata.get('memory_id', 'unknown')}: {json_e}. Content: {memory_content[:150]}...")
                    continue
                except Exception as ex:
                    logger.error(f"Unexpected error in get_user_preferences for memory {metadata.get('memory_id', 'unknown')}: {ex}. Content: {memory_content[:150]}...")
                    continue
            
            return preferences
            
        except Exception as e:
            logger.error(f"Error getting user preferences: {str(e)}")
            return {}
    
    async def get_project_context(self, user_id: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Get project context and history"""
        try:
            search_query = f"user:{user_id} category:project"
            if project_name:
                search_query += f" project_name:{project_name}"
            
            memories = self.memory.search(search_query, limit=10)
            
            project_context = {
                'current_project': None,
                'recent_projects': [],
                'tech_stacks': [],
                'project_phases': []
            }
            
            for memory in memories:
                if not isinstance(memory, dict):
                    logger.warning(f"Unexpected memory format (not a dict) in project context: {memory}. Skipping.")
                    continue

                metadata = memory.get('metadata', {})
                project_info = {
                    'name': metadata.get('project_name', 'Unknown'),
                    'type': metadata.get('project_type', 'general'),
                    'phase': metadata.get('phase', 'planning'),
                    'timestamp': metadata.get('timestamp')
                }
                
                # Try to parse tech stack
                try:
                    tech_stack_raw = metadata.get('tech_stack', '[]')
                    # Mem0 stores JSON strings for dicts/lists within metadata, so we need to load them.
                    if isinstance(tech_stack_raw, str):
                        tech_stack = json.loads(tech_stack_raw)
                    else:
                        tech_stack = tech_stack_raw # Already the correct type
                    
                    project_info['tech_stack'] = tech_stack
                    if isinstance(tech_stack, list):
                        project_context['tech_stacks'].extend(tech_stack)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Could not decode tech_stack for memory {memory.get('id', 'unknown')}: {tech_stack_raw}. Error: {e}")
                    project_info['tech_stack'] = []
                except Exception as e:
                    logger.error(f"Unexpected error processing tech_stack for memory {memory.get('id', 'unknown')}: {e}")
                    project_info['tech_stack'] = []
                
                project_context['recent_projects'].append(project_info)
            
            # Sort recent projects by timestamp
            project_context['recent_projects'].sort(
                key=lambda x: x.get('timestamp') or '', reverse=True
            )

            # Set current project (most recent)
            if project_context['recent_projects']:
                project_context['current_project'] = project_context['recent_projects'][0]
            
            # Use a set to collect unique tech stacks from all projects, ensuring they are strings before adding.
            unique_tech_stacks = set()
            for proj in project_context['recent_projects']:
                for item in proj.get('tech_stack', []):
                    if isinstance(item, str):
                        unique_tech_stacks.add(item)
            project_context['tech_stacks'] = list(unique_tech_stacks)
            
            return project_context
            
        except Exception as e:
            logger.error(f"Error getting project context: {str(e)}")
            return {}
    
    async def search_memories(self, user_id: str, query: str, 
                            category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories with semantic similarity"""
        try:
            search_query = f"user:{user_id} {query}"
            if category:
                search_query += f" category:{category}"
            
            memories = self.memory.search(search_query, limit=limit)
            
            results = []
            for memory in memories:
                if not isinstance(memory, dict):
                    logger.warning(f"Unexpected memory format (not a dict) in search memories: {memory}. Skipping.")
                    continue

                result = {
                    'content': memory.get('text', ''),
                    'metadata': memory.get('metadata', {}),
                    'relevance_score': memory.get('score', 0.0),
                    'category': memory.get('metadata', {}).get('category', 'unknown'),
                    'timestamp': memory.get('metadata', {}).get('timestamp')
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching memories: {str(e)}")
            return []
    
    async def update_memory(self, memory_id: str, user_id: str, 
                          new_data: Dict[str, Any]) -> bool:
        """Update existing memory (limited support in Mem0)"""
        try:
            # Mem0 doesn't support direct updates, so we'll add new memory with update flag
            update_description = f"Memory update for {memory_id}: {json.dumps(new_data)}"
            
            metadata = {
                "category": "update",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "original_memory_id": memory_id,
                "update_type": "modification"
            }
            
            self.memory.add(
                messages=[{"role": "system", "content": update_description}],
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"Added update record for memory {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating memory: {str(e)}")
            return False
    
    async def delete_memories(self, user_id: str, memory_filters: Dict[str, Any]) -> int:
        """Delete memories matching filters (limited support in Mem0)"""
        try:
            # Mem0 has limited deletion support, so we'll mark as deleted
            delete_description = f"Memories marked for deletion: {json.dumps(memory_filters)}"
            
            metadata = {
                "category": "deletion",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "deletion_filters": json.dumps(memory_filters),
                "status": "marked_deleted"
            }
            
            self.memory.add(
                messages=[{"role": "system", "content": delete_description}],
                user_id=user_id,
                metadata=metadata
            )
            
            logger.info(f"Marked memories for deletion for user {user_id}")
            return 1  # Return count of deletion records created
            
        except Exception as e:
            logger.error(f"Error deleting memories: {str(e)}")
            return 0
    
    async def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about user's memory usage"""
        try:
            # Get all memories for user
            memories = self.memory.search(f"user:{user_id}", limit=1000)
            
            stats = {
                'total_memories': len(memories),
                'categories': {},
                'oldest_memory': None,
                'newest_memory': None,
                'conversation_count': 0,
                'project_count': 0
            }
            
            timestamps = []
            
            for memory in memories:
                if not isinstance(memory, dict):
                    logger.warning(f"Unexpected memory format (not a dict) in memory stats: {memory}. Skipping.")
                    continue
                
                # Mem0 returns the full memory object structure here, which should be a dict.
                metadata = memory.get('metadata', {})
                category = metadata.get('category', 'unknown')
                timestamp = metadata.get('timestamp')
                
                # Count by category
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
                
                # Track timestamps
                if timestamp:
                    timestamps.append(timestamp)
                
                # Special counts
                if category == 'conversation':
                    stats['conversation_count'] += 1
                elif category == 'project':
                    stats['project_count'] += 1
            
            # Set oldest and newest
            if timestamps:
                timestamps.sort()
                stats['oldest_memory'] = timestamps[0]
                stats['newest_memory'] = timestamps[-1]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {str(e)}")
            return {}
    
    def _get_or_create_session(self, user_id: str) -> str:
        """Get or create a session ID for the user (basic compatibility method)"""
        # This method is kept for backward compatibility
        # Enhanced session management should use EnhancedSessionManager
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'session_id': str(uuid.uuid4()),
                'created_at': datetime.now(),
                'last_activity': datetime.now()
            }
        
        # Update last activity
        self.user_sessions[user_id]['last_activity'] = datetime.now()
        
        return self.user_sessions[user_id]['session_id']
    
    async def save_context(self, key: str, value: Any, user_id: str = "system") -> str:
        """Save context data for orchestration system compatibility"""
        try:
            context_data = {
                'context_key': key,
                'context_value': value,
                'timestamp': datetime.now().isoformat(),
                'source': 'orchestration'
            }
            
            # Store as project context if it's system-level
            if user_id == "system":
                return await self.store_project_context(
                    user_id="system_orchestration",
                    project_data=context_data
                )
            else:
                # Store as user-specific sanctuary state
                return await self.store_sanctuary_state(user_id, context_data)
                
        except Exception as e:
            logger.error(f"Error saving context {key}: {e}")
            return ""
    
    async def cleanup_old_sessions(self, hours: int = 24):
        """Clean up old inactive sessions"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        expired_users = [
            user_id for user_id, session in self.user_sessions.items()
            if session['last_activity'] < cutoff_time
        ]
        
        for user_id in expired_users:
            del self.user_sessions[user_id]
        
        logger.info(f"Cleaned up {len(expired_users)} expired sessions")
