import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Search, Globe, Brain } from 'lucide-react';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'mama-bear';
  timestamp: Date;
  type: 'text' | 'search' | 'web-result';
  metadata?: {
    searchQuery?: string;
    url?: string;
    title?: string;
  };
}

interface Project {
  id: string;
  name: string;
  description: string;
  lastActive: Date;
  messageCount: number;
}

const MainChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [showBrowser, setShowBrowser] = useState(false);
  const [browserUrl, setBrowserUrl] = useState('');
  const [isInitializing, setIsInitializing] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Initialize with Mama Bear greeting
  useEffect(() => {
    const initializeChat = async () => {
      setIsInitializing(true);
      
      // Simulate loading sanctuary
      await new Promise(resolve => setTimeout(resolve, 4000));
      
      setIsInitializing(false);
      
      // Welcome message from Mama Bear
      const welcomeMessage: Message = {
        id: '1',
        content: `🐻 Welcome to your sanctuary, dear! I'm Mama Bear, your research specialist and caring companion. 

I'm here to help you explore ideas, research topics, and discover new knowledge. I can:
• 🌐 Search the web and browse any site
• 📚 Analyze documents and papers
• 💡 Help with project planning and research
• 🔍 Dive deep into any topic you're curious about

What would you like to explore today? I'm excited to learn alongside you! ✨`,
        sender: 'mama-bear',
        timestamp: new Date(),
        type: 'text'
      };
      
      setMessages([welcomeMessage]);
      
      // Load example projects
      setProjects([
        {
          id: '1',
          name: 'AI Research Hub',
          description: 'Exploring latest AI developments and papers',
          lastActive: new Date(),
          messageCount: 23
        },
        {
          id: '2', 
          name: 'Web Development Deep Dive',
          description: 'Modern frameworks and best practices',
          lastActive: new Date(Date.now() - 86400000),
          messageCount: 45
        }
      ]);
    };
    
    initializeChat();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };
    
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);
    
    try {
      // Connect to actual Mama Bear backend
      const response = await fetch('http://localhost:5001/api/mama-bear/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentInput,
          user_id: 'sanctuary-user',
          conversation_id: currentProject?.id || 'default'
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      const mamaBearResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response || '🐻 I encountered an issue processing your request. Let me try again!',
        sender: 'mama-bear',
        timestamp: new Date(),
        type: 'text'
      };
      
      setMessages(prev => [...prev, mamaBearResponse]);
      
    } catch (error) {
      console.error('Chat API error:', error);
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: `🐻 I'm having trouble connecting to my systems right now. This might be because:

• The backend is still starting up
• There's a network connectivity issue  
• My AI models are being updated

Let me try to reconnect... In the meantime, feel free to ask me anything and I'll respond once I'm back online! ✨`,
        sender: 'mama-bear',
        timestamp: new Date(),
        type: 'text'
      };
      
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (isInitializing) {
    return (
      <div className="h-full flex items-center justify-center bg-gradient-to-br from-purple-50 via-blue-50 to-green-50">
        <motion.div 
          className="text-center space-y-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <motion.div
            className="text-6xl"
            animate={{ 
              rotate: [0, 10, -10, 0],
              scale: [1, 1.1, 1] 
            }}
            transition={{ 
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            🐻
          </motion.div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Preparing your research sanctuary...
          </h2>
          <div className="flex items-center justify-center space-x-2">
            <motion.div
              className="w-3 h-3 bg-purple-500 rounded-full"
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 1, repeat: Infinity, delay: 0 }}
            />
            <motion.div
              className="w-3 h-3 bg-blue-500 rounded-full"
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
            />
            <motion.div
              className="w-3 h-3 bg-green-500 rounded-full"
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
            />
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-green-50 flex">
      {/* Left Sidebar - Projects & Chat History */}
      <motion.div 
        className="w-80 bg-white/70 backdrop-blur-xl border-r border-purple-200/50 p-4 overflow-y-auto"
        initial={{ x: -320 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <div className="space-y-4">
          {/* Header */}
          <div className="text-center pb-4 border-b border-purple-200/50">
            <h2 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              🐻 Mama Bear Central
            </h2>
            <p className="text-sm text-gray-600 mt-1">Research Specialist</p>
          </div>
          
          {/* Current Project */}
          {currentProject && (
            <div className="bg-purple-100/50 rounded-lg p-3">
              <h3 className="font-medium text-purple-800">{currentProject.name}</h3>
              <p className="text-sm text-purple-600 mt-1">{currentProject.description}</p>
              <div className="text-xs text-purple-500 mt-2">
                {currentProject.messageCount} messages
              </div>
            </div>
          )}
          
          {/* Projects List */}
          <div className="space-y-2">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Recent Projects</h3>
            {projects.map((project) => (
              <motion.div
                key={project.id}
                className="p-3 rounded-lg bg-white/50 border border-purple-100 cursor-pointer hover:bg-purple-50/50 transition-colors"
                whileHover={{ scale: 1.02 }}
                onClick={() => setCurrentProject(project)}
              >
                <div className="font-medium text-gray-800">{project.name}</div>
                <div className="text-sm text-gray-600 truncate">{project.description}</div>
                <div className="text-xs text-gray-500 mt-1">
                  {project.messageCount} messages • {project.lastActive.toLocaleDateString()}
                </div>
              </motion.div>
            ))}
          </div>
          
          {/* New Project Button */}
          <motion.button
            className="w-full p-3 rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 text-white font-medium"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            ✨ Start New Project
          </motion.button>
        </div>
      </motion.div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <motion.div 
          className="bg-white/70 backdrop-blur-xl border-b border-purple-200/50 p-4 flex items-center justify-between"
          initial={{ y: -60 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
              🐻
            </div>
            <div>
              <h1 className="font-bold text-gray-800">Mama Bear Research Sanctuary</h1>
              <p className="text-sm text-gray-600">Your caring AI research companion</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <motion.button
              className="p-2 rounded-lg bg-purple-100/50 text-purple-600 hover:bg-purple-200/50 transition-colors"
              whileHover={{ scale: 1.1 }}
              onClick={() => setShowBrowser(!showBrowser)}
            >
              <Globe size={20} />
            </motion.button>
            <motion.button
              className="p-2 rounded-lg bg-blue-100/50 text-blue-600 hover:bg-blue-200/50 transition-colors"
              whileHover={{ scale: 1.1 }}
            >
              <Brain size={20} />
            </motion.button>
          </div>
        </motion.div>

        <div className="flex-1 flex">
          {/* Messages Area */}
          <div className={`flex-1 flex flex-col ${showBrowser ? 'w-2/3' : 'w-full'}`}>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className={`max-w-2xl px-4 py-3 rounded-2xl ${
                      message.sender === 'user' 
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white ml-12'
                        : 'bg-white/70 backdrop-blur-sm border border-purple-200/50 text-gray-800 mr-12'
                    }`}>
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      <div className={`text-xs mt-2 ${
                        message.sender === 'user' ? 'text-purple-100' : 'text-gray-500'
                      }`}>
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              
              {/* Loading indicator */}
              {isLoading && (
                <motion.div
                  className="flex justify-start"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className="bg-white/70 backdrop-blur-sm border border-purple-200/50 text-gray-800 mr-12 px-4 py-3 rounded-2xl">
                    <div className="flex items-center space-x-2">
                      <motion.div
                        className="flex space-x-1"
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                      >
                        <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                        <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      </motion.div>
                      <span className="text-sm text-gray-600">Mama Bear is thinking...</span>
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <motion.div 
              className="border-t border-purple-200/50 bg-white/50 backdrop-blur-xl p-4"
              initial={{ y: 60 }}
              animate={{ y: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
            >
              <div className="flex items-end space-x-3">
                <div className="flex-1 relative">
                  <input
                    ref={inputRef}
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask Mama Bear anything... 🐻✨"
                    className="w-full px-4 py-3 rounded-2xl border border-purple-200/50 bg-white/70 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent resize-none"
                    disabled={isLoading}
                  />
                </div>
                <motion.button
                  onClick={sendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  className="p-3 rounded-2xl bg-gradient-to-r from-purple-500 to-blue-500 text-white disabled:opacity-50 disabled:cursor-not-allowed"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Send size={20} />
                </motion.button>
              </div>
            </motion.div>
          </div>

          {/* Browser Panel */}
          <AnimatePresence>
            {showBrowser && (
              <motion.div
                className="w-1/3 border-l border-purple-200/50 bg-white/30 backdrop-blur-xl"
                initial={{ x: 400 }}
                animate={{ x: 0 }}
                exit={{ x: 400 }}
                transition={{ duration: 0.3, ease: "easeOut" }}
              >
                <div className="p-4 border-b border-purple-200/50">
                  <div className="flex items-center space-x-2">
                    <Search size={16} className="text-gray-500" />
                    <input
                      type="text"
                      value={browserUrl}
                      onChange={(e) => setBrowserUrl(e.target.value)}
                      placeholder="Enter URL or search..."
                      className="flex-1 px-3 py-2 rounded-lg border border-purple-200 bg-white/50 focus:outline-none focus:ring-2 focus:ring-purple-300"
                    />
                  </div>
                </div>
                <div className="h-full flex items-center justify-center text-gray-500">
                  <div className="text-center">
                    <Globe size={48} className="mx-auto mb-4 text-purple-400" />
                    <p>Browser preview will appear here</p>
                    <p className="text-sm mt-2">*Connected to Scrapybara for live browsing*</p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default MainChat;
