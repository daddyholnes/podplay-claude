# .env file for Mama Bear Intelligent Model Management
# Copy this to your backend directory as .env

# =================================
# MAMA BEAR MODEL CONFIGURATION
# =================================

# Primary Gemini API Key (your current key)
GEMINI_API_KEY=AIzaSyCNUGhuoAvvaSJ2ypsqzgtUCaLSusRZs5Y

# Backup Gemini API Key (your second billing account - REPLACE WITH ACTUAL KEY)
GEMINI_API_KEY_BACKUP=YOUR_SECOND_GEMINI_API_KEY_HERE

# Model Management Settings
MAMA_BEAR_DEFAULT_TEMPERATURE=0.7
MAMA_BEAR_MAX_TOKENS=8192
MAMA_BEAR_QUOTA_SAFETY_MARGIN=0.1
MAMA_BEAR_MAX_FALLBACK_ATTEMPTS=6

# Health Monitoring
MAMA_BEAR_HEALTH_CHECK_INTERVAL=300
MAMA_BEAR_ERROR_THRESHOLD=3
MAMA_BEAR_RECOVERY_TIMEOUT=1800

# Performance Optimization
MAMA_BEAR_ENABLE_CACHING=true
MAMA_BEAR_CACHE_TTL=3600
MAMA_BEAR_LOG_MODEL_USAGE=true

# =================================
# EXISTING CONFIGURATION
# =================================

# Scrapybara Configuration
SCRAPYBARA_API_KEY=scrapy-abaf2356-01d5-4d65-88d3-eebcd177b214

# Other AI APIs (existing)
ANTHROPIC_API_KEY=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
OPENAI_API_KEY=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

# Mem0.ai Configuration
MEM0_API_KEY=m0-tBwWs1ygkxcbEiVvX6iXdwiJ42epw8a3wyoEUlpg
MEM0_USER_ID=nathan_sanctuary
MEM0_MEMORY_ENABLED=True
MEM0_RAG_ENABLED=True

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/home/woody/Podplay-Sanctuary/podplay-build-beta-10490f7d079e.json
GOOGLE_CLOUD_PROJECT=podplay-build-beta

# Application Settings
FLASK_ENV=development
LOG_LEVEL=INFO
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000

# =================================
# USAGE EXAMPLE SCRIPTS
# =================================

# Test script to verify model management is working
cat > test_mama_bear_models.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for Mama Bear Intelligent Model Management
Run this to verify your setup is working correctly
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.mama_bear_model_manager import MamaBearModelManager, MamaBearResponse
from services.mama_bear_specialized_variants import *
from utils.mama_bear_monitoring import MamaBearMonitoring

