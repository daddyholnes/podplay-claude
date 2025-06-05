
import React, { useState } from 'react';
import { useTheme } from '../hooks/useTheme';
import { useMamaBear } from '../hooks/useMamaBear';
import { useToast } from '../hooks/useToast';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Modal from '../components/ui/Modal';
import { SquaresPlusIcon, MagnifyingGlassCircleIcon, ArrowDownTrayIcon, CodeBracketIcon } from '../components/icons';
import LoadingSpinner from '../components/ui/LoadingSpinner';

interface MCPTool {
  id: string;
  name: string;
  description: string;
  version: string;
  author: string;
  tags: string[];
  iconUrl?: string;
  source: 'GitHub' | 'DockerHub' | 'Custom';
  installed: boolean;
}

const mockMCPTools: MCPTool[] = [
  { id: 'mcp-1', name: 'Scrapybara Agent Controller', description: 'Advanced control an d orchestration for Scrapybara instances.', version: '1.2.0', author: 'Podplay Inc.', tags: ['scrapybara', 'automation', 'devops'], iconUrl: 'https://picsum.photos/seed/mcp1/64/64', source: 'GitHub', installed: true },
  { id: 'mcp-2', name: 'Mem0 Synapse', description: 'Enhanced memory management and RAG capabilities for Mem0.', version: '0.8.5', author: 'Memory Co.', tags: ['memory', 'rag', 'ai'], iconUrl: 'https://picsum.photos/seed/mcp2/64/64', source: 'Custom', installed: false },
  { id: 'mcp-3', name: 'Docker Vision Toolkit', description: 'Integrates computer vision models from Docker Hub.', version: '2.1.0', author: 'Visionaries', tags: ['docker', 'vision', 'ml'], iconUrl: 'https://picsum.photos/seed/mcp3/64/64', source: 'DockerHub', installed: false },
  { id: 'mcp-4', name: 'Gemini Function Weaver', description: 'Easily define and call Gemini functions.', version: '1.0.3', author: 'Google Fans', tags: ['gemini', 'functions', 'api'], iconUrl: 'https://picsum.photos/seed/mcp4/64/64', source: 'GitHub', installed: true },
  { id: 'mcp-5', name: 'Claude Opus Scribe', description: 'Advanced text generation and summarization with Claude.', version: '0.5.0', author: 'Anthropic Devs', tags: ['claude', 'nlp', 'text'], iconUrl: 'https://picsum.photos/seed/mcp5/64/64', source: 'Custom', installed: false },
];


