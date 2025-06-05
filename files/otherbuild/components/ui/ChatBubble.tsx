
import React from 'react';
import { ChatMessage } from '../../types';
import { useTheme } from '../../hooks/useTheme';
import { PaperClipIcon } from '../icons';

interface ChatBubbleProps {
  message: ChatMessage;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message }) => {
  const { theme } = useTheme();
  const isUser = message.sender === 'user';
  const isSystem = message.sender === 'system';

  if (isSystem) {
    return (
      <div className="text-center my-2">
        <span className={`text-xs px-2 py-1 rounded-full ${theme.chatBubbleBg} ${theme.text}/70 border ${theme.accent.replace('text-','border-')}/20`}>
          {message.text}
        </span>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3 animate-fadeIn`}>
      <div 
        className={`max-w-[75%] md:max-w-[60%] p-3 rounded-xl shadow ${theme.chatBubbleText}
          ${isUser ? `${theme.accent.replace('text-','bg-')} text-white` : `${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/20`}
          ${theme.interactiveNeon && isUser ? theme.interactiveNeon : ''}
        `}
      >
        {!isUser && message.variant && (
          <p className={`text-xs font-semibold mb-1 ${isUser ? 'text-white/80' : `${theme.accent}`}`}>
            {message.avatar || '🐻'} {message.variant}
          </p>
        )}
        <p className="whitespace-pre-wrap text-sm leading-relaxed break-words">
          {message.text}
        </p>
        {message.attachments && message.attachments.length > 0 && (
          <div className="mt-2 border-t border-white/20 dark:border-gray-600/50 pt-2">
            {message.attachments.map((file, index) => (
              <div key={index} className={`text-xs flex items-center ${isUser ? 'text-white/90' : `${theme.text}/80`}`}>
                <PaperClipIcon className="w-3 h-3 mr-1.5 flex-shrink-0"/> 
                <span>{file.name} ({ (file.size / 1024).toFixed(1) } KB)</span>
              </div>
            ))}
          </div>
        )}
        <p className={`text-xs mt-1.5 ${isUser ? 'text-right text-white/70' : `text-left ${theme.text}/60`}`}>
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
};

export default ChatBubble;