import React, { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';
import { AuroraBackground } from '@/components/ui/AuroraBackground';
import { BackgroundGradientAnimation } from '@/components/ui/BackgroundGradientAnimation';
import { GlowingEffect } from '@/components/ui/GlowingEffect';

interface ServiceStatus {
  name: string;
  status: 'active' | 'inactive' | 'loading';
  endpoint: string;
}

interface SanctuaryLayoutProps {
  children: React.ReactNode;
  currentPage?: string;
}

export const SanctuaryLayout: React.FC<SanctuaryLayoutProps> = ({ 
  children, 
  currentPage = 'Home' 
}) => {
  const [services, setServices] = useState<ServiceStatus[]>([
    { name: 'Memory Manager', status: 'loading', endpoint: '/api/memory/status' },
    { name: 'Theme Manager', status: 'loading', endpoint: '/api/theme/status' },
    { name: 'Scrapybara Manager', status: 'loading', endpoint: '/api/scrape/status' },
    { name: 'Mama Bear Agent', status: 'loading', endpoint: '/api/agent/status' }
  ]);

  const [isNavOpen, setIsNavOpen] = useState(false);
  const [theme, setTheme] = useState('sanctuary');

  const sanctuaryPages = [
    { name: 'Home', icon: '🏠', description: 'Welcome to your sanctuary' },
    { name: 'Memory Palace', icon: '🧠', description: 'Your AI-powered memory system' },
    { name: 'Creation Studio', icon: '🎨', description: 'Build and design with AI' },
    { name: 'Learning Hub', icon: '📚', description: 'Structured learning paths' },
    { name: 'Sensory Garden', icon: '🌸', description: 'Calming sensory experiences' },
    { name: 'Connection Center', icon: '💫', description: 'AI companions and chat' },
    { name: 'Control Center', icon: '⚙️', description: 'Settings and customization' }
  ];

  // Check service status
  useEffect(() => {
    const checkServices = async () => {
      const updatedServices = await Promise.all(
        services.map(async (service) => {
          try {
            const response = await fetch(`http://localhost:5001${service.endpoint}`);
            const data = await response.json();
            return { 
              ...service, 
              status: data.status === 'active' ? 'active' as const : 'inactive' as const 
            };
          } catch (error) {
            return { ...service, status: 'inactive' as const };
          }
        })
      );
      setServices(updatedServices);
    };

    checkServices();
    const interval = setInterval(checkServices, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const StatusIndicator = ({ status }: { status: 'active' | 'inactive' | 'loading' }) => (
    <div className={cn(
      "w-3 h-3 rounded-full transition-all duration-300",
      status === 'active' && "bg-green-400 shadow-lg shadow-green-400/50 animate-pulse",
      status === 'inactive' && "bg-red-400 shadow-lg shadow-red-400/50",
      status === 'loading' && "bg-yellow-400 shadow-lg shadow-yellow-400/50 animate-spin"
    )} />
  );

  return (
    <div className="min-h-screen bg-sanctuary-bg text-sanctuary-text relative overflow-hidden">
      {/* Dynamic Background based on theme */}
      {theme === 'aurora' && <AuroraBackground />}
      {theme === 'gradient' && <BackgroundGradientAnimation />}
      
      {/* Header Bar */}
      <header className="relative z-50 bg-black/20 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo and Current Page */}
            <div className="flex items-center space-x-4">
              <GlowingEffect>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  Podplay Sanctuary
                </h1>
              </GlowingEffect>
              <span className="text-sanctuary-muted">→ {currentPage}</span>
            </div>

            {/* Service Status */}
            <div className="flex items-center space-x-6">
              <div className="hidden md:flex items-center space-x-4">
                {services.map((service) => (
                  <div key={service.name} className="flex items-center space-x-2">
                    <StatusIndicator status={service.status} />
                    <span className="text-sm text-sanctuary-muted">{service.name}</span>
                  </div>
                ))}
              </div>

              {/* Theme Selector */}
              <select 
                value={theme} 
                onChange={(e) => setTheme(e.target.value)}
                className="bg-black/20 border border-white/20 rounded-lg px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400"
              >
                <option value="sanctuary">Sanctuary</option>
                <option value="aurora">Aurora</option>
                <option value="gradient">Gradient</option>
              </select>

              {/* Navigation Toggle */}
              <button
                onClick={() => setIsNavOpen(!isNavOpen)}
                className="p-2 rounded-lg bg-black/20 border border-white/20 hover:bg-white/10 transition-colors"
              >
                <span className="text-xl">{isNavOpen ? '✕' : '☰'}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Sidebar */}
      <nav className={cn(
        "fixed top-16 left-0 h-[calc(100vh-4rem)] w-80 bg-black/30 backdrop-blur-xl border-r border-white/10 z-40 transform transition-transform duration-300",
        isNavOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="p-6">
          <h2 className="text-lg font-semibold mb-6 text-sanctuary-accent">Navigation</h2>
          <div className="space-y-2">
            {sanctuaryPages.map((page) => (
              <button
                key={page.name}
                className={cn(
                  "w-full text-left p-4 rounded-xl transition-all duration-200 group",
                  "hover:bg-white/10 hover:scale-[1.02] hover:shadow-lg",
                  currentPage === page.name && "bg-purple-500/20 border border-purple-400/30"
                )}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl group-hover:scale-110 transition-transform">{page.icon}</span>
                  <div>
                    <div className="font-medium">{page.name}</div>
                    <div className="text-sm text-sanctuary-muted">{page.description}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className={cn(
        "relative z-10 transition-all duration-300",
        isNavOpen ? "ml-80" : "ml-0"
      )}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </div>
      </main>

      {/* Overlay when nav is open */}
      {isNavOpen && (
        <div 
          className="fixed inset-0 bg-black/20 z-30 lg:hidden"
          onClick={() => setIsNavOpen(false)}
        />
      )}
    </div>
  );
};