
import React, { createContext, useState, useCallback, ReactNode } from 'react';
import { ToastMessage } from '../types';
import { v4 as uuidv4 } from 'uuid';
import ToastContainer from '../components/ui/ToastContainer';

interface ToastContextType {
  addToast: (message: string, type: ToastMessage['type'], duration?: number) => void;
}

export const ToastContext = createContext<ToastContextType | undefined>(undefined);

interface ToastProviderProps {
  children: ReactNode;
}

export const ToastProvider: React.FC<ToastProviderProps> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback((message: string, type: ToastMessage['type'], duration: number = 5000) => {
    const id = uuidv4();
    setToasts(prevToasts => [...prevToasts, { id, message, type, duration }]);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts(prevToasts => prevToasts.filter(toast => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </ToastContext.Provider>
  );
};