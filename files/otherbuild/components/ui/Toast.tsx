
import React, { useEffect, useState } from 'react';
import { ToastMessage } from '../../types';
import { CheckCircleIcon, ExclamationCircleIcon, InformationCircleIcon, XMarkIcon, ExclamationTriangleIcon } from '../icons';

interface ToastProps {
  toast: ToastMessage;
  removeToast: (id: string) => void;
}

const Toast: React.FC<ToastProps> = ({ toast, removeToast }) => {
  const [exiting, setExiting] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setExiting(true);
      setTimeout(() => removeToast(toast.id), 300); // Allow time for exit animation
    }, toast.duration || 5000);

    return () => clearTimeout(timer);
  }, [toast, removeToast]);

  const handleClose = () => {
    setExiting(true);
    setTimeout(() => removeToast(toast.id), 300);
  };

  const typeStyles = {
    success: { bg: 'bg-green-500', icon: <CheckCircleIcon className="w-6 h-6 text-white" /> },
    error: { bg: 'bg-red-500', icon: <ExclamationCircleIcon className="w-6 h-6 text-white" /> },
    info: { bg: 'bg-blue-500', icon: <InformationCircleIcon className="w-6 h-6 text-white" /> },
    warning: { bg: 'bg-yellow-500', icon: <ExclamationTriangleIcon className="w-6 h-6 text-white" /> },
  };

  const currentStyle = typeStyles[toast.type];

  return (
    <div
      className={`
        flex items-center p-4 mb-3 rounded-lg shadow-lg text-white
        ${currentStyle.bg}
        transition-all duration-300 ease-in-out
        ${exiting ? 'opacity-0 translate-x-full' : 'opacity-100 translate-x-0'}
      `}
      role="alert"
    >
      <div className="flex-shrink-0 mr-3">{currentStyle.icon}</div>
      <div className="flex-grow text-sm font-medium">{toast.message}</div>
      <button onClick={handleClose} className="ml-4 p-1 rounded-full hover:bg-white/20" aria-label="Close toast">
        <XMarkIcon className="w-5 h-5 text-white" />
      </button>
    </div>
  );
};

export default Toast;