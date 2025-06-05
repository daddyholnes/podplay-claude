import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Brain, Zap, Shield, Search, Code, Wrench, Globe, Crown } from 'lucide-react';
import { ImmersiveLoader } from '../../../shared-components/src/components/effects/ImmersiveLoader';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'mama-bear';
  timestamp: Date;
  agent?: string;
}

interface OrchestrationStatus {
  orchestrator_available: boolean;
  agents_available: number;
  agent_types: string[];
  success: boolean;
}

const agentIcons: { [key: string]: React.ComponentType<{ className?: string }> } = {
  research_specialist: Search,
  devops_specialist: Wrench,
  scout_commander: Shield,
  model_coordinator: Brain,
  tool_curator: Code,
  integration_architect: Zap,
  live_api_specialist: Globe,
  lead_developer: Crown
};

const agentColors: { [key: string]: string } = {
  research_specialist: 'text-blue-400',
  devops_specialist: 'text-green-400',
  scout_commander: 'text-red-400',
  model_coordinator: 'text-purple-400',
  tool_curator: 'text-yellow-400',
  integration_architect: 'text-pink-400',
  live_api_specialist: 'text-cyan-400',
  lead_developer: 'text-orange-400'
};

export const ConnectionCenter: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [status, setStatus] = useState<OrchestrationStatus | null>(null);
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Show magical loading for 4 seconds before revealing the sanctuary
    const initTimer = setTimeout(() => {
      setIsInitializing(false);
    }, 4000);

    // Check orchestration status on mount
    fetchStatus();
    
    // Add welcome message (but don't show until loading is done)
    setTimeout(() => {
      setMessages([{
        id: '1',
        content: '🐻 Welcome to your enhanced Mama Bear Sanctuary! I have 8 specialized AI companions ready to help you. What would you like to work on today?',
        sender: 'mama-bear',
        timestamp: new Date()
      }]);
    }, 4000);

    return () => clearTimeout(initTimer);
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/mama-bear/orchestration/status');
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Failed to fetch orchestration status:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5001/api/mama-bear/orchestration/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const mamaBearMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: data.response,
          sender: 'mama-bear',
          timestamp: new Date(),
          agent: data.selected_agent || 'mama-bear'
        };
        
        setMessages(prev => [...prev, mamaBearMessage]);
      } else {
        throw new Error(data.error || 'Failed to get response');
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I encountered an error: ${error}. Please try again.`,
        sender: 'mama-bear',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Magical loading screen for sanctuary initialization */}
      {isInitializing && (
        <ImmersiveLoader
          message="Awakening your AI companions..."
          showBearClimbing={true}
          showRocketLaunch={true}
          showHoneyParticles={true}
          onComplete={() => setIsInitializing(false)}
        />
      )}
      
      {/* Main content - only show after initialization */}
      {!isInitializing && (
        <div className="min-h-[80vh] flex flex-col pr-20">
      {/* Header with Status */}
      <div className="p-6 border-b border-white/10">
        <h1 className="text-4xl font-bold text-sanctuary-accent mb-4 flex items-center gap-3">
          <Bot className="text-purple-400" />
          💫 Enhanced Mama Bear Connection Center
        </h1>
        
        {status && (
          <div className="flex items-center gap-4 p-4 rounded-xl bg-black/20 backdrop-blur-sm border border-purple-400/30">
            <div className={`w-3 h-3 rounded-full ${status.orchestrator_available ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span className="text-sanctuary-text">
              {status.agents_available} AI Companions Active
            </span>
            
            <div className="flex gap-2 ml-4">
              {status.agent_types.map((agent) => {
                const IconComponent = agentIcons[agent] || Bot;
                const colorClass = agentColors[agent] || 'text-gray-400';
                return (
                  <div key={agent} title={agent.replace('_', ' ')}>
                    <IconComponent 
                      className={`w-5 h-5 ${colorClass}`}
                    />
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] p-4 rounded-2xl ${
                message.sender === 'user'
                  ? 'bg-purple-600/20 border border-purple-400/30 text-sanctuary-text'
                  : 'bg-black/20 border border-white/10 text-sanctuary-text'
              }`}
            >
              <div className="flex items-start gap-3">
                {message.sender === 'mama-bear' && (
                  <div className="flex items-center gap-2">
                    <Bot className="w-5 h-5 text-purple-400" />
                    {message.agent && agentIcons[message.agent] && (
                      <div className="flex items-center gap-1">
                        {React.createElement(agentIcons[message.agent], {
                          className: `w-4 h-4 ${agentColors[message.agent] || 'text-gray-400'}`
                        })}
                      </div>
                    )}
                  </div>
                )}
                
                {message.sender === 'user' && (
                  <User className="w-5 h-5 text-blue-400" />
                )}
                
                <div className="flex-1">
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  <span className="text-xs text-sanctuary-muted mt-2 block">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[70%] p-4 rounded-2xl bg-black/20 border border-white/10">
              <div className="flex items-center gap-3">
                <Bot className="w-5 h-5 text-purple-400 animate-pulse" />
                <span className="text-sanctuary-muted">Mama Bear is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-white/10">
        <div className="flex gap-3">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts with Mama Bear and her 8 AI companions..."
            className="flex-1 p-4 rounded-xl bg-black/20 border border-white/10 text-sanctuary-text placeholder-sanctuary-muted resize-none focus:outline-none focus:border-purple-400/50 transition-colors"
            rows={3}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
            className="px-6 py-4 rounded-xl bg-purple-600/20 border border-purple-400/30 text-purple-400 hover:bg-purple-600/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Send
          </button>
        </div>
        
        <p className="text-xs text-sanctuary-muted mt-3 text-center">
          💡 Try asking about development, debugging, research, or just share what's on your mind!
        </p>
      </div>
        </div>
      )}
    </>
  );
};
