# 🏰 Podplay Sanctuary Backend Integration Guide
## Comprehensive Guide for UI Developer Integration

### ✅ **BACKEND STATUS: ALL CRITICAL SYSTEMS OPERATIONAL**

**Last Updated:** June 5, 2025  
**Backend Version:** Alpha with Jules' 289 Error Fixes Applied  
**Error Status:** ✅ All critical backend files are error-free  

---

## 🎯 **Quick Start for UI Integration**

### **1. Backend Server Setup**
```bash
cd /home/woody/Documents/podplay-claude/backend
python app.py
```
**Server runs on:** `http://localhost:5001`

### **2. WebSocket Connection**
```javascript
import io from 'socket.io-client';
const socket = io('http://localhost:5001');
```

### **3. Essential API Endpoints**
- **Health Check:** `GET /health`
- **Mama Bear Chat:** `POST /api/mama-bear/chat`
- **Computer Use:** `POST /api/computer-use/execute`
- **Collaborative Workspace:** `POST /api/collaborative/create-workspace`

---

## 🗂️ **Core Backend Systems**

### **1. Mama Bear AI Agent System**
**File:** `/backend/services/mama_bear_agent.py`  
**Status:** ✅ Error-free with 7 specialized variants

**Available Variants:**
- `architect` - Backend design & system architecture
- `designer` - UI/UX design & visual accessibility  
- `guide` - Patient, step-by-step guidance
- `connector` - APIs & real-time system integration
- `multimedia` - Rich media & file processing
- `scout` - Research & technology exploration
- `guardian` - Security & production readiness

**API Integration:**
```javascript
// Switch Mama Bear variant
const response = await fetch('/api/mama-bear/switch-variant', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    variant_type: 'designer',
    user_id: 'user123'
  })
});

// Chat with active variant
const chatResponse = await fetch('/api/mama-bear/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Help me design a beautiful UI component',
    user_id: 'user123',
    context: { current_page: 'dashboard' }
  })
});
```

### **2. Enhanced Scrapybara Orchestration**
**File:** `/backend/services/enhanced_scrapybara_orchestration.py`  
**Status:** ✅ Error-free with computer use capabilities

**Features:**
- Autonomous task execution
- Multi-step workflow orchestration
- Browser automation
- Desktop interaction
- File system operations

**API Integration:**
```javascript
// Execute computer use task
const taskResponse = await fetch('/api/computer-use/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    description: 'Take a screenshot of the current page',
    task_type: 'browser',
    context: { url: window.location.href }
  })
});
```

### **3. Collaborative Workspace System**
**File:** `/backend/api/collaborative_workspace_api.py`  
**Status:** ✅ Error-free with WebSocket support

**Features:**
- Real-time collaborative editing
- Workspace creation and management
- User role management
- Live cursor tracking
- Shared computer use sessions

**WebSocket Events:**
```javascript
// Join workspace
socket.emit('join_workspace', {
  workspace_id: 'workspace123',
  user_id: 'user123'
});

// Listen for real-time updates
socket.on('workspace_update', (data) => {
  console.log('Workspace updated:', data);
});

// Share cursor position
socket.emit('cursor_move', {
  workspace_id: 'workspace123',
  position: { x: 100, y: 200 }
});
```

### **4. Enhanced Memory System**
**File:** `/backend/services/enhanced_memory_system.py`  
**Status:** ✅ Error-free with Mem0 integration

**Features:**
- Persistent conversation memory
- User preference learning
- Context preservation across sessions
- Intelligent memory retrieval

---

## 🔌 **API Endpoints Reference**

### **Health & Status**
```
GET  /health                           - Server health check
GET  /api/services/status              - Service status overview
```

### **Mama Bear AI**
```
POST /api/mama-bear/chat               - Chat with active variant
POST /api/mama-bear/switch-variant     - Switch to different variant
GET  /api/mama-bear/variants           - List available variants
GET  /api/mama-bear/insights/:user_id  - Get user interaction insights
```

