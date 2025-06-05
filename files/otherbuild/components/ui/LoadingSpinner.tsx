
import React from 'react';
import { useTheme } from '../../hooks/useTheme';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'md', text }) => {
  const { theme } = useTheme();

  const sizeClasses = {
    sm: 'w-6 h-6 border-2',
    md: 'w-10 h-10 border-4',
    lg: 'w-16 h-16 border-4',
  };

  const accentColor = theme.accent.startsWith('text-') ? theme.accent.split('-')[1] : 'sky'; // Default to sky if parsing fails

  return (
    <div className="flex flex-col items-center justify-center space-y-2">
      <div 
        className={`animate-spin rounded-full ${sizeClasses[size]} border-${accentColor}-500 border-t-transparent`}
      />
      {text && <p className={`${theme.text}/80 text-sm`}>{text}</p>}
    </div>
  );
};

export default LoadingSpinner;