
import React, { useState } from 'react';
import { useMamaBear } from '../hooks/useMamaBear';
import { useTheme } from '../hooks/useTheme';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import { CpuChipIcon, PlayIcon, StopIcon, PauseIcon, PlusCircleIcon } from '../components/icons';
import MultiModalChatBar from '../components/MultiModalChatBar';
import ChatBubble from '../components/ui/ChatBubble';
import LoadingSpinner from '../components/ui/LoadingSpinner';

interface VMInstance {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'paused' | 'creating';
  cpuUsage: number;
  ramUsage: number;
  template: string;
}

const VMHubPage: React.FC = () => {
  const { chatHistory, isLoading: mamaBearLoading, sendUserMessage, currentVariant } = useMamaBear();
  const { theme } = useTheme();
  const [instances, setInstances] = useState<VMInstance[]>([
    { id: 'vm-1', name: 'Dev Server Alpha', status: 'running', cpuUsage: 35, ramUsage: 60, template: 'Ubuntu 22.04 LTS' },
    { id: 'vm-2', name: 'Python Scraper Bot', status: 'stopped', cpuUsage: 0, ramUsage: 0, template: 'Python 3.10 Flask' },
    { id: 'vm-3', name: 'NixOS Testbed', status: 'paused', cpuUsage: 5, ramUsage: 10, template: 'NixOS Custom' },
  ]);
  const [selectedInstance, setSelectedInstance] = useState<VMInstance | null>(instances[0]);
  const [isLoadingOp, setIsLoadingOp] = useState<{[key: string]: boolean}>({}); // For VM operations

  const handleCreateInstance = async () => {
    setIsLoadingOp(prev => ({...prev, create: true}));
    await sendUserMessage("Mama Bear, please create a new VM instance using the default template.");
    // Simulate instance creation
    setTimeout(() => {
      const newId = `vm-${instances.length + 1}`;
      const newInstance: VMInstance = {
        id: newId,
        name: `New Instance ${instances.length + 1}`,
        status: 'creating',
        cpuUsage: 0,
        ramUsage: 0,
        template: 'Default Template',
      };
      setInstances(prev => [...prev, newInstance]);
      setTimeout(() => {
        setInstances(prev => prev.map(inst => inst.id === newId ? {...inst, status: 'running', cpuUsage: 10, ramUsage: 20} : inst));
        setIsLoadingOp(prev => ({...prev, create: false}));
      }, 2000);
    }, 500);
  };
  
  const handleVMOperation = (instanceId: string, operation: 'start' | 'stop' | 'pause') => {
    setIsLoadingOp(prev => ({...prev, [instanceId]: true}));
    sendUserMessage(`Mama Bear, please ${operation} instance ${instanceId}.`);
    setTimeout(() => {
      setInstances(prev => prev.map(inst => {
        if (inst.id === instanceId) {
          let newStatus: VMInstance['status'] = inst.status;
          if (operation === 'start') newStatus = 'running';
          if (operation === 'stop') newStatus = 'stopped';
          if (operation === 'pause') newStatus = 'paused';
          return { ...inst, status: newStatus, cpuUsage: newStatus === 'running' ? 20:0, ramUsage: newStatus === 'running' ? 30:0 };
        }
        return inst;
      }));
      setIsLoadingOp(prev => ({...prev, [instanceId]: false}));
    }, 1500);
  };

  return (
    <div className="flex h-full">
      {/* Left Pane: Mama Bear Chat and Controls */}
      <div className="w-1/3 min-w-[350px] flex flex-col border-r dark:border-gray-700">
        <header className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20 flex justify-between items-center`}>
          <h1 className="text-xl font-semibold">{currentVariant}</h1>
        </header>
        <div className="flex-grow overflow-y-auto p-4 space-y-4" style={{ scrollbarWidth: 'thin' }}>
          {chatHistory.map((msg) => (
            <ChatBubble key={msg.id} message={msg} />
          ))}
          {mamaBearLoading && <div className="flex justify-center py-4"><LoadingSpinner text="Mama Bear is processing..." /></div>}
        </div>
        <MultiModalChatBar />
      </div>

      {/* Right Pane: VM Instance View */}
      <div className="flex-1 flex flex-col">
        <header className={`p-4 border-b ${theme.accent.replace('text-','border-')}/20 flex justify-between items-center bg-white/10 backdrop-blur-sm`}>
          <h2 className="text-lg font-semibold">Scrapybara Instances</h2>
          <Button onClick={handleCreateInstance} leftIcon={<PlusCircleIcon className="w-5 h-5"/>} size="sm" isLoading={isLoadingOp['create']}>
            New Instance
          </Button>
        </header>
        
        <div className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 overflow-y-auto" style={{ scrollbarWidth: 'thin' }}>
          {instances.map(instance => (
            <Card key={instance.id} className={`${selectedInstance?.id === instance.id ? `ring-2 ${theme.accent.replace('text-','ring-')}` : ''}`} interactive onClick={() => setSelectedInstance(instance)}>
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold truncate" title={instance.name}>{instance.name}</h3>
                <span className={`px-2 py-0.5 text-xs rounded-full
                  ${instance.status === 'running' ? 'bg-green-500/20 text-green-700 dark:text-green-400' : 
                    instance.status === 'stopped' ? 'bg-red-500/20 text-red-700 dark:text-red-400' :
                    instance.status === 'paused' ? 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-400' :
                    'bg-blue-500/20 text-blue-700 dark:text-blue-400'}`}>
                  {instance.status}
                </span>
              </div>
              <p className="text-xs opacity-70 mb-1">Template: {instance.template}</p>
              <div className="text-xs space-y-1 mb-3">
                <p>CPU: {instance.cpuUsage}% <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5"><div className={`h-1.5 rounded-full ${theme.accent.replace('text-','bg-')}`} style={{width: `${instance.cpuUsage}%`}}></div></div></p>
                <p>RAM: {instance.ramUsage}% <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5"><div className={`h-1.5 rounded-full ${theme.accent.replace('text-','bg-')}`} style={{width: `${instance.ramUsage}%`}}></div></div></p>
              </div>
              <div className="flex space-x-2">
                <Button size="sm" variant="ghost" onClick={() => handleVMOperation(instance.id, 'start')} disabled={instance.status === 'running' || isLoadingOp[instance.id]} leftIcon={<PlayIcon className="w-4 h-4"/>} />
                <Button size="sm" variant="ghost" onClick={() => handleVMOperation(instance.id, 'pause')} disabled={instance.status !== 'running' || isLoadingOp[instance.id]} leftIcon={<PauseIcon className="w-4 h-4"/>} />
                <Button size="sm" variant="ghost" onClick={() => handleVMOperation(instance.id, 'stop')} disabled={instance.status === 'stopped' || isLoadingOp[instance.id]} leftIcon={<StopIcon className="w-4 h-4"/>} />
              </div>
              {isLoadingOp[instance.id] && <div className="absolute inset-0 bg-white/50 dark:bg-black/50 flex items-center justify-center rounded-xl"><LoadingSpinner size="sm"/></div>}
            </Card>
          ))}
        </div>

        {selectedInstance && (
          <div className={`p-4 border-t ${theme.accent.replace('text-','border-')}/20 bg-white/5 backdrop-blur-sm`}>
            <h3 className="text-md font-semibold mb-2">{selectedInstance.name} - Details / Terminal (mock)</h3>
            <div className={`h-48 p-2 rounded ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/20 overflow-y-auto text-xs font-mono`} style={{ scrollbarWidth: 'thin' }}>
              <p>&gt; Connecting to {selectedInstance.name}...</p>
              <p>&gt; Authentication successful.</p>
              <p>&gt; Last login: {new Date().toLocaleString()}</p>
              <p className={`${theme.text}/70`}># This is a mock terminal output for {selectedInstance.name}.</p>
              <p className={`${theme.text}/70`}># Status: {selectedInstance.status}</p>
              <p className={`${theme.text}/70`}># Type 'help' for commands.</p>
              <p className={`${theme.accent}`}># _</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VMHubPage;