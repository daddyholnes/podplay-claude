
import React, { useState } from 'react';
import { useTheme } from '../hooks/useTheme';
import Card from '../components/ui/Card';
import Modal from '../components/ui/Modal';
import { PlayCircleIcon } from '../components/icons';
import { MINI_APPS_LIST } from '../constants';
import { MiniApp } from '../types';
import Button from '../components/ui/Button';

const MiniAppsPage: React.FC = () => {
  const { theme } = useTheme();
  const [selectedApp, setSelectedApp] = useState<MiniApp | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleAppClick = (app: MiniApp) => {
    setSelectedApp(app);
    setIsModalOpen(true);
  };

  return (
    <div className="p-6 flex flex-col h-full">
      <header className="mb-6">
        <h1 className={`text-3xl font-bold ${theme.accent} flex items-center`}>
          <PlayCircleIcon className="w-8 h-8 mr-2" /> Mini Apps
        </h1>
        <p className={`${theme.text}/70`}>Quick access to popular AI web tools and services.</p>
      </header>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 overflow-y-auto flex-grow" style={{ scrollbarWidth: 'thin' }}>
        {MINI_APPS_LIST.map(app => (
          <Card 
            key={app.id} 
            className="flex flex-col items-center text-center p-4" 
            interactive 
            onClick={() => handleAppClick(app)}
          >
            <img 
              src={app.logoUrl} 
              alt={`${app.name} logo`} 
              className="w-16 h-16 mb-3 rounded-lg object-contain"
              onError={(e) => (e.currentTarget.src = 'https://picsum.photos/seed/defaultlogo/64/64')} // Fallback image
            />
            <h3 className="font-semibold text-md mb-1 truncate w-full" title={app.name}>{app.name}</h3>
            <p className="text-xs opacity-70 h-10 overflow-hidden text-ellipsis">{app.description}</p>
          </Card>
        ))}
      </div>

      {selectedApp && (
        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={selectedApp.name} size="xl">
          <div className="flex flex-col h-[80vh]"> {/* Ensure modal content has height */}
            <div className="mb-2 flex justify-between items-center">
                <p className="text-sm opacity-80">{selectedApp.description}</p>
                <Button variant="ghost" size="sm" onClick={() => window.open(selectedApp.appUrl, '_blank')}>Open in New Tab</Button>
            </div>
            <iframe
              src={selectedApp.appUrl}
              title={selectedApp.name}
              className="w-full flex-grow border-0 rounded-md shadow-inner"
              sandbox="allow-scripts allow-same-origin allow-forms allow-popups" // Adjust sandbox as needed
              onError={(e) => console.error("Iframe loading error for " + selectedApp.name, e)}
            >
              <p>Your browser does not support iframes, or the content provider prevents embedding. Please <a href={selectedApp.appUrl} target="_blank" rel="noopener noreferrer" className={`${theme.accent} hover:underline`}>open this app in a new tab</a>.</p>
            </iframe>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default MiniAppsPage;