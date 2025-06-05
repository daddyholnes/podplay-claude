import React, { useState, useEffect, useCallback } from 'react';
import { useMamaBear } from '../hooks/useMamaBear';
import { useTheme } from '../hooks/useTheme';
import ChatBubble from '../components/ui/ChatBubble';
import MultiModalChatBar from '../components/MultiModalChatBar';
import { Cog6ToothIcon, ArrowPathIcon } from '../components/icons';
import { AI_MODELS_FOR_MULTIMODAL_CHAT } from '../constants';
import { ChatMessage } from '../types';
import { v4 as uuidv4 } from 'uuid';
import LoadingSpinner from '../components/ui/LoadingSpinner';

interface ModelSettings {
  temperature: number;
  maxTokens: number;
  topP: number;
}

const MultiModalChatPage: React.FC = () => {
  const { currentVariant, addMessage: globalAddMessage, isLoading: globalIsLoading } = useMamaBear();
  const { theme } = useTheme();
  
  const [selectedModel, setSelectedModel] = useState(AI_MODELS_FOR_MULTIMODAL_CHAT[0]);
  const [chatHistories, setChatHistories] = useState<Record<string, ChatMessage[]>>({});
  const [currentChat, setCurrentChat] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [modelSettings, setModelSettings] = useState<ModelSettings>({
    temperature: 0.7,
    maxTokens: 2048,
    topP: 0.9,
  });
  const chatContainerRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    setCurrentChat(chatHistories[selectedModel.id] || []);
  }, [selectedModel, chatHistories]);

  useEffect(() => {
    chatContainerRef.current?.scrollTo(0, chatContainerRef.current.scrollHeight);
  }, [currentChat]);

  const addMessageToHistory = useCallback((modelId: string, message: ChatMessage) => {
    setChatHistories(prev => ({
      ...prev,
      [modelId]: [...(prev[modelId] || []), message]
    }));
  }, []);
  
  const handleSendMessage = async (text: string, attachments?: File[]) => {
    if (!text.trim() && (!attachments || attachments.length === 0)) return;
    setIsLoading(true);

    const userMessage: ChatMessage = {
      id: uuidv4(),
      text,
      sender: 'user',
      timestamp: new Date().toISOString(),
      attachments,
    };
    addMessageToHistory(selectedModel.id, userMessage);

    // Simulate model response
    setTimeout(() => {
      const modelResponse: ChatMessage = {
        id: uuidv4(),
        text: `Response from ${selectedModel.name} (Provider: ${selectedModel.provider}): You said "${text}". Temp: ${modelSettings.temperature}, Tokens: ${modelSettings.maxTokens}.`,
        sender: 'mama_bear', // Simulating model as Mama Bear
        timestamp: new Date().toISOString(),
        variant: currentVariant, // Or a specific model variant
      };
      addMessageToHistory(selectedModel.id, modelResponse);
      setIsLoading(false);
    }, 1500 + Math.random() * 1000);
  };

  const handleClearChat = () => {
    setChatHistories(prev => ({ ...prev, [selectedModel.id]: [] }));
    // Optionally add a system message
    const systemMessage: ChatMessage = {
      id: uuidv4(),
      text: `Chat history with ${selectedModel.name} cleared.`,
      sender: 'system',
      timestamp: new Date().toISOString(),
    };
    addMessageToHistory(selectedModel.id, systemMessage);
  };

  return (
    <div className="flex h-full">
      {/* Left Sidebar: Chat History (per model) */}
      <div className={`w-1/4 min-w-[200px] max-w-[300px] ${theme.chatBubbleBg} border-r ${theme.accent.replace('text-','border-')}/20 flex flex-col`}>
        <div className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20`}>
          <h2 className={`text-lg font-semibold ${theme.accent}`}>Models</h2>
          <select
            value={selectedModel.id}
            onChange={(e) => setSelectedModel(AI_MODELS_FOR_MULTIMODAL_CHAT.find(m => m.id === e.target.value) || AI_MODELS_FOR_MULTIMODAL_CHAT[0])}
            className={`mt-2 w-full p-2 rounded-lg ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/50 focus:ring-1 focus:${theme.accent.replace('text-','ring-')} outline-none text-sm transition-colors duration-200`}
          >
            {AI_MODELS_FOR_MULTIMODAL_CHAT.map(model => (
              <option key={model.id} value={model.id}>{model.name} ({model.provider})</option>
            ))}
          </select>
        </div>
        <div className="flex-grow p-4 overflow-y-auto space-y-2" style={{ scrollbarWidth: 'thin' }}>
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Recent Chats with {selectedModel.name}</h3>
          {currentChat.filter(msg => msg.sender === 'user').slice(-5).reverse().map(msg => (
            <div key={msg.id} className={`p-2 rounded-lg text-xs cursor-pointer hover:${theme.accent.replace('text-','bg-')}/10 truncate`}>
              {msg.text}
            </div>
          ))}
          {currentChat.length === 0 && <p className="text-xs italic opacity-60">No messages yet with {selectedModel.name}.</p>}
        </div>
         <div className={`p-3 border-t ${theme.accent.replace('text-','border-')}/20`}>
            <button onClick={handleClearChat} className={`w-full text-xs p-2 rounded-lg ${theme.text}/70 hover:${theme.text} hover:bg-red-500/20 transition-colors flex items-center justify-center`}>
              <ArrowPathIcon className="w-4 h-4 mr-1.5"/> Clear Chat with {selectedModel.name}
            </button>
        </div>
      </div>

      {/* Center: Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <header className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20 flex justify-between items-center bg-white/10 backdrop-blur-sm`}>
          <div>
            <h1 className="text-xl font-semibold">Chat with: {selectedModel.name}</h1>
            <p className="text-xs opacity-70">Provider: {selectedModel.provider} | Mama Bear Variant: {currentVariant}</p>
          </div>
        </header>
        <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4" style={{ scrollbarWidth: 'thin' }}>
          {currentChat.map((msg) => (
            <ChatBubble key={msg.id} message={msg} />
          ))}
          {isLoading && <div className="flex justify-center py-4"><LoadingSpinner text={`${selectedModel.name} is thinking...`} /></div>}
        </div>
        <MultiModalChatBar pageContextSpecificSend={handleSendMessage} />
      </div>

      {/* Right Sidebar: Model Settings */}
      <div className={`w-1/4 min-w-[250px] max-w-[350px] ${theme.chatBubbleBg} border-l ${theme.accent.replace('text-','border-')}/20 flex flex-col p-4 space-y-4`}>
        <h2 className={`text-lg font-semibold ${theme.accent} flex items-center`}><Cog6ToothIcon className="w-5 h-5 mr-2"/>Model Settings</h2>
        <div>
          <label htmlFor="temperature" className="block text-sm font-medium opacity-80">Temperature: {modelSettings.temperature.toFixed(1)}</label>
          <input
            type="range" id="temperature" min="0" max="1" step="0.1"
            value={modelSettings.temperature}
            onChange={(e) => setModelSettings(s => ({ ...s, temperature: parseFloat(e.target.value) }))}
            className={`w-full h-2 rounded-lg appearance-none cursor-pointer ${theme.accent.replace('text-','bg-')}/30 accent-${theme.accent.split('-')[1]}-500`} // `accent-*` for slider color
          />
        </div>
        <div>
          <label htmlFor="maxTokens" className="block text-sm font-medium opacity-80">Max Tokens: {modelSettings.maxTokens}</label>
          <input
            type="range" id="maxTokens" min="256" max="4096" step="128"
            value={modelSettings.maxTokens}
            onChange={(e) => setModelSettings(s => ({ ...s, maxTokens: parseInt(e.target.value) }))}
            className={`w-full h-2 rounded-lg appearance-none cursor-pointer ${theme.accent.replace('text-','bg-')}/30 accent-${theme.accent.split('-')[1]}-500`}
          />
        </div>
        <div>
          <label htmlFor="topP" className="block text-sm font-medium opacity-80">Top-P: {modelSettings.topP.toFixed(2)}</label>
          <input
            type="range" id="topP" min="0.1" max="1" step="0.05"
            value={modelSettings.topP}
            onChange={(e) => setModelSettings(s => ({ ...s, topP: parseFloat(e.target.value) }))}
            className={`w-full h-2 rounded-lg appearance-none cursor-pointer ${theme.accent.replace('text-','bg-')}/30 accent-${theme.accent.split('-')[1]}-500`}
          />
        </div>
        <div className="text-xs opacity-60 border-t border-gray-500/30 pt-3 mt-auto">
            Settings are applied per model. Changes affect new messages.
            <p className="mt-2">Model Availability: <span className="text-green-500">Online</span> (mocked)</p>
        </div>
      </div>
    </div>
  );
};

export default MultiModalChatPage;