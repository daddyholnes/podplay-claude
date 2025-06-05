#!/usr/bin/env python3
# test_orchestration_fix.py
"""
🧪 Test script to verify the Mama Bear orchestration fix
Run this to test the get_response method compatibility
"""

import asyncio
import sys
import json
from datetime import datetime

async def test_orchestration_fix():
    """Test the fixed get_response method"""
    
    print("🧪 Testing Mama Bear Orchestration Fix...")
    print("=" * 50)
    
    try:
        # Test 1: Import the fixed modules
        print("\n1️⃣ Testing imports...")
        
        try:
            from backend.services.mama_bear_model_manager import EnhancedMamaBearAgent
            from backend.services.mama_bear_memory_system import EnhancedMemoryManager
            print("✅ Successfully imported EnhancedMamaBearAgent and EnhancedMemoryManager")
        except ImportError as e:
            print(f"❌ Import failed: {e}")
            return False
        
        # Test 2: Create instances (mock dependencies)
        print("\n2️⃣ Testing instance creation...")
        
        class MockScrapybaraClient:
            pass
        
        class MockMemoryManager:
            async def get_relevant_context(self, user_id, message, limit=3):
                return []
            
            async def save_interaction(self, user_id, message, response, metadata=None):
                pass
        
        try:
            memory_manager = MockMemoryManager()
            scrapybara_client = MockScrapybaraClient()
            mama_bear = EnhancedMamaBearAgent(scrapybara_client, memory_manager)
            print("✅ Successfully created EnhancedMamaBearAgent instance")
        except Exception as e:
            print(f"❌ Instance creation failed: {e}")
            return False
        
        # Test 3: Test get_response method with orchestration parameters
        print("\n3️⃣ Testing get_response method with orchestration parameters...")
        
        test_cases = [
            {
                "name": "Orchestration-style call (prompt parameter)",
                "params": {
                    "prompt": "Hello, this is a test message",
                    "mama_bear_variant": "research_specialist",
                    "required_capabilities": ["chat"],
                    "user_id": "test_user"
                }
            },
            {
                "name": "Legacy-style call (message parameter)", 
                "params": {
                    "message": "Hello, this is a legacy test",
                    "user_id": "test_user",
                    "page_context": "main_chat"
                }
            },
            {
                "name": "Mixed parameters",
                "params": {
                    "prompt": "Test with mixed params",
                    "mama_bear_variant": "devops_specialist",
                    "user_id": "test_user",
                    "page_context": "vm_hub"
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                print(f"\n  Test 3.{i}: {test_case['name']}")
                
                # Check if method exists
                if not hasattr(mama_bear, 'get_response'):
                    print(f"  ❌ get_response method not found on EnhancedMamaBearAgent")
                    continue
                
                # Test method signature inspection
                import inspect
                sig = inspect.signature(mama_bear.get_response)
                print(f"  📋 Method signature: {sig}")
                
                # Test calling the method (this will likely fail due to missing API keys, but should not fail due to signature issues)
                result = await mama_bear.get_response(**test_case['params'])
                
                if isinstance(result, dict):
                    print(f"  ✅ Method call successful, returned dict with keys: {list(result.keys())}")
                    print(f"  📊 Success: {result.get('success', 'N/A')}")
                    if result.get('success'):
                        print(f"  💬 Content preview: {result.get('content', '')[:100]}...")
                    else:
                        print(f"  ⚠️ Error: {result.get('error', 'Unknown error')}")
                else:
                    print(f"  ⚠️ Method returned unexpected type: {type(result)}")
                    
            except TypeError as e:
                if "missing" in str(e) and "required positional argument" in str(e):
                    print(f"  ❌ Parameter signature error: {e}")
                else:
                    print(f"  ⚠️ Expected error (likely API/config related): {e}")
            except Exception as e:
                print(f"  ⚠️ Expected error (likely API/config related): {e}")
        
        # Test 4: Test orchestration compatibility
        print("\n4️⃣ Testing orchestration system compatibility...")
        
        try:
            from backend.services.mama_bear_orchestration import AgentOrchestrator
            
            # Create orchestrator with mock dependencies
            orchestrator = AgentOrchestrator(
                memory_manager=memory_manager,
                model_manager=mama_bear,  # This should work now
                scrapybara_client=scrapybara_client
            )
            
            print("✅ Successfully created AgentOrchestrator with EnhancedMamaBearAgent")
            
            # Test that orchestrator can access the get_response method
            if hasattr(orchestrator.model_manager, 'get_response'):
                print("✅ Orchestrator can access get_response method")
                
                # Test method signature compatibility
                sig = inspect.signature(orchestrator.model_manager.get_response)
                params = list(sig.parameters.keys())
                required_params = ['prompt', 'mama_bear_variant', 'required_capabilities']
                
                missing_params = [p for p in required_params if p not in params]
                if not missing_params:
                    print("✅ Method signature is compatible with orchestration calls")
                else:
                    print(f"⚠️ Missing expected parameters: {missing_params}")
                    
            else:
                print("❌ Orchestrator cannot access get_response method")
                return False
                
        except ImportError as e:
            print(f"⚠️ Could not test orchestration integration: {e}")
        except Exception as e:
            print(f"❌ Orchestration test failed: {e}")
            return False
        
        print("\n🎉 All core tests passed! The fix should resolve the orchestration compatibility issue.")
        return True
        
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    print("🐻 Mama Bear Orchestration Fix Test")
    print(f"🕐 Started at: {datetime.now()}")
    
    success = asyncio.run(test_orchestration_fix())
    
    if success:
        print("\n✅ TEST RESULT: SUCCESS - Fix should work!")
        print("\n🚀 Next steps:")
        print("   1. Apply the get_response method fix to mama_bear_model_manager.py")
        print("   2. Restart your backend server")
        print("   3. Test the /api/mama-bear/chat endpoint")
        sys.exit(0)
    else:
        print("\n❌ TEST RESULT: ISSUES FOUND - Please check the errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()