import React from 'react';
import { useTheme } from '../hooks/useTheme';
import { ThemeName } from '../types';
import { SunIcon, MoonIcon, SparklesIcon } from './icons'; // Assuming icons exist

const ThemeSelector: React.FC = () => {
  const { theme, themeName, setThemeName, themes } = useTheme(); // Added 'theme' here

  const themeOptions = [
    { name: ThemeName.LIGHT, label: 'Sky', icon: <SunIcon className="w-5 h-5" /> },
    { name: ThemeName.PURPLE, label: 'Neon', icon: <SparklesIcon className="w-5 h-5" /> },
    { name: ThemeName.DARK, label: 'Stellar', icon: <MoonIcon className="w-5 h-5" /> },
  ];

  return (
    <div className="fixed bottom-4 right-4 z-50 p-2 bg-white/30 dark:bg-gray-800/30 backdrop-blur-md rounded-2xl shadow-lg flex space-x-1">
      {themeOptions.map(option => (
        <button
          key={option.name}
          onClick={() => setThemeName(option.name)}
          title={themes[option.name].name}
          className={`p-2 rounded-full transition-all duration-300 ease-in-out focus:outline-none
            ${themeName === option.name 
              ? `${theme.accent.replace('text-', 'bg-')} text-white shadow-md` 
              : `text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700`
            }
            ${themes[themeName].interactiveNeon && themeName === option.name ? themes[themeName].interactiveNeon : ''}
          `}
        >
          {option.icon}
          <span className="sr-only">{option.label}</span>
        </button>
      ))}
    </div>
  );
};

export default ThemeSelector;