async def test_model_management():
    """Test the complete Mama Bear model management system"""
    print("🐻 Testing Mama Bear Intelligent Model Management System")
    print("=" * 60)
    
    # Initialize the model manager
    print("\n1. Initializing Model Manager...")
    model_manager = MamaBearModelManager()
    
    # Test model status
    print("\n2. Checking Model Status...")
    status = model_manager.get_model_status()
    for model_id, model_status in status.items():
        health_icon = "✅" if model_status['is_healthy'] else "❌"
        print(f"   {health_icon} {model_id}: {model_status['quota_status']} (Account: {model_status['billing_account']})")
    
    # Test model warm-up
    print("\n3. Warming up models...")
    try:
        await model_manager.warm_up_models()
        print("   ✅ Model warm-up completed")
    except Exception as e:
        print(f"   ⚠️  Warm-up had issues: {e}")
    
    # Test different types of requests
    test_messages = [
        {
            'messages': [{'role': 'user', 'content': 'Hello Mama Bear! How are you today?'}],
            'context': {'variant': 'main_chat', 'simple': True},
            'description': 'Simple greeting (should use Flash model)'
        },
        {
            'messages': [{'role': 'user', 'content': 'Can you analyze the pros and cons of different machine learning approaches for natural language processing, considering computational efficiency, accuracy, and implementation complexity?'}],
            'context': {'variant': 'main_chat', 'requires_reasoning': True},
            'description': 'Complex analysis (should use Pro model)'
        },
        {
            'messages': [{'role': 'user', 'content': 'Help me set up a new development environment with Python, Node.js, and Docker.'}],
            'context': {'variant': 'vm_hub'},
            'description': 'DevOps task (should prefer fast models)'
        }
    ]
    
    print("\n4. Testing Different Request Types...")
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n   Test {i}: {test_case['description']}")
        try:
            response = await model_manager.generate_response(
                messages=test_case['messages'],
                mama_bear_context=test_case['context']
            )
            
            print(f"   ✅ Success!")
            print(f"      Model Used: {response.model_used}")
            print(f"      Billing Account: {response.billing_account}")
            print(f"      Processing Time: {response.processing_time:.2f}s")
            print(f"      Fallback Count: {response.fallback_count}")
            if response.quota_warnings:
                print(f"      Quota Warnings: {len(response.quota_warnings)}")
            print(f"      Response Preview: {response.content[:100]}...")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Test quota simulation
    print("\n5. Testing Quota Management...")
    print("   (Simulating quota exhaustion on primary models)")
    
    # Temporarily exhaust primary model quotas
    for model_id, config in model_manager.models.items():
        if 'primary' in model_id:
            config.current_requests_day = config.requests_per_day
    
    try:
        response = await model_manager.generate_response(
            messages=[{'role': 'user', 'content': 'This should trigger fallback to backup models.'}],
            mama_bear_context={'variant': 'main_chat'}
        )
        print(f"   ✅ Fallback successful! Used: {response.model_used} (Account: {response.billing_account})")
        print(f"      Fallback attempts: {response.fallback_count}")
    except Exception as e:
        print(f"   ❌ Fallback failed: {e}")
    
    # Reset quotas
    for model_id, config in model_manager.models.items():
        config.current_requests_day = 0
    
    print("\n6. Final Status Check...")
    final_status = model_manager.get_model_status()
    healthy_models = sum(1 for status in final_status.values() if status['is_healthy'])
    total_models = len(final_status)
    
    print(f"   Healthy Models: {healthy_models}/{total_models}")
    print(f"   System Status: {'✅ READY' if healthy_models > 0 else '❌ DEGRADED'}")
    
    print("\n🐻 Mama Bear Model Management Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_model_management())
EOF

# Integration example for your Flask app
cat > integrate_mama_bear.py << 'EOF'
#!/usr/bin/env python3
"""
Integration example showing how to add Mama Bear Model Management 
to your existing Flask application
"""

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import asyncio
import logging

# Import your existing services
from services.mama_bear_model_manager import EnhancedMamaBearAgent
from services.memory_manager import MemoryManager
from utils.mama_bear_monitoring import MamaBearMonitoring
from api.mama_bear_endpoints import mama_bear_bp
import scrapybara

def create_enhanced_app():
    """Create Flask app with enhanced Mama Bear intelligence"""
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Initialize extensions
    socketio = SocketIO(app, cors_allowed_origins="*")
    CORS(app)
    
    # Initialize core services
    scrapybara_client = scrapybara.Scrapybara()
    memory_manager = MemoryManager()
    
    # Initialize enhanced Mama Bear with intelligent model management
    mama_bear_agent = EnhancedMamaBearAgent(scrapybara_client, memory_manager)
    
    # Initialize monitoring
    mama_bear_monitoring = MamaBearMonitoring(mama_bear_agent.model_manager)
    
    # Store in app context
    app.mama_bear_agent = mama_bear_agent
    app.mama_bear_monitoring = mama_bear_monitoring
    
    # Register blueprints
    app.register_blueprint(mama_bear_bp)
    
    # WebSocket handlers
    @socketio.on('mama_bear_message')
    async def handle_mama_bear_message(data):
        """Handle real-time Mama Bear messages with intelligent routing"""
        try:
            response = await mama_bear_agent.process_message(
                message=data['message'],
                page_context=data.get('page_context', 'main_chat'),
                user_id=data.get('user_id', 'default_user'),
                **data.get('options', {})
            )
            
            # Record metrics
            mama_bear_monitoring.record_request(response.get('metadata', {}))
            
            # Emit response
            emit('mama_bear_response', {
                'success': True,
                'content': response['content'],
                'metadata': response.get('metadata', {}),
                'mama_bear_variant': response['metadata'].get('mama_bear_variant', 'Unknown')
            })
            
        except Exception as e:
            emit('mama_bear_response', {
                'success': False,
                'error': str(e),
                'content': "I'm having trouble right now, but I'm working on it! 🐻💙"
            })
    
    @socketio.on('get_mama_bear_status')
    async def handle_status_request():
        """Get real-time system status"""
        try:
            status = await mama_bear_agent.get_system_status()
            emit('mama_bear_status', {
                'success': True,
                'status': status
            })
        except Exception as e:
            emit('mama_bear_status', {
                'success': False,
                'error': str(e)
            })
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            status = mama_bear_agent.model_manager.get_model_status()
            healthy_models = sum(1 for s in status.values() if s['is_healthy'])
            
            return jsonify({
                'status': 'healthy' if healthy_models > 0 else 'degraded',
                'healthy_models': healthy_models,
                'total_models': len(status),
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500
    
    # Startup tasks
    @app.before_first_request
    async def startup_tasks():
        """Run startup tasks"""
        try:
            # Warm up models
            await mama_bear_agent.model_manager.warm_up_models()
            app.logger.info("🐻 Mama Bear Model Management initialized successfully!")
            
        except Exception as e:
            app.logger.error(f"🐻 ❌ Startup error: {e}")
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_enhanced_app()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🐻 Starting Podplay Sanctuary with Enhanced Mama Bear Intelligence...")
    print("🚀 Model Management: ENABLED")
    print("📊 Monitoring: ENABLED")
    print("🔄 Quota Management: ENABLED")
    print("🛡️  Failover Protection: ENABLED")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
EOF

# Make scripts executable
chmod +x test_mama_bear_models.py
chmod +x integrate_mama_bear.py

echo "🐻 Mama Bear Intelligent Model Management Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Add your second Gemini API key to GEMINI_API_KEY_BACKUP in .env"
echo "2. Run: python test_mama_bear_models.py"
echo "3. Integrate with: python integrate_mama_bear.py"
echo ""
echo "Features Enabled:"
echo "✅ Intelligent model selection based on task complexity"
echo "✅ Automatic quota management and fallover"
echo "✅ Multi-billing account support"
echo "✅ Real-time health monitoring"
echo "✅ Performance optimization"
echo "✅ Comprehensive analytics and reporting"
echo ""
echo "Your Mama Bear is now super intelligent! 🚀✨"