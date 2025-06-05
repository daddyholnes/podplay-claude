
import React, { createContext, useState, useCallback, ReactNode, useEffect } from 'react';
import { ChatMessage, MamaBearVariantName, PageContext } from '../types';
import { MAMA_BEAR_VARIANTS, LOCAL_STORAGE_USER_ID_KEY } from '../constants';
import { v4 as uuidv4 } from 'uuid';

interface MamaBearContextType {
  currentVariant: MamaBearVariantName;
  setCurrentVariant: (variant: MamaBearVariantName) => void;
  chatHistory: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  sendUserMessage: (text: string, attachments?: File[]) => Promise<void>;
  isLoading: boolean;
  userId: string;
  activeConversationId: string | null;
  startNewConversation: () => void;
  pageContext: PageContext | null;
  setPageContext: (context: PageContext) => void;
}

export const MamaBearContext = createContext<MamaBearContextType | undefined>(undefined);

interface MamaBearProviderProps {
  children: ReactNode;
}

export const MamaBearProvider: React.FC<MamaBearProviderProps> = ({ children }) => {
  const [currentVariant, setCurrentVariantState] = useState<MamaBearVariantName>(MamaBearVariantName.DEFAULT);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userId, setUserId] = useState<string>('');
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [pageContext, setPageContextState] = useState<PageContext | null>(null);


  useEffect(() => {
    let storedUserId = localStorage.getItem(LOCAL_STORAGE_USER_ID_KEY);
    if (!storedUserId) {
      storedUserId = uuidv4();
      localStorage.setItem(LOCAL_STORAGE_USER_ID_KEY, storedUserId);
    }
    setUserId(storedUserId);
    startNewConversation(); // Start a new conversation on load
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  
  const setPageContext = useCallback((context: PageContext) => {
    setPageContextState(context);
    setCurrentVariantState(MAMA_BEAR_VARIANTS[context] || MamaBearVariantName.DEFAULT);
  }, []);


  const setCurrentVariant = useCallback((variant: MamaBearVariantName) => {
    setCurrentVariantState(variant);
  }, []);
  
  const addMessage = useCallback((message: ChatMessage) => {
    setChatHistory(prev => [...prev, message]);
  }, []);

  const startNewConversation = useCallback(() => {
    setActiveConversationId(uuidv4());
    setChatHistory([]); // Clear history for new conversation
    // Potentially add a system message like "New conversation started"
    addMessage({
      id: uuidv4(),
      sender: 'system',
      text: `New chat started with ${currentVariant}.`,
      timestamp: new Date().toISOString(),
    });
  }, [addMessage, currentVariant]);


  const sendUserMessage = useCallback(async (text: string, attachments?: File[]) => {
    if (!text.trim() && (!attachments || attachments.length === 0)) return;

    const userMessage: ChatMessage = {
      id: uuidv4(),
      text: text,
      sender: 'user',
      timestamp: new Date().toISOString(),
      attachments: attachments,
      avatar: '👤' // Placeholder avatar
    };
    addMessage(userMessage);
    setIsLoading(true);

    // Simulate Mama Bear's response
    // In a real app, this would involve API calls to the backend
    setTimeout(() => {
      const mamaBearResponse: ChatMessage = {
        id: uuidv4(),
        text: `I am ${currentVariant}, and I've received your message: "${text}". I'm processing this information. ${ attachments && attachments.length > 0 ? `I also see you've attached ${attachments.length} file(s).` : '' } `,
        sender: 'mama_bear',
        timestamp: new Date().toISOString(),
        variant: currentVariant,
        avatar: '🐻' // Placeholder avatar
      };
      addMessage(mamaBearResponse);
      setIsLoading(false);
    }, 1500 + Math.random() * 1000);
  }, [addMessage, currentVariant]);


  return (
    <MamaBearContext.Provider value={{ 
      currentVariant, 
      setCurrentVariant, 
      chatHistory, 
      addMessage, 
      sendUserMessage, 
      isLoading,
      userId,
      activeConversationId,
      startNewConversation,
      pageContext,
      setPageContext
    }}>
      {children}
    </MamaBearContext.Provider>
  );
};