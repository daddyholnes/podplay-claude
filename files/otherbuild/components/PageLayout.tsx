import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { PAGES, APP_NAME } from '../constants';
import { useTheme } from '../hooks/useTheme';
import { Bars3Icon, XMarkIcon } from './icons'; // Assuming icons exist

interface PageLayoutProps {
  children: React.ReactNode;
}

const PageLayout: React.FC<PageLayoutProps> = ({ children }) => {
  const { theme } = useTheme();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const currentPageName = PAGES.find(p => p.path === location.pathname)?.name || APP_NAME;

  return (
    <div className={`flex h-screen ${theme.text} overflow-hidden`}>
      {/* Sidebar for larger screens */}
      <aside className={`hidden md:flex flex-col w-64 ${theme.chatBubbleBg} border-r ${theme.accent.replace('text-','border-')}/20 transition-all duration-300 z-20`}>
        <div className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20 flex items-center justify-center`}>
          <img src="https://picsum.photos/seed/podplaylogo/40/40" alt="Logo" className="w-10 h-10 rounded-full mr-2" />
          <h1 className={`text-xl font-bold ${theme.accent}`}>{APP_NAME}</h1>
        </div>
        <nav className="flex-grow p-4 space-y-2 overflow-y-auto" style={{ scrollbarWidth: 'thin' }}>
          {PAGES.map((page) => (
            <NavLink
              key={page.path}
              to={page.path}
              className={({ isActive }) => 
                `flex items-center space-x-3 p-3 rounded-xl transition-colors duration-200 hover:${theme.accent.replace('text-','bg-')}/20 
                ${isActive ? `${theme.accent.replace('text-','bg-')}/30 ${theme.accent}` : `${theme.text}/80 hover:${theme.text}`}
                ${theme.interactiveNeon && isActive ? theme.interactiveNeon : ''}
                group`
              }
            >
              {({ isActive }) => (
                <>
                  {page.icon && <page.icon className={`w-5 h-5 ${isActive ? theme.accent : `${theme.text}/70 group-hover:${theme.text}`}`} />}
                  <span className="text-sm font-medium">{page.name}</span>
                </>
              )}
            </NavLink>
          ))}
        </nav>
        <div className={`p-2 border-t ${theme.accent.replace('text-','border-')}/20 text-center text-xs ${theme.text}/60`}>
          Podplay Sanctuary &copy; {new Date().getFullYear()}
        </div>
      </aside>

      {/* Mobile Sidebar (Drawer) */}
      {sidebarOpen && (
         <div 
            className="fixed inset-0 bg-black/50 z-30 md:hidden" 
            onClick={() => setSidebarOpen(false)}
          >
          <aside 
            className={`fixed top-0 left-0 h-full w-64 ${theme.chatBubbleBg} border-r ${theme.accent.replace('text-','border-')}/20 transition-transform duration-300 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} z-40 flex flex-col`}
            onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside sidebar
          >
            <div className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20 flex items-center justify-between`}>
              <div className="flex items-center">
                <img src="https://picsum.photos/seed/podplaylogo/32/32" alt="Logo" className="w-8 h-8 rounded-full mr-2" />
                <h1 className={`text-lg font-bold ${theme.accent}`}>{APP_NAME}</h1>
              </div>
              <button onClick={() => setSidebarOpen(false)} className={`${theme.text} p-1 rounded hover:bg-gray-500/20`}>
                <XMarkIcon className="w-6 h-6"/>
              </button>
            </div>
            <nav className="flex-grow p-4 space-y-2 overflow-y-auto" style={{ scrollbarWidth: 'thin' }}>
              {PAGES.map((page) => (
                <NavLink
                  key={page.path}
                  to={page.path}
                  onClick={() => setSidebarOpen(false)} // Close sidebar on navigation
                  className={({ isActive }) => 
                    `flex items-center space-x-3 p-3 rounded-xl transition-colors duration-200 hover:${theme.accent.replace('text-','bg-')}/20 
                    ${isActive ? `${theme.accent.replace('text-','bg-')}/30 ${theme.accent}` : `${theme.text}/80 hover:${theme.text}`}
                    ${theme.interactiveNeon && isActive ? theme.interactiveNeon : ''}
                    group`
                  }
                >
                  {({ isActive }) => (
                    <>
                      {page.icon && <page.icon className={`w-5 h-5 ${isActive ? theme.accent : `${theme.text}/70 group-hover:${theme.text}`}`} />}
                      <span className="text-sm font-medium">{page.name}</span>
                    </>
                  )}
                </NavLink>
              ))}
            </nav>
            <div className={`p-2 border-t ${theme.accent.replace('text-','border-')}/20 text-center text-xs ${theme.text}/60`}>
              &copy; {new Date().getFullYear()}
            </div>
          </aside>
        </div>
      )}


      {/* Main content area */}
      <main className="flex-1 flex flex-col overflow-hidden relative z-10">
         {/* Mobile Header */}
        <header className={`md:hidden p-3 ${theme.chatBubbleBg} border-b ${theme.accent.replace('text-','border-')}/20 flex items-center justify-between sticky top-0 z-20`}>
          <button onClick={() => setSidebarOpen(true)} className={`${theme.text} p-2 rounded hover:bg-gray-500/20`}>
            <Bars3Icon className="w-6 h-6"/>
          </button>
          <h2 className={`text-md font-semibold ${theme.accent}`}>{currentPageName}</h2>
          <div className="w-8"></div> {/* Spacer */}
        </header>
        <div className="flex-1 overflow-y-auto" style={{ scrollbarWidth: 'thin' }}>
          {children}
        </div>
      </main>
    </div>
  );
};

export default PageLayout;