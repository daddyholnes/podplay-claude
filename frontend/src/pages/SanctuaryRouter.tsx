import React, { useState, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import SanctuaryNavigation from '../components/SanctuaryNavigation';

// Lazy load sanctuary pages
const MainChat = React.lazy(() => import('./MainChat'));
const ScrapybaraHub = React.lazy(() => import('./ScrapybaraHub'));

// Placeholder components for pages not yet built
const ComingSoonPage: React.FC<{ title: string; description: string }> = ({ title, description }) => (
  <div className="h-full flex items-center justify-center">
    <motion.div
      className="text-center space-y-6 max-w-md mx-auto p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        className="text-6xl mb-4"
        animate={{ 
          rotate: [0, 10, -10, 0],
          scale: [1, 1.1, 1] 
        }}
        transition={{ 
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        🚧
      </motion.div>
      
      <h1 className="text-3xl font-bold text-white/90">{title}</h1>
      <p className="text-white/70 text-lg">{description}</p>
      
      <motion.div
        className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20"
        whileHover={{ scale: 1.05 }}
        transition={{ duration: 0.2 }}
      >
        <p className="text-white/80 mb-4">🐻 Mama Bear is preparing this magical space...</p>
        <div className="flex items-center justify-center space-x-2">
          <motion.div
            className="w-2 h-2 bg-purple-400 rounded-full"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1, repeat: Infinity, delay: 0 }}
          />
          <motion.div
            className="w-2 h-2 bg-blue-400 rounded-full"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
          />
          <motion.div
            className="w-2 h-2 bg-green-400 rounded-full"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
          />
        </div>
      </motion.div>
    </motion.div>
  </div>
);

const SanctuaryRouter: React.FC = () => {
  const [currentPage, setCurrentPage] = useState('main-chat');
  const [isNavCollapsed, setIsNavCollapsed] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'main-chat':
        return <MainChat />;
      case 'vm-hub':
        return <ScrapybaraHub />;
      case 'scout-bear':
        return <ComingSoonPage 
          title="Scout Mama Bear" 
          description="Autonomous exploration and task execution coming soon!" 
        />;
      case 'multi-modal':
        return <ComingSoonPage 
          title="Model Symposium" 
          description="Multi-AI chat hub with all your favorite models coming soon!" 
        />;
      case 'mcp-marketplace':
        return <ComingSoonPage 
          title="MCP Marketplace" 
          description="Tool discovery and installation center coming soon!" 
        />;
      case 'live-api':
        return <ComingSoonPage 
          title="Live API Studio" 
          description="Real-time API testing and development coming soon!" 
        />;
      case 'integration-workbench':
        return <ComingSoonPage 
          title="Integration Workbench" 
          description="Advanced workflow automation coming soon!" 
        />;
      default:
        return <MainChat />;
    }
  };

  const getPageTitle = () => {
    const titles = {
      'main-chat': 'Mama Bear Central',
      'vm-hub': 'Scrapybara Command Center',
      'scout-bear': 'Scout Mama Bear',
      'multi-modal': 'Model Symposium',
      'mcp-marketplace': 'MCP Marketplace',
      'live-api': 'Live API Studio',
      'integration-workbench': 'Integration Workbench'
    };
    return titles[currentPage as keyof typeof titles] || 'Podplay Sanctuary';
  };

  return (
    <div className="h-screen overflow-hidden relative">
      {/* Living Background */}
      <div className="fixed inset-0 z-0 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.3),rgba(255,255,255,0.1))]"></div>
        <div className="absolute inset-0 bg-[conic-gradient(from_0deg_at_50%_50%,rgba(120,119,198,0.1),rgba(255,255,255,0.05),rgba(120,119,198,0.1))] animate-pulse"></div>
      </div>
      
      {/* Main Layout */}
      <div className="relative z-10 h-full flex">
        {/* Navigation Sidebar */}
        <SanctuaryNavigation
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          isCollapsed={isNavCollapsed}
          onToggleCollapse={() => setIsNavCollapsed(!isNavCollapsed)}
        />
        
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Page Header */}
          <motion.div
            className="bg-white/5 backdrop-blur-xl border-b border-white/10 px-6 py-4"
            initial={{ y: -60 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-white">
                  {getPageTitle()}
                </h1>
                <p className="text-white/70 text-sm mt-1">
                  Welcome to your digital sanctuary ✨
                </p>
              </div>
              
              {/* Status Indicators */}
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-sm text-white/70">Backend Active</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                  <span className="text-sm text-white/70">AI Agents Ready</span>
                </div>
              </div>
            </div>
          </motion.div>
          
          {/* Page Content */}
          <div className="flex-1 overflow-hidden">
            <Suspense 
              fallback={
                <div className="h-full flex items-center justify-center">
                  <motion.div 
                    className="text-center space-y-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <motion.div
                      className="text-6xl"
                      animate={{ 
                        rotate: [0, 10, -10, 0],
                        scale: [1, 1.1, 1] 
                      }}
                      transition={{ 
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                    >
                      🐻
                    </motion.div>
                    <h2 className="text-xl font-bold text-white">
                      Loading sanctuary page...
                    </h2>
                    <div className="flex items-center justify-center space-x-2">
                      <motion.div
                        className="w-3 h-3 bg-purple-400 rounded-full"
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                      />
                      <motion.div
                        className="w-3 h-3 bg-blue-400 rounded-full"
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                      />
                      <motion.div
                        className="w-3 h-3 bg-green-400 rounded-full"
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                      />
                    </div>
                  </motion.div>
                </div>
              }
            >
              <AnimatePresence mode="wait">
                <motion.div
                  key={currentPage}
                  className="h-full"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                >
                  {renderPage()}
                </motion.div>
              </AnimatePresence>
            </Suspense>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SanctuaryRouter;
