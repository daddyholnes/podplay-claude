import React, { useState, useRef, useEffect } from 'react';
import { useMamaBear } from '../hooks/useMamaBear';
import { useTheme } from '../hooks/useTheme';
import { ChatBubbleOvalLeftEllipsisIcon, XMarkIcon, ArrowPathIcon } from './icons';
import { useDraggable } from '../hooks/useDraggable'; // Import the hook

const MamaBearFloat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { currentVariant, chatHistory, sendUserMessage, isLoading, startNewConversation } = useMamaBear();
  const { theme } = useTheme();
  const [userInput, setUserInput] = useState('');

  const floatContentRef = useRef<HTMLDivElement>(null);
  const floatHeaderRef = useRef<HTMLDivElement>(null);
  
  const [initialFloatPosition, setInitialFloatPosition] = useState({ x: 0, y: 0 });
  const [hasBeenDragged, setHasBeenDragged] = useState(false);

  const { currentPosition: floatPosition } = useDraggable({
    contentRef: floatContentRef,
    handleRef: floatHeaderRef,
    initialPosition: initialFloatPosition,
    onDragStart: () => setHasBeenDragged(true),
    onDragEnd: (pos) => setInitialFloatPosition(pos) // Persist position after drag
  });
  
  useEffect(() => {
    // Reset position when re-opening if it wasn't dragged to a new spot
    if (isOpen && !hasBeenDragged) {
       if (floatContentRef.current) {
           floatContentRef.current.style.transform = 'translate(0px, 0px)';
       }
       setInitialFloatPosition({ x: 0, y: 0 }); // Reset for next open if not dragged
    }
    if (!isOpen) {
        setHasBeenDragged(false); // Reset dragged state when closed
    }
  }, [isOpen, hasBeenDragged]);


  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleQuickSend = () => {
    if (userInput.trim()) {
      sendUserMessage(userInput);
      setUserInput('');
    }
  };
  
  const handleClose = () => {
    setIsOpen(false);
  };


  return (
    <>
      <button
        onClick={toggleOpen}
        title={`Mama Bear (${currentVariant})`}
        className={`fixed bottom-20 right-4 z-40 p-3 rounded-full shadow-xl transition-all duration-300 ease-in-out transform hover:scale-110
          ${theme.accent.replace('text-', 'bg-')} ${theme.interactiveNeon || ''} text-white
        `}
      >
        {isOpen ? <XMarkIcon className="w-7 h-7" /> : <ChatBubbleOvalLeftEllipsisIcon className="w-7 h-7" />}
      </button>

      {isOpen && (
        <div 
          ref={floatContentRef}
          className={`fixed bottom-36 right-4 z-30 w-80 max-h-[500px] flex flex-col
            ${theme.chatBubbleBg} ${theme.text} rounded-2xl shadow-2xl border ${theme.accent.replace('text-','border-')}/80 
            overflow-hidden animate-fadeIn
          `}
          // Initial style for position if needed, transform is handled by useDraggable
        >
          <div 
            ref={floatHeaderRef}
            className={`p-3 border-b ${theme.accent.replace('text-','border-')}/30 flex justify-between items-center`}
            style={{ cursor: 'grab' }} // Indicate draggable handle
          >
            <h3 className="font-semibold text-sm">{currentVariant}</h3>
            <div className="flex items-center">
                <button onClick={startNewConversation} title="Start New Chat" className={`p-1 rounded-full hover:bg-opacity-20 ${theme.text} hover:bg-gray-500/20 mr-1`}>
                  <ArrowPathIcon className="w-4 h-4"/>
                </button>
                <button onClick={handleClose} title="Close Chat" className={`p-1 rounded-full hover:bg-opacity-20 ${theme.text} hover:bg-gray-500/20`}>
                  <XMarkIcon className="w-4 h-4"/>
                </button>
            </div>
          </div>
          
          <div className="flex-grow overflow-y-auto p-3 space-y-2 text-xs" style={{ scrollbarWidth: 'thin' }}>
            {chatHistory.length === 0 && <p className="italic text-center py-4">No messages yet. Say hi!</p>}
            {chatHistory.slice(-10).map((msg) => ( // Show last 10 messages
              <div key={msg.id} className={`p-2 rounded-lg max-w-[85%] ${msg.sender === 'user' ? `ml-auto ${theme.accent.replace('text-','bg-')}/20` : `${theme.accent.replace('text-','bg-')}/10`}`}>
                <p className="whitespace-pre-wrap">{msg.text}</p>
                <span className="text-gray-500 dark:text-gray-400 text-[10px] block mt-1 text-right">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            ))}
             {isLoading && <div className="text-center text-xs italic py-1">Mama Bear is thinking...</div>}
          </div>

          <div className={`p-2 border-t ${theme.accent.replace('text-','border-')}/30 flex`}>
            <input 
              type="text" 
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleQuickSend()}
              placeholder="Quick message..."
              className={`flex-grow p-2 text-xs rounded-lg bg-white/50 dark:bg-black/20 focus:ring-1 focus:outline-none ${theme.text} placeholder-${theme.text}/70 focus:ring-${theme.accent.split('-')[1]}-500`}
            />
            <button 
              onClick={handleQuickSend} 
              disabled={isLoading || !userInput.trim()}
              className={`ml-2 px-3 py-2 text-xs rounded-lg transition-colors ${isLoading || !userInput.trim() ? 'bg-gray-400 cursor-not-allowed' : `${theme.accent.replace('text-', 'bg-')} hover:${theme.accent.replace('text-', 'bg-')}/80`} text-white`}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default MamaBearFloat;