const MCPMarketplacePage: React.FC = () => {
  const { theme } = useTheme();
  const { sendUserMessage, currentVariant } = useMamaBear();
  const { addToast } = useToast();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTool, setSelectedTool] = useState<MCPTool | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [tools, setTools] = useState<MCPTool[]>(mockMCPTools);
  const [installingToolId, setInstallingToolId] = useState<string | null>(null);

  const filteredTools = tools.filter(tool => 
    tool.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tool.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tool.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleViewDetails = (tool: MCPTool) => {
    setSelectedTool(tool);
    setIsModalOpen(true);
  };
  
  const handleInstall = async (tool: MCPTool) => {
    if (tool.installed) {
      addToast(`${tool.name} is already installed.`, 'info');
      return;
    }
    setInstallingToolId(tool.id);
    await sendUserMessage(`Mama Bear, please install MCP tool: ${tool.name} from ${tool.source}.`);
    // Simulate installation
    setTimeout(() => {
      setTools(prevTools => prevTools.map(t => t.id === tool.id ? {...t, installed: true} : t));
      addToast(`${tool.name} installed successfully!`, 'success');
      setInstallingToolId(null);
      if(selectedTool && selectedTool.id === tool.id) {
        setSelectedTool(prev => prev ? ({...prev, installed: true}) : null);
      }
    }, 2500);
  };

  return (
    <div className="p-6 flex flex-col h-full">
      <header className="mb-6">
        <h1 className={`text-3xl font-bold ${theme.accent} flex items-center`}>
          <SquaresPlusIcon className="w-8 h-8 mr-2" /> MCP Marketplace - Tool Discovery
        </h1>
        <p className={`${theme.text}/70`}>Browse, install, and manage Model Context Protocol (MCP) servers. Current Mama Bear: {currentVariant}</p>
      </header>

      <div className="mb-6 flex items-center space-x-4">
        <Input 
          placeholder="Search tools by name, description, or tag..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          icon={<MagnifyingGlassCircleIcon className="w-5 h-5"/>}
          className="flex-grow"
        />
        {/* Add filters for source, installed status etc. later */}
      </div>

      {filteredTools.length === 0 && (
        <div className="flex-grow flex flex-col items-center justify-center text-center p-6">
          <MagnifyingGlassCircleIcon className={`w-16 h-16 ${theme.text}/30 mb-4`} />
          <h3 className="text-xl font-semibold mb-2">No Tools Found</h3>
          <p className={`${theme.text}/60`}>Try adjusting your search term or filters.</p>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 overflow-y-auto flex-grow" style={{ scrollbarWidth: 'thin' }}>
        {filteredTools.map(tool => (
          <Card key={tool.id} className="flex flex-col" interactive>
            <div className="flex items-center mb-3">
              <img src={tool.iconUrl || `https://picsum.photos/seed/${tool.id}/64/64`} alt={tool.name} className="w-12 h-12 rounded-lg mr-3" />
              <div>
                <h3 className="text-lg font-semibold truncate" title={tool.name}>{tool.name}</h3>
                <p className="text-xs opacity-70">{tool.author} - v{tool.version}</p>
              </div>
            </div>
            <p className="text-sm opacity-80 mb-3 h-16 overflow-hidden text-ellipsis">{tool.description}</p>
            <div className="flex flex-wrap gap-1 mb-3">
              {tool.tags.slice(0,3).map(tag => <span key={tag} className={`px-2 py-0.5 text-xs rounded-full ${theme.accent.replace('text-','bg-')}/20 ${theme.accent}`}>{tag}</span>)}
            </div>
            <div className="mt-auto flex space-x-2">
              <Button variant="secondary" size="sm" onClick={() => handleViewDetails(tool)} className="flex-1">Details</Button>
              <Button 
                size="sm" 
                onClick={() => handleInstall(tool)} 
                disabled={tool.installed || installingToolId === tool.id} 
                isLoading={installingToolId === tool.id}
                leftIcon={<ArrowDownTrayIcon className="w-4 h-4"/>}
                className="flex-1"
              >
                {tool.installed ? 'Installed' : (installingToolId === tool.id ? 'Installing...' : 'Install')}
              </Button>
            </div>
             {installingToolId === tool.id && <div className="absolute inset-0 bg-white/30 dark:bg-black/30 flex items-center justify-center rounded-xl"><LoadingSpinner size="sm"/></div>}
          </Card>
        ))}
      </div>

      {selectedTool && (
        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={selectedTool.name} size="lg">
          <div className="flex items-start space-x-4">
            <img src={selectedTool.iconUrl || `https://picsum.photos/seed/${selectedTool.id}/128/128`} alt={selectedTool.name} className="w-24 h-24 rounded-lg" />
            <div>
              <p className="text-sm opacity-80 mb-1">Author: {selectedTool.author} | Version: {selectedTool.version}</p>
              <p className="text-sm opacity-80 mb-3">Source: {selectedTool.source}</p>
              <div className="flex flex-wrap gap-2 mb-3">
                {selectedTool.tags.map(tag => <span key={tag} className={`px-2 py-1 text-xs rounded-full ${theme.accent.replace('text-','bg-')}/20 ${theme.accent}`}>{tag}</span>)}
              </div>
            </div>
          </div>
          <p className="my-4">{selectedTool.description}</p>
          
          <h4 className="font-semibold mb-2 mt-4">Installation Details (Mock)</h4>
          <div className={`p-3 rounded ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/20 text-xs font-mono`}>
            <p>MCP Server URL: https://mcp.example.com/{selectedTool.id}</p>
            <p>Protocol Version: 1.1</p>
            <p>Requires: Docker (if applicable), API Keys (if applicable)</p>
          </div>

          <div className="mt-6 flex justify-end space-x-3">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Close</Button>
            <Button 
              onClick={() => { handleInstall(selectedTool); if (!selectedTool.installed) setIsModalOpen(false); }} 
              disabled={selectedTool.installed || installingToolId === selectedTool.id} 
              isLoading={installingToolId === selectedTool.id}
              leftIcon={<ArrowDownTrayIcon className="w-5 h-5"/>}
            >
              {selectedTool.installed ? 'Already Installed' : (installingToolId === selectedTool.id ? 'Installing...' : 'Install Tool')}
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default MCPMarketplacePage;