### **Computer Use**
```
POST /api/computer-use/execute         - Execute computer use task
GET  /api/computer-use/sessions        - List active sessions
POST /api/computer-use/screenshot      - Take screenshot
POST /api/computer-use/click           - Perform click action
```

### **Collaborative Workspace**
```
POST /api/collaborative/create-workspace    - Create new workspace
GET  /api/collaborative/workspaces/:id      - Get workspace details
POST /api/collaborative/join-workspace      - Join existing workspace
PUT  /api/collaborative/workspaces/:id      - Update workspace
```

### **Enhanced Orchestration**
```
POST /api/orchestration/execute-workflow   - Execute autonomous workflow
GET  /api/orchestration/active-tasks       - List active tasks
POST /api/orchestration/multi-step         - Execute multi-step workflow
```

---

## 📡 **WebSocket Events**

### **Connection & Authentication**
```javascript
socket.emit('authenticate', { user_id: 'user123', token: 'jwt_token' });
socket.on('authenticated', (data) => console.log('Connected:', data));
```

### **Workspace Events**
```javascript
// Joining/Leaving
socket.emit('join_workspace', { workspace_id, user_id });
socket.emit('leave_workspace', { workspace_id, user_id });

// Real-time collaboration
socket.on('user_joined', (data) => { /* Update UI */ });
socket.on('user_left', (data) => { /* Update UI */ });
socket.on('workspace_update', (data) => { /* Sync changes */ });

// Cursor tracking
socket.emit('cursor_move', { workspace_id, position });
socket.on('cursor_moved', (data) => { /* Update cursor UI */ });
```

### **Computer Use Events**
```javascript
// Task execution
socket.emit('execute_computer_task', { task_id, description });
socket.on('task_progress', (data) => { /* Update progress */ });
socket.on('task_completed', (data) => { /* Show results */ });

// Real-time screen sharing
socket.on('screen_update', (data) => { /* Update shared screen */ });
```

---

## 🎨 **UI Integration Patterns**

### **1. Mama Bear Chat Interface**
```jsx
const MamaBearChat = () => {
  const [messages, setMessages] = useState([]);
  const [activeVariant, setActiveVariant] = useState('architect');
  
  const sendMessage = async (message) => {
    const response = await fetch('/api/mama-bear/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        user_id: currentUser.id,
        context: { current_variant: activeVariant }
      })
    });
    
    const result = await response.json();
    setMessages(prev => [...prev, result]);
  };
  
  return (
    <div className="mama-bear-chat">
      <VariantSelector 
        active={activeVariant}
        onChange={setActiveVariant}
      />
      <MessageList messages={messages} />
      <MessageInput onSend={sendMessage} />
    </div>
  );
};
```

### **2. Collaborative Workspace Component**
```jsx
const CollaborativeWorkspace = ({ workspaceId }) => {
  const [participants, setParticipants] = useState([]);
  const [cursors, setCursors] = useState({});
  
  useEffect(() => {
    socket.emit('join_workspace', { workspace_id: workspaceId, user_id: currentUser.id });
    
    socket.on('user_joined', (user) => {
      setParticipants(prev => [...prev, user]);
    });
    
    socket.on('cursor_moved', ({ user_id, position }) => {
      setCursors(prev => ({ ...prev, [user_id]: position }));
    });
    
    return () => {
      socket.emit('leave_workspace', { workspace_id: workspaceId, user_id: currentUser.id });
    };
  }, [workspaceId]);
  
  return (
    <div className="collaborative-workspace">
      <ParticipantsList participants={participants} />
      <SharedCanvas cursors={cursors} />
      <ComputerUsePanel workspaceId={workspaceId} />
    </div>
  );
};
```

### **3. Computer Use Interface**
```jsx
const ComputerUsePanel = () => {
  const [activeSession, setActiveSession] = useState(null);
  const [taskProgress, setTaskProgress] = useState(null);
  
  const executeTask = async (description) => {
    const response = await fetch('/api/computer-use/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        description,
        task_type: 'browser',
        context: { session_id: activeSession?.id }
      })
    });
    
    const result = await response.json();
    setTaskProgress(result);
  };
  
  return (
    <div className="computer-use-panel">
      <TaskInput onExecute={executeTask} />
      {taskProgress && <ProgressIndicator progress={taskProgress} />}
      <ScreenshotPreview sessionId={activeSession?.id} />
    </div>
  );
};
```

