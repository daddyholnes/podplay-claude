
import React from 'react';
import { HashRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { MamaBearProvider } from './contexts/MamaBearContext';
import { ToastProvider } from './contexts/ToastContext';

import MainChatPage from './pages/MainChatPage';
import VMHubPage from './pages/VMHubPage';
import ScoutAgentPage from './pages/ScoutAgentPage';
import MultiModalChatPage from './pages/MultiModalChatPage';
import MCPMarketplacePage from './pages/MCPMarketplacePage';
import IntegrationWorkbenchPage from './pages/IntegrationWorkbenchPage';
import LiveAPIStudioPage from './pages/LiveAPIStudioPage';
import MiniAppsPage from './pages/MiniAppsPage';

import AnimatedBackground from './components/AnimatedBackground';
import ThemeSelector from './components/ThemeSelector';
import MamaBearFloat from './components/MamaBearFloat';
import PageLayout from './components/PageLayout';
import { PAGES } from './constants';
import { useMamaBear } from './hooks/useMamaBear';

const CurrentPageContextUpdater: React.FC = () => {
  const location = useLocation();
  const { setPageContext } = useMamaBear();

  React.useEffect(() => {
    const currentPage = PAGES.find(p => p.path === location.pathname);
    if (currentPage) {
      setPageContext(currentPage.pageContext);
    } else {
      // Handle cases like 404 or default context if needed
      const defaultPage = PAGES.find(p => p.path === '/');
      if (defaultPage) {
         setPageContext(defaultPage.pageContext);
      }
    }
  }, [location, setPageContext]);

  return null;
};


const App: React.FC = () => {
  return (
    <ThemeProvider>
      <ToastProvider>
        <MamaBearProvider>
            <Router>
              <CurrentPageContextUpdater />
              <div className="relative min-h-screen flex flex-col transition-colors duration-500">
                <AnimatedBackground />
                <PageLayout>
                  <Routes>
                    <Route path="/" element={<MainChatPage />} />
                    <Route path="/vm-hub" element={<VMHubPage />} />
                    <Route path="/scout" element={<ScoutAgentPage />} />
                    <Route path="/multi-modal-chat" element={<MultiModalChatPage />} />
                    <Route path="/mcp-marketplace" element={<MCPMarketplacePage />} />
                    <Route path="/integrations" element={<IntegrationWorkbenchPage />} />
                    <Route path="/live-api-studio" element={<LiveAPIStudioPage />} />
                    <Route path="/mini-apps" element={<MiniAppsPage />} />
                    {/* Add a 404 Page */}
                    <Route path="*" element={<div>Page Not Found</div>} /> 
                  </Routes>
                </PageLayout>
                <MamaBearFloat />
                <ThemeSelector />
              </div>
            </Router>
        </MamaBearProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}

export default App;