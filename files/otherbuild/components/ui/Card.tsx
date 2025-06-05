import React from 'react';
import { useTheme } from '../../hooks/useTheme';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  title?: string;
  footer?: React.ReactNode;
  imgSrc?: string;
  imgAlt?: string;
  interactive?: boolean;
}

const Card: React.FC<CardProps> = ({ children, title, footer, imgSrc, imgAlt, interactive, className = '', ...props }) => {
  const { theme } = useTheme();

  const interactiveClasses = interactive 
    ? `hover:shadow-soft-xl hover:scale-[1.02] transition-all duration-300 ease-in-out cursor-pointer ${theme.interactiveNeon ? `hover:${theme.interactiveNeon}` : ''}` 
    : '';

  return (
    <div
      className={`rounded-xl shadow-soft-lg overflow-hidden ${theme.chatBubbleBg} ${theme.text} border ${theme.accent.replace('text-','border-')}/20 ${interactiveClasses} ${className}`}
      {...props}
    >
      {imgSrc && <img src={imgSrc} alt={imgAlt || title || 'Card image'} className="w-full h-48 object-cover" />}
      {title && (
        <div className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20`}>
          <h3 className={`text-lg font-semibold ${theme.accent}`}>{title}</h3>
        </div>
      )}
      <div className="p-4">
        {children}
      </div>
      {footer && (
        <div className={`p-4 border-t ${theme.accent.replace('text-','border-')}/20`}>
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;