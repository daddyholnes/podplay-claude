
import React, { useState, useRef, useCallback } from 'react';
import { PaperAirplaneIcon, PaperClipIcon, MicrophoneIcon, VideoCameraIcon, FaceSmileIcon } from './icons'; // Assuming icons exist
import { useMamaBear } from '../hooks/useMamaBear';
import { useTheme } from '../hooks/useTheme';
import { useToast } from '../hooks/useToast';

interface MultiModalChatBarProps {
  pageContextSpecificSend?: (text: string, attachments?: File[]) => Promise<void>; // Optional override for send logic
}

const MultiModalChatBar: React.FC<MultiModalChatBarProps> = ({ pageContextSpecificSend }) => {
  const [message, setMessage] = useState('');
  const [attachments, setAttachments] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { sendUserMessage: globalSendUserMessage, isLoading } = useMamaBear();
  const { theme } = useTheme();
  const { addToast } = useToast();

  const effectiveSendMessage = pageContextSpecificSend || globalSendUserMessage;

  const handleSend = async () => {
    if (isLoading) return;
    if (!message.trim() && attachments.length === 0) {
      addToast('Please type a message or add an attachment.', 'warning');
      return;
    }
    
    try {
      await effectiveSendMessage(message, attachments);
      setMessage('');
      setAttachments([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = ''; // Reset file input
      }
    } catch (error) {
      console.error("Error sending message:", error);
      addToast('Failed to send message.', 'error');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setAttachments(prev => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const removeAttachment = (fileName: string) => {
    setAttachments(prev => prev.filter(file => file.name !== fileName));
  };

  const handlePaste = (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    const items = e.clipboardData?.items;
    if (items) {
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.startsWith('image/')) {
          const blob = items[i].getAsFile();
          if (blob) {
            setAttachments(prev => [...prev, blob]);
            addToast(`Pasted image: ${blob.name}`, 'info');
          }
        }
      }
    }
  };
  
  const iconButtonClass = `p-2 rounded-full hover:bg-opacity-20 transition-colors ${theme.text} hover:bg-gray-500/20`;

  return (
    <div className={`p-4 border-t ${theme.chatBubbleBg} ${theme.text} border-gray-300 dark:border-gray-700`}>
      {attachments.length > 0 && (
        <div className="mb-2 flex flex-wrap gap-2">
          {attachments.map((file, idx) => (
            <div key={idx} className="bg-gray-200 dark:bg-gray-700 text-xs p-1 px-2 rounded-full flex items-center">
              <span>{file.name.length > 20 ? `${file.name.substring(0,17)}...` : file.name}</span>
              <button onClick={() => removeAttachment(file.name)} className="ml-2 text-red-500 hover:text-red-700 text-sm">&times;</button>
            </div>
          ))}
        </div>
      )}
      <div className="flex items-center space-x-2">
        <button onClick={() => addToast('Audio recording coming soon!', 'info')} className={iconButtonClass} title="Record Audio">
          <MicrophoneIcon className="w-6 h-6" />
        </button>
        <button onClick={() => addToast('Video recording coming soon!', 'info')} className={iconButtonClass} title="Record Video">
          <VideoCameraIcon className="w-6 h-6" />
        </button>
        <button onClick={() => fileInputRef.current?.click()} className={iconButtonClass} title="Attach File">
          <PaperClipIcon className="w-6 h-6" />
          <input type="file" ref={fileInputRef} onChange={handleFileChange} multiple className="hidden" />
        </button>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          onPaste={handlePaste}
          placeholder="Ask Mama Bear anything..."
          rows={1}
          className={`flex-grow p-3 rounded-xl bg-white/50 dark:bg-black/20 focus:ring-2 focus:outline-none resize-none ${theme.text} placeholder-${theme.text}/70 focus:ring-${theme.accent.split('-')[1]}-500 min-h-[48px] max-h-[150px]`}
          style={{ scrollbarWidth: 'thin' }} // For Firefox
        />
        <button onClick={() => addToast('Emoji picker coming soon!', 'info')} className={iconButtonClass} title="Emoji">
          <FaceSmileIcon className="w-6 h-6" />
        </button>
        <button 
          onClick={handleSend} 
          disabled={isLoading}
          className={`p-3 rounded-xl transition-colors ${isLoading ? 'bg-gray-400 cursor-not-allowed' : `${theme.accent.replace('text-', 'bg-')} hover:${theme.accent.replace('text-', 'bg-')}/80`} text-white ${theme.interactiveNeon && !isLoading ? theme.interactiveNeon : ''}`}
          title="Send Message"
        >
          <PaperAirplaneIcon className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
};

export default MultiModalChatBar;