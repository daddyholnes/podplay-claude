
import React from 'react';
import { useTheme } from '../../hooks/useTheme';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  leftIcon,
  rightIcon,
  isLoading,
  className = '',
  ...props
}) => {
  const { theme } = useTheme();

  const baseStyles = `font-semibold rounded-lg focus:outline-none focus:ring-2 focus:ring-opacity-50 transition-all duration-200 ease-in-out inline-flex items-center justify-center`;

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  const primaryBg = theme.accent.replace('text-', 'bg-');
  const primaryHoverBg = `${primaryBg}/80`; // Assuming a way to derive hover color or define it in theme
  const primaryFocusRing = theme.accent.replace('text-', 'ring-');
  
  const variantStyles = {
    primary: `${primaryBg} text-white hover:${primaryHoverBg} focus:${primaryFocusRing} ${theme.interactiveNeon || ''}`,
    secondary: `bg-gray-200 dark:bg-gray-700 ${theme.text} hover:bg-gray-300 dark:hover:bg-gray-600 focus:ring-gray-400`,
    danger: `bg-red-500 text-white hover:bg-red-600 focus:ring-red-400 ${theme.interactiveNeon ? theme.interactiveNeon.replace('purple','red-500') : ''}`, // basic neon color change
    ghost: `${theme.text} hover:bg-gray-500/10 focus:ring-gray-400`,
  };

  const loadingStyles = isLoading ? 'opacity-70 cursor-not-allowed' : '';

  return (
    <button
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${loadingStyles} ${className}`}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading && (
        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {leftIcon && !isLoading && <span className="mr-2">{leftIcon}</span>}
      {children}
      {rightIcon && !isLoading && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
};

export default Button;