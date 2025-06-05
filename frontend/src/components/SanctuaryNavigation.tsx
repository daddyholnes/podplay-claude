import React from 'react';
import { motion } from 'framer-motion';
import { 
  MessageCircle, 
  Monitor, 
  Bot, 
  Layers, 
  Package, 
  Zap, 
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

interface SanctuaryNavigationProps {
  currentPage: string;
  onPageChange: (pageId: string) => void;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
}

const SanctuaryNavigation: React.FC<SanctuaryNavigationProps> = ({
  currentPage,
  onPageChange,
  isCollapsed = false,
  onToggleCollapse
}) => {
  const navigationItems = [
    {
      id: 'main-chat',
      name: 'Mama Bear Central',
      description: 'Research & Planning Hub',
      icon: <MessageCircle size={20} />,
      badge: 'Core'
    },
    {
      id: 'vm-hub',
      name: 'Scrapybara Command',
      description: 'VM Instance Control',
      icon: <Monitor size={20} />,
      badge: 'DevOps'
    },
    {
      id: 'scout-bear',
      name: 'Scout Mama Bear',
      description: 'Autonomous Explorer',
      icon: <Bot size={20} />,
      badge: 'Auto'
    },
    {
      id: 'multi-modal',
      name: 'Model Symposium',
      description: 'Multi-AI Chat Hub',
      icon: <Layers size={20} />,
      badge: 'AI'
    },
    {
      id: 'mcp-marketplace',
      name: 'MCP Marketplace',
      description: 'Tool Discovery Center',
      icon: <Package size={20} />,
      badge: 'Tools'
    },
    {
      id: 'live-api',
      name: 'Live API Studio',
      description: 'Real-time API Testing',
      icon: <Zap size={20} />,
      badge: 'API'
    },
    {
      id: 'integration-workbench',
      name: 'Integration Workbench',
      description: 'Advanced Workflows',
      icon: <Settings size={20} />,
      badge: 'Pro'
    }
  ];

  return (
    <motion.div
      className={`bg-white/10 backdrop-blur-xl border-r border-white/20 flex flex-col transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
      initial={{ x: -256 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      {/* Header */}
      <div className="p-4 border-b border-white/10">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className="text-lg font-bold text-white">🏰 Sanctuary</h2>
              <p className="text-sm text-white/70">Choose your space</p>
            </motion.div>
          )}
          
          <motion.button
            onClick={onToggleCollapse}
            className="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </motion.button>
        </div>
      </div>

      {/* Navigation Items */}
      <div className="flex-1 overflow-y-auto p-2">
        <div className="space-y-1">
          {navigationItems.map((item, index) => {
            const isActive = currentPage === item.id;
            
            return (
              <motion.button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`w-full p-3 rounded-xl text-left transition-all duration-200 group ${
                  isActive 
                    ? 'bg-white/20 text-white shadow-lg' 
                    : 'text-white/70 hover:bg-white/10 hover:text-white'
                }`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 + 0.3 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <div className="flex items-center space-x-3">
                  <div className={`flex-shrink-0 transition-colors ${
                    isActive ? 'text-white' : 'text-white/70 group-hover:text-white'
                  }`}>
                    {item.icon}
                  </div>
                  
                  {!isCollapsed && (
                    <motion.div
                      className="flex-1 min-w-0"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.4 }}
                    >
                      <div className="flex items-center justify-between">
                        <div className="min-w-0 flex-1">
                          <div className="font-medium truncate">{item.name}</div>
                          <div className="text-xs text-white/50 truncate">{item.description}</div>
                        </div>
                        
                        {item.badge && (
                          <motion.span
                            className={`ml-2 px-2 py-1 text-xs rounded-full font-medium ${
                              isActive 
                                ? 'bg-white/20 text-white' 
                                : 'bg-white/10 text-white/60'
                            }`}
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ delay: index * 0.1 + 0.5 }}
                          >
                            {item.badge}
                          </motion.span>
                        )}
                      </div>
                    </motion.div>
                  )}
                </div>
                
                {/* Active indicator */}
                {isActive && (
                  <motion.div
                    className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-purple-400 to-blue-400 rounded-r-full"
                    layoutId="activeIndicator"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.2 }}
                  />
                )}
              </motion.button>
            );
          })}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-white/10">
        {!isCollapsed && (
          <motion.div
            className="text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <div className="text-xs text-white/50 mb-2">Sanctuary Status</div>
            <div className="flex items-center justify-center space-x-1">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-white/70">All systems active</span>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default SanctuaryNavigation;
