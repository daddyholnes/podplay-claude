import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Monitor, 
  Play, 
  Pause, 
  Square, 
  Terminal, 
  Globe, 
  Settings,
  Cpu,
  HardDrive,
  Wifi,
  Clock
} from 'lucide-react';

interface ScrapybaraInstance {
  id: string;
  name: string;
  type: 'ubuntu' | 'browser' | 'windows';
  status: 'running' | 'paused' | 'stopped';
  uptime: number;
  cpu: number;
  memory: number;
  storage: number;
  lastActivity: Date;
  cdpUrl?: string;
}

interface InstanceMetrics {
  cpu: number;
  memory: number;
  network: number;
  storage: number;
}

const ScrapybaraHub: React.FC = () => {
  const [instances, setInstances] = useState<ScrapybaraInstance[]>([]);
  const [selectedInstance, setSelectedInstance] = useState<ScrapybaraInstance | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [metrics, setMetrics] = useState<Record<string, InstanceMetrics>>({});
  const [terminalVisible, setTerminalVisible] = useState(false);

  // Mock data for development
  useEffect(() => {
    const mockInstances: ScrapybaraInstance[] = [
      {
        id: 'ubuntu-1',
        name: 'Development Ubuntu',
        type: 'ubuntu',
        status: 'running',
        uptime: 3600,
        cpu: 45,
        memory: 62,
        storage: 78,
        lastActivity: new Date(Date.now() - 300000),
      },
      {
        id: 'browser-1',
        name: 'Research Browser',
        type: 'browser',
        status: 'paused',
        uptime: 1800,
        cpu: 12,
        memory: 34,
        storage: 45,
        lastActivity: new Date(Date.now() - 900000),
        cdpUrl: 'ws://localhost:9222'
      }
    ];
    setInstances(mockInstances);
    setSelectedInstance(mockInstances[0]);

    // Mock metrics
    const mockMetrics: Record<string, InstanceMetrics> = {};
    mockInstances.forEach(instance => {
      mockMetrics[instance.id] = {
        cpu: Math.random() * 100,
        memory: Math.random() * 100,
        network: Math.random() * 50,
        storage: instance.storage
      };
    });
    setMetrics(mockMetrics);
  }, []);

  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-green-500';
      case 'paused': return 'text-yellow-500';
      case 'stopped': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'ubuntu': return <Terminal className="w-5 h-5" />;
      case 'browser': return <Globe className="w-5 h-5" />;
      case 'windows': return <Monitor className="w-5 h-5" />;
      default: return <Monitor className="w-5 h-5" />;
    }
  };

  const handleAction = async (instanceId: string, action: 'start' | 'pause' | 'stop') => {
    // TODO: Connect to backend Scrapybara API
    console.log(`${action} instance ${instanceId}`);
    
    setInstances(prev => prev.map(instance => 
      instance.id === instanceId 
        ? { ...instance, status: action === 'start' ? 'running' : action as any }
        : instance
    ));
  };

  const createNewInstance = async (type: 'ubuntu' | 'browser' | 'windows') => {
    setIsCreating(true);
    
    // TODO: Connect to backend to create new instance
    setTimeout(() => {
      const newInstance: ScrapybaraInstance = {
        id: `${type}-${Date.now()}`,
        name: `New ${type.charAt(0).toUpperCase() + type.slice(1)} Instance`,
        type,
        status: 'running',
        uptime: 0,
        cpu: 0,
        memory: 0,
        storage: 0,
        lastActivity: new Date(),
      };
      
      setInstances(prev => [...prev, newInstance]);
      setSelectedInstance(newInstance);
      setIsCreating(false);
    }, 2000);
  };

  return (
    <div className="h-full bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex">
      {/* Left Sidebar - Instance List */}
      <motion.div 
        className="w-80 bg-white/70 backdrop-blur-xl border-r border-slate-200/50 overflow-y-auto"
        initial={{ x: -320 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <div className="p-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                🖥️ Scrapybara Hub
              </h2>
              <p className="text-sm text-gray-600">Remote Desktop Control</p>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-3 gap-2 mb-6">
            <motion.button
              onClick={() => createNewInstance('ubuntu')}
              className="p-3 rounded-lg bg-orange-100/50 text-orange-600 hover:bg-orange-200/50 transition-colors text-center"
              whileHover={{ scale: 1.05 }}
              disabled={isCreating}
            >
              <Terminal className="w-5 h-5 mx-auto mb-1" />
              <span className="text-xs">Ubuntu</span>
            </motion.button>
            <motion.button
              onClick={() => createNewInstance('browser')}
              className="p-3 rounded-lg bg-blue-100/50 text-blue-600 hover:bg-blue-200/50 transition-colors text-center"
              whileHover={{ scale: 1.05 }}
              disabled={isCreating}
            >
              <Globe className="w-5 h-5 mx-auto mb-1" />
              <span className="text-xs">Browser</span>
            </motion.button>
            <motion.button
              onClick={() => createNewInstance('windows')}
              className="p-3 rounded-lg bg-purple-100/50 text-purple-600 hover:bg-purple-200/50 transition-colors text-center"
              whileHover={{ scale: 1.05 }}
              disabled={isCreating}
            >
              <Monitor className="w-5 h-5 mx-auto mb-1" />
              <span className="text-xs">Windows</span>
            </motion.button>
          </div>

          {/* Instances List */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Active Instances</h3>
            {instances.map((instance) => (
              <motion.div
                key={instance.id}
                className={`p-4 rounded-lg border cursor-pointer transition-all ${
                  selectedInstance?.id === instance.id
                    ? 'bg-blue-100/50 border-blue-300 ring-2 ring-blue-200'
                    : 'bg-white/50 border-slate-200 hover:bg-slate-50/50'
                }`}
                whileHover={{ scale: 1.02 }}
                onClick={() => setSelectedInstance(instance)}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {getTypeIcon(instance.type)}
                    <span className="font-medium text-gray-800">{instance.name}</span>
                  </div>
                  <div className={`text-xs font-medium ${getStatusColor(instance.status)}`}>
                    {instance.status}
                  </div>
                </div>
                
                <div className="text-xs text-gray-600 space-y-1">
                  <div className="flex justify-between">
                    <span>CPU:</span>
                    <span>{instance.cpu}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Memory:</span>
                    <span>{instance.memory}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Uptime:</span>
                    <span>{formatUptime(instance.uptime)}</span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-1 mt-3">
                  {instance.status === 'stopped' && (
                    <button
                      onClick={(e) => { e.stopPropagation(); handleAction(instance.id, 'start'); }}
                      className="flex-1 p-1 rounded bg-green-100 text-green-600 hover:bg-green-200 transition-colors"
                    >
                      <Play className="w-3 h-3 mx-auto" />
                    </button>
                  )}
                  {instance.status === 'running' && (
                    <button
                      onClick={(e) => { e.stopPropagation(); handleAction(instance.id, 'pause'); }}
                      className="flex-1 p-1 rounded bg-yellow-100 text-yellow-600 hover:bg-yellow-200 transition-colors"
                    >
                      <Pause className="w-3 h-3 mx-auto" />
                    </button>
                  )}
                  {instance.status === 'paused' && (
                    <button
                      onClick={(e) => { e.stopPropagation(); handleAction(instance.id, 'start'); }}
                      className="flex-1 p-1 rounded bg-green-100 text-green-600 hover:bg-green-200 transition-colors"
                    >
                      <Play className="w-3 h-3 mx-auto" />
                    </button>
                  )}
                  <button
                    onClick={(e) => { e.stopPropagation(); handleAction(instance.id, 'stop'); }}
                    className="flex-1 p-1 rounded bg-red-100 text-red-600 hover:bg-red-200 transition-colors"
                  >
                    <Square className="w-3 h-3 mx-auto" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {isCreating && (
            <motion.div
              className="mt-4 p-4 bg-blue-100/50 rounded-lg border border-blue-200"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center space-x-2">
                <motion.div
                  className="w-4 h-4 bg-blue-500 rounded-full"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1, repeat: Infinity }}
                />
                <span className="text-sm text-blue-700">Creating new instance...</span>
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {selectedInstance ? (
          <>
            {/* Instance Header */}
            <motion.div 
              className="bg-white/70 backdrop-blur-xl border-b border-slate-200/50 p-6"
              initial={{ y: -60 }}
              animate={{ y: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="p-3 rounded-lg bg-blue-100/50 text-blue-600">
                    {getTypeIcon(selectedInstance.type)}
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold text-gray-800">{selectedInstance.name}</h1>
                    <p className="text-gray-600 capitalize">{selectedInstance.type} Instance</p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                    selectedInstance.status === 'running' ? 'bg-green-100 text-green-700' :
                    selectedInstance.status === 'paused' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {selectedInstance.status}
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <motion.button
                    onClick={() => setTerminalVisible(!terminalVisible)}
                    className="p-2 rounded-lg bg-slate-100/50 text-slate-600 hover:bg-slate-200/50 transition-colors"
                    whileHover={{ scale: 1.1 }}
                  >
                    <Terminal className="w-5 h-5" />
                  </motion.button>
                  <motion.button
                    className="p-2 rounded-lg bg-slate-100/50 text-slate-600 hover:bg-slate-200/50 transition-colors"
                    whileHover={{ scale: 1.1 }}
                  >
                    <Settings className="w-5 h-5" />
                  </motion.button>
                </div>
              </div>
            </motion.div>

            {/* Metrics Dashboard */}
            <div className="p-6 bg-white/30 border-b border-slate-200/50">
              <div className="grid grid-cols-4 gap-6">
                <div className="bg-white/50 backdrop-blur-sm rounded-lg p-4 border border-slate-200/50">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">CPU Usage</span>
                    <Cpu className="w-4 h-4 text-blue-500" />
                  </div>
                  <div className="text-2xl font-bold text-gray-800">{selectedInstance.cpu}%</div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                    <div 
                      className="bg-blue-500 h-1.5 rounded-full transition-all duration-300" 
                      style={{ width: `${selectedInstance.cpu}%` }}
                    />
                  </div>
                </div>

                <div className="bg-white/50 backdrop-blur-sm rounded-lg p-4 border border-slate-200/50">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Memory</span>
                    <HardDrive className="w-4 h-4 text-green-500" />
                  </div>
                  <div className="text-2xl font-bold text-gray-800">{selectedInstance.memory}%</div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                    <div 
                      className="bg-green-500 h-1.5 rounded-full transition-all duration-300" 
                      style={{ width: `${selectedInstance.memory}%` }}
                    />
                  </div>
                </div>

                <div className="bg-white/50 backdrop-blur-sm rounded-lg p-4 border border-slate-200/50">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Network</span>
                    <Wifi className="w-4 h-4 text-purple-500" />
                  </div>
                  <div className="text-2xl font-bold text-gray-800">
                    {metrics[selectedInstance.id]?.network.toFixed(1) || '0.0'} MB/s
                  </div>
                  <div className="text-xs text-gray-500 mt-1">Incoming</div>
                </div>

                <div className="bg-white/50 backdrop-blur-sm rounded-lg p-4 border border-slate-200/50">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Uptime</span>
                    <Clock className="w-4 h-4 text-orange-500" />
                  </div>
                  <div className="text-2xl font-bold text-gray-800">{formatUptime(selectedInstance.uptime)}</div>
                  <div className="text-xs text-gray-500 mt-1">Active session</div>
                </div>
              </div>
            </div>

            {/* Main Display Area */}
            <div className="flex-1 flex">
              {/* Desktop/Browser Preview */}
              <div className="flex-1 bg-black/10 flex items-center justify-center">
                <motion.div
                  className="w-full h-full max-w-6xl max-h-4xl bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 flex items-center justify-center"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <div className="text-center space-y-4">
                    <Monitor className="w-24 h-24 mx-auto text-slate-400" />
                    <div>
                      <h3 className="text-xl font-bold text-slate-700 mb-2">Remote Desktop Preview</h3>
                      <p className="text-slate-600 mb-4">
                        {selectedInstance.status === 'running' 
                          ? 'Live desktop streaming will appear here'
                          : `Instance is ${selectedInstance.status}. Start it to view desktop.`
                        }
                      </p>
                      {selectedInstance.status === 'stopped' && (
                        <motion.button
                          onClick={() => handleAction(selectedInstance.id, 'start')}
                          className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                          whileHover={{ scale: 1.05 }}
                        >
                          <Play className="w-4 h-4 inline mr-2" />
                          Start Instance
                        </motion.button>
                      )}
                    </div>
                  </div>
                </motion.div>
              </div>

              {/* Terminal Panel */}
              <AnimatePresence>
                {terminalVisible && (
                  <motion.div
                    className="w-96 bg-gray-900/90 backdrop-blur-xl border-l border-gray-700/50"
                    initial={{ x: 400 }}
                    animate={{ x: 0 }}
                    exit={{ x: 400 }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                  >
                    <div className="p-4 border-b border-gray-700/50">
                      <div className="flex items-center justify-between">
                        <h3 className="text-white font-medium">Terminal</h3>
                        <button
                          onClick={() => setTerminalVisible(false)}
                          className="text-gray-400 hover:text-white"
                        >
                          ×
                        </button>
                      </div>
                    </div>
                    <div className="h-full bg-black/50 p-4 font-mono text-sm text-green-400">
                      <div className="mb-2">woody@{selectedInstance.type}-instance:~$ </div>
                      <div className="text-gray-400 mb-2"># Terminal connected to {selectedInstance.name}</div>
                      <div className="text-gray-400 mb-2"># Type commands to interact with the remote instance</div>
                      <div className="flex items-center">
                        <span className="text-green-400">$ </span>
                        <div className="w-2 h-4 bg-green-400 ml-1 animate-pulse"></div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center space-y-4">
              <Monitor className="w-24 h-24 mx-auto text-slate-400" />
              <div>
                <h3 className="text-xl font-bold text-slate-700 mb-2">Select an Instance</h3>
                <p className="text-slate-600">Choose a Scrapybara instance from the sidebar to manage</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScrapybaraHub;
