#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Create taskmaster storage directory
const taskmasterDir = path.join(__dirname, '.taskmaster');
if (!fs.existsSync(taskmasterDir)) {
  fs.mkdirSync(taskmasterDir, { recursive: true });
  console.log('✅ Created .taskmaster directory');
}

// Create current project tasks based on our phase
const tasksFile = path.join(taskmasterDir, 'tasks.json');
const currentTasks = {
  "tasks": [
    {
      "id": "task_001",
      "title": "Implement Service Layer Classes",
      "description": "Create EnhancedMamaBearAgent, MemoryManager, ScrapybaraManager, and ThemeManager service classes",
      "status": "in_progress",
      "priority": "critical",
      "phase": "services",
      "tags": ["backend", "services", "mama-bear", "memory", "scrapybara"],
      "created": new Date().toISOString(),
      "mamaBearVariant": "architect"
    },
    {
      "id": "task_002", 
      "title": "Setup React Frontend Foundation",
      "description": "Initialize React app with routing, theme system, and Magic MCP component library",
      "status": "pending",
      "priority": "high",
      "phase": "frontend",
      "tags": ["frontend", "react", "themes", "routing"],
      "created": new Date().toISOString(),
      "mamaBearVariant": "designer"
    },
    {
      "id": "task_003",
      "title": "Implement 7 Specialized Pages",
      "description": "Build Main Chat, VM Hub, Scout Agent, Multi-Modal Chat, MCP Marketplace, Integration Workbench, Live API Studio",
      "status": "pending", 
      "priority": "high",
      "phase": "frontend",
      "tags": ["frontend", "pages", "ui", "sanctuary"],
      "created": new Date().toISOString(),
      "mamaBearVariant": "guide"
    },
    {
      "id": "task_004",
      "title": "WebSocket Real-time Features",
      "description": "Complete SocketIO handlers for streaming, file uploads, and live interactions",
      "status": "pending",
      "priority": "medium",
      "phase": "integration", 
      "tags": ["websocket", "streaming", "real-time"],
      "created": new Date().toISOString(),
      "mamaBearVariant": "connector"
    },
    {
      "id": "task_005",
      "title": "Multi-modal Support Integration",
      "description": "Implement audio, video, and file upload capabilities across all sanctuary features",
      "status": "pending",
      "priority": "medium", 
      "phase": "integration",
      "tags": ["multimodal", "audio", "video", "files"],
      "created": new Date().toISOString(),
      "mamaBearVariant": "multimedia"
    }
  ],
  "meta": {
    "lastUpdated": new Date().toISOString(),
    "nextId": "task_006",
    "currentPhase": "services",
    "sanctuaryContext": {
      "activeTheme": "sky",
      "mamaBearOnDuty": "architect",
      "priorityFocus": "service_implementation"
    }
  }
};

fs.writeFileSync(tasksFile, JSON.stringify(currentTasks, null, 2));
console.log('✅ Created Sanctuary-specific tasks');

// Create phase tracking
const phaseFile = path.join(taskmasterDir, 'phases.json');
const phaseData = {
  "phases": {
    "foundation": {
      "status": "completed",
      "completedAt": new Date().toISOString(),
      "deliverables": ["Flask app", "SocketIO setup", "Configuration system"]
    },
    "services": {
      "status": "in_progress", 
      "startedAt": new Date().toISOString(),
      "deliverables": ["Service classes", "API integrations", "Memory persistence"]
    },
    "frontend": {
      "status": "pending",
      "deliverables": ["React app", "7 pages", "Theme system", "Component library"]
    },
    "integration": {
      "status": "pending",
      "deliverables": ["Real-time features", "Multi-modal support", "Full testing"]
    },
    "polish": {
      "status": "pending",
      "deliverables": ["Production deployment", "Performance optimization", "Documentation"]
    }
  },
  "currentPhase": "services",
  "sanctuary": {
    "totalProgress": "20%",
    "nextMilestone": "Complete all service layer implementations"
  }
};

fs.writeFileSync(phaseFile, JSON.stringify(phaseData, null, 2));
console.log('✅ Created phase tracking');

// Create mama bear context
const mamaBearFile = path.join(taskmasterDir, 'mama-bear-context.json');
const mamaBearContext = {
  "variants": {
    "architect": {
      "personality": "Systematic, methodical, focuses on structure and scalability",
      "expertise": ["Backend design", "Service architecture", "System integration"],
      "currentTask": "Service layer implementation"
    },
    "designer": {
      "personality": "Creative, aesthetic-focused, emphasizes user experience",
      "expertise": ["UI/UX design", "Theme systems", "Visual accessibility"],
      "status": "standby"
    },
    "guide": {
      "personality": "Patient, educational, breaks down complex concepts",
      "expertise": ["Documentation", "User guidance", "Feature explanation"],
      "status": "standby"
    },
    "connector": {
      "personality": "Integration-focused, handles communication between systems",
      "expertise": ["APIs", "WebSockets", "Real-time systems"],
      "status": "standby"
    },
    "multimedia": {
      "personality": "Handles rich media, audio/video processing",
      "expertise": ["File handling", "Media processing", "Multi-modal interfaces"],
      "status": "standby"
    },
    "scout": {
      "personality": "Research-oriented, explores new technologies",
      "expertise": ["Technology research", "Integration testing", "Innovation"],
      "status": "standby"
    },
    "guardian": {
      "personality": "Security and reliability focused, ensures safe operations",
      "expertise": ["Security", "Error handling", "Production readiness"],
      "status": "standby"
    }
  },
  "activeVariant": "architect",
  "contextSwitching": {
    "seamless": true,
    "memoryPersistence": true,
    "crossVariantLearning": true
  }
};

fs.writeFileSync(mamaBearFile, JSON.stringify(mamaBearContext, null, 2));
console.log('✅ Created Mama Bear context');

// Verify configuration
const configFile = path.join(__dirname, 'taskmaster.config.json');
if (fs.existsSync(configFile)) {
  const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
  console.log(`✅ Configuration verified for ${config.projectName}`);
  console.log(`🎯 Current phase: ${config.workflow.currentPhase}`);
  console.log(`🐻 Active Mama Bear: ${mamaBearContext.activeVariant}`);
} else {
  console.log('⚠️  Configuration file not found');
}

console.log('');
console.log('🏗️  PODPLAY SANCTUARY - TASKMASTER AI INITIALIZED');
console.log('');
console.log('📋 Current Priority Tasks:');
console.log('   1. ✨ Implement Service Layer Classes (Critical)');
console.log('   2. 🎨 Setup React Frontend Foundation (High)');
console.log('   3. 📱 Build 7 Specialized Pages (High)');
console.log('');
console.log('🐻 Mama Bear Architect is on duty for service implementation');
console.log('🌤️  Sky Sanctuary theme active');
console.log('');
console.log('🚀 Ready to continue building your neurodivergent-friendly sanctuary!');