---

## 🔧 **Development Setup**

### **1. Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-collaborative.txt
pip install -r requirements-scrapybara.txt
```

### **2. Environment Variables**
Create `/backend/.env`:
```bash
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
MEM0_API_KEY=your_mem0_key
SCRAPYBARA_API_KEY=your_scrapybara_key
```

### **3. Frontend Integration**
```bash
cd frontend
npm install socket.io-client
npm install @types/socket.io-client  # For TypeScript
```

---

## 🐛 **Error Handling Patterns**

### **API Error Handling**
```javascript
const handleApiRequest = async (url, options) => {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    
    // Show user-friendly error message
    showErrorToast('Something went wrong. Mama Bear is looking into it! 🐻');
    
    return { error: true, message: error.message };
  }
};
```

### **WebSocket Reconnection**
```javascript
const setupWebSocket = () => {
  const socket = io('http://localhost:5001', {
    reconnection: true,
    reconnectionDelay: 1000,
    maxReconnectionAttempts: 5
  });
  
  socket.on('connect', () => {
    console.log('Connected to Podplay Sanctuary! 🏰');
  });
  
  socket.on('disconnect', () => {
    console.log('Temporarily disconnected from sanctuary...');
  });
  
  socket.on('reconnect', () => {
    console.log('Reconnected to sanctuary! Welcome back! 💜');
  });
  
  return socket;
};
```

---

## 📊 **Performance Optimization**

### **1. Request Batching**
```javascript
// Batch multiple Mama Bear requests
const batchChatRequests = async (messages) => {
  const batchResponse = await fetch('/api/mama-bear/chat-batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages,
      user_id: currentUser.id,
      batch_size: 5
    })
  });
  
  return await batchResponse.json();
};
```

### **2. WebSocket Event Throttling**
```javascript
// Throttle cursor movement events
const throttledCursorMove = throttle((position) => {
  socket.emit('cursor_move', {
    workspace_id: currentWorkspace.id,
    position
  });
}, 100); // Limit to 10 events per second
```

---

## 🎯 **Testing Integration**

### **Backend Health Check**
```javascript
const checkBackendHealth = async () => {
  try {
    const response = await fetch('/health');
    const data = await response.json();
    
    return data.status === 'healthy';
  } catch (error) {
    return false;
  }
};
```

### **Service Status Validation**
```javascript
const validateServices = async () => {
  const response = await fetch('/api/services/status');
  const services = await response.json();
  
  const requiredServices = [
    'memory_manager',
    'theme_manager', 
    'mama_bear_agent',
    'scrapybara_orchestrator'
  ];
  
  return requiredServices.every(service => 
    services[service] === 'initialized'
  );
};
```

---

## 🏗️ **Architecture Notes**

### **Key Design Principles**
1. **Neurodivergent-Friendly:** Patient, step-by-step interactions
2. **Context Preservation:** Memory across sessions and variant switches
3. **Real-time Collaboration:** Live updates without overwhelming users
4. **Sensory-Friendly:** Gentle notifications and visual feedback
5. **Error Recovery:** Graceful degradation and helpful error messages

### **Security Considerations**
- All API endpoints require authentication
- WebSocket connections are validated
- Computer use tasks are sandboxed
- Collaborative workspaces have role-based permissions

### **Scalability Features**
- Horizontal scaling support via Redis
- Database connection pooling
- WebSocket clustering capability
- Async task processing

---

## 📞 **Support & Contact**

**Backend Status:** ✅ All systems operational  
**Last Validation:** June 5, 2025  
**Version:** Alpha with Jules' comprehensive fixes

**Integration Issues?**
- Check `/health` endpoint first
- Validate WebSocket connection
- Review error logs in browser console
- Test with minimal API calls

Remember: This is your sanctuary - a safe, supportive space designed specifically for neurodivergent developers. Every feature prioritizes your comfort and cognitive needs. 🏰💜
