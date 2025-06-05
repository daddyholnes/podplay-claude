import React from 'react';
import { useTheme } from '../../hooks/useTheme';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

const Input: React.FC<InputProps> = ({ label, error, icon, className = '', type = 'text', ...props }) => {
  const { theme } = useTheme();
  const hasIcon = Boolean(icon);

  return (
    <div className="w-full">
      {label && <label className={`block text-sm font-medium mb-1 ${theme.text}/80`}>{label}</label>}
      <div className="relative">
        {hasIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className={`${theme.text}/50`}>{icon}</span>
          </div>
        )}
        <input
          type={type}
          className={`
            block w-full px-3 py-2 rounded-lg shadow-sm
            ${theme.chatBubbleBg} ${theme.text} 
            border ${error ? 'border-red-500' : `${theme.accent.replace('text-','border-')}/30`}
            focus:outline-none focus:ring-2 ${error ? 'focus:ring-red-500' : `focus:${theme.accent.replace('text-','ring-')}`}
            placeholder-${theme.text}/50
            transition-colors duration-200
            ${hasIcon ? 'pl-10' : ''}
            ${className}
          `}
          {...props}
        />
      </div>
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  );
};

export default Input;