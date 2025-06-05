import React, { useState, useEffect } from 'react';
import MultiModalChatBar from '../components/MultiModalChatBar';
import ChatBubble from '../components/ui/ChatBubble';
import { useMamaBear } from '../hooks/useMamaBear';
import { useTheme } from '../hooks/useTheme';
import { DocumentTextIcon } from '../components/icons';
import Button from '../components/ui/Button';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const MainChatPage: React.FC = () => {
  const { chatHistory, isLoading, sendUserMessage, currentVariant } = useMamaBear();
  const { theme } = useTheme();
  const [showBrowserPreview, setShowBrowserPreview] = useState(false);
  const [selectedProject, setSelectedProject] = useState('Default Project');
  const chatContainerRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatContainerRef.current?.scrollTo(0, chatContainerRef.current.scrollHeight);
  }, [chatHistory]);

  const projects = ['Default Project', 'Scrapybara Integration', 'New UI Design', 'Mem0 Research'];

  return (
    <div className="flex h-full">
      {/* Left Sidebar - Chat History / Projects */}
      <div className={`w-1/4 min-w-[250px] max-w-[350px] ${theme.chatBubbleBg} border-r ${theme.accent.replace('text-','border-')}/20 flex flex-col`}>
        <div className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20`}>
          <h2 className={`text-lg font-semibold ${theme.accent}`}>Projects</h2>
          <select 
            value={selectedProject} 
            onChange={(e) => setSelectedProject(e.target.value)}
            className={`mt-2 w-full p-2 rounded-lg ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/50 focus:ring-1 focus:${theme.accent.replace('text-','ring-')} outline-none text-sm transition-colors duration-200`}
          >
            {projects.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <div className="flex-grow p-4 overflow-y-auto space-y-2" style={{ scrollbarWidth: 'thin' }}>
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Recent Chats (mock)</h3>
          {['Chat about API keys', 'Scrapybara ideas', 'Theme discussion'].map((chatTitle, idx) => (
            <div key={idx} className={`p-2 rounded-lg text-xs cursor-pointer hover:${theme.accent.replace('text-','bg-')}/10 ${idx === 0 ? `${theme.accent.replace('text-','bg-')}/20` : ''}`}>
              {chatTitle}
            </div>
          ))}
        </div>
         <div className={`p-3 border-t ${theme.accent.replace('text-','border-')}/20`}>
            <Button variant="secondary" size="sm" className="w-full">Load Chat History</Button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-opacity-50" style={{backgroundImage: theme.animations.clouds ? 'none' : (theme.animations.particles ? 'none' : (theme.animations.stars ? 'none' : 'initial'))}}>
        <header className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20 flex justify-between items-center bg-white/10 backdrop-blur-sm`}>
          <div>
            <h1 className="text-xl font-semibold">{currentVariant}</h1>
            <p className="text-xs opacity-70">Project: {selectedProject}</p>
          </div>
          <Button 
            variant="ghost" 
            onClick={() => setShowBrowserPreview(!showBrowserPreview)}
            leftIcon={<DocumentTextIcon className="w-5 h-5"/>}
          >
            {showBrowserPreview ? 'Hide' : 'Show'} Browser
          </Button>
        </header>
        
        <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4" style={{ scrollbarWidth: 'thin' }}>
          {chatHistory.map((msg) => (
            <ChatBubble key={msg.id} message={msg} />
          ))}
          {isLoading && (
            <div className="flex justify-center py-4">
              <LoadingSpinner text="Mama Bear is thinking..." />
            </div>
          )}
        </div>
        <MultiModalChatBar pageContextSpecificSend={sendUserMessage} />
      </div>

      {/* Collapsible Browser Preview */}
      {showBrowserPreview && (
        <div className={`w-1/3 min-w-[300px] max-w-[500px] ${theme.chatBubbleBg} border-l ${theme.accent.replace('text-','border-')}/20 flex flex-col transition-all duration-300 animate-slideInRight`}>
          <div className={`p-3 border-b ${theme.accent.replace('text-','border-')}/20 flex justify-between items-center`}>
            <h3 className="text-md font-semibold">Browser Preview</h3>
            <Button variant="ghost" size="sm" onClick={() => setShowBrowserPreview(false)}>Close</Button>
          </div>
          <div className="flex-grow p-4 bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            {/* <p className="text-gray-400 dark:text-gray-500 italic">Browser preview (mocked)</p> */}
            <iframe 
                src="https://example.com" 
                title="Mock Browser Preview" 
                className="w-full h-full border-0 rounded-lg shadow-inner"
                sandbox="allow-scripts allow-same-origin" 
            ></iframe>
          </div>
          <div className={`p-2 border-t ${theme.accent.replace('text-','border-')}/20`}>
             <input type="text" placeholder="https://example.com" className={`w-full p-1.5 text-xs rounded-lg ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/50 focus:ring-1 focus:${theme.accent.replace('text-','ring-')} outline-none transition-colors duration-200`} />
          </div>
        </div>
      )}
    </div>
  );
};

export default MainChatPage;