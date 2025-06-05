
import React, { createContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { Theme, ThemeName, Themes } from '../types';
import { THEMES, DEFAULT_THEME, LOCAL_STORAGE_THEME_KEY } from '../constants';

interface ThemeContextType {
  theme: Theme;
  themeName: ThemeName;
  setThemeName: (name: ThemeName) => void;
  themes: Themes;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [themeName, setThemeNameState] = useState<ThemeName>(() => {
    const storedThemeName = localStorage.getItem(LOCAL_STORAGE_THEME_KEY) as ThemeName;
    return storedThemeName && THEMES[storedThemeName] ? storedThemeName : DEFAULT_THEME;
  });

  const setThemeName = useCallback((name: ThemeName) => {
    setThemeNameState(name);
    localStorage.setItem(LOCAL_STORAGE_THEME_KEY, name);
  }, []);

  useEffect(() => {
    const currentTheme = THEMES[themeName];
    const root = window.document.documentElement;
    
    // Remove old theme classes
    Object.values(THEMES).forEach(t => root.classList.remove(t.className));
    
    // Add new theme class
    root.classList.add(currentTheme.className);
    if (themeName === ThemeName.DARK || themeName === ThemeName.PURPLE) {
        root.classList.add('dark'); // For Tailwind's dark mode variant if configured by class
    } else {
        root.classList.remove('dark');
    }

  }, [themeName]);

  const theme = THEMES[themeName];

  return (
    <ThemeContext.Provider value={{ theme, themeName, setThemeName, themes: THEMES }}>
      {children}
    </ThemeContext.Provider>
  );
};