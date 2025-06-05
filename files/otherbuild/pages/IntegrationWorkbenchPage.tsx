
import React, { useState } from 'react';
import { useTheme } from '../hooks/useTheme';
import { useMamaBear } from '../hooks/useMamaBear';
import { useToast } from '../hooks/useToast';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Modal from '../components/ui/Modal';
import { PuzzlePieceIcon, PlusCircleIcon, CodeBracketIcon, EyeIcon, EyeSlashIcon } from '../components/icons';

interface ServiceConnector {
  id: string;
  name: string;
  logoUrl: string;
  description: string;
  category: string;
}

interface WorkflowStep {
  id: string;
  serviceId: string;
  action: string;
  config: Record<string, any>;
}

interface Integration {
  id: string;
  name: string;
  trigger: WorkflowStep;
  actions: WorkflowStep[];
  enabled: boolean;
}

const mockConnectors: ServiceConnector[] = [
  { id: 'zapier', name: 'Zapier', logoUrl: 'https://picsum.photos/seed/zapier/64/64', description: 'Automate workflows by connecting your apps.', category: 'Automation' },
  { id: 'edenai', name: 'Eden AI', logoUrl: 'https://picsum.photos/seed/edenai/64/64', description: 'Access multiple AI providers through a single API.', category: 'AI Gateway' },
  { id: 'n8n', name: 'N8N', logoUrl: 'https://picsum.photos/seed/n8n/64/64', description: 'Extendable workflow automation tool.', category: 'Automation' },
  { id: 'vertexai', name: 'Vertex AI', logoUrl: 'https://picsum.photos/seed/vertexai/64/64', description: 'Build, deploy, and scale ML models.', category: 'ML Platform' },
  { id: 'github', name: 'GitHub', logoUrl: 'https://picsum.photos/seed/github2/64/64', description: 'Code hosting and collaboration.', category: 'Development' },
  { id: 'slack', name: 'Slack', logoUrl: 'https://picsum.photos/seed/slack/64/64', description: 'Team communication platform.', category: 'Communication' },
];

const IntegrationWorkbenchPage: React.FC = () => {
  const { theme } = useTheme();
  const { sendUserMessage, currentVariant } = useMamaBear();
  const { addToast } = useToast();
  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [showSecretModal, setShowSecretModal] = useState(false);
  const [secretName, setSecretName] = useState('');
  const [secretValue, setSecretValue] = useState('');
  const [showSecretValue, setShowSecretValue] = useState(false);

  const handleCreateIntegration = () => {
    sendUserMessage("Mama Bear, let's create a new integration.");
    addToast('Visual workflow builder coming soon! For now, imagine a new integration card appearing.', 'info');
    // Mock: Add a placeholder integration
    const newIntegration: Integration = {
      id: `int-${Date.now()}`,
      name: `New Integration ${integrations.length + 1}`,
      trigger: {id: 't1', serviceId: 'mock', action: 'New Email', config: {}},
      actions: [{id: 'a1', serviceId: 'mock', action: 'Post to Slack', config: {}}],
      enabled: false,
    };
    setIntegrations(prev => [...prev, newIntegration]);
  };

  const handleSaveSecret = () => {
    if (!secretName.trim() || !secretValue.trim()) {
      addToast('Secret name and value cannot be empty.', 'error');
      return;
    }
    sendUserMessage(`Mama Bear, please save a secret named "${secretName}".`);
    addToast(`Secret "${secretName}" saved (mocked). Mama Bear is guiding you securely!`, 'success');
    setSecretName('');
    setSecretValue('');
    setShowSecretModal(false);
  };

  return (
    <div className="p-6 flex flex-col h-full">
      <header className="mb-6">
        <h1 className={`text-3xl font-bold ${theme.accent} flex items-center`}>
          <PuzzlePieceIcon className="w-8 h-8 mr-2" /> Integration Workbench
        </h1>
        <p className={`${theme.text}/70`}>Create and manage connections with external services. Mama Bear ({currentVariant}) is here to help.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 flex-grow">
        {/* Workflow Builder / Integrations List */}
        <div className="md:col-span-2 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">My Integrations</h2>
            <Button onClick={handleCreateIntegration} leftIcon={<PlusCircleIcon className="w-5 h-5"/>}>New Integration</Button>
          </div>
          {integrations.length === 0 && (
            <Card className="flex-grow flex items-center justify-center">
              <div className="text-center">
                <PuzzlePieceIcon className={`w-16 h-16 ${theme.text}/30 mb-4`} />
                <p className={`${theme.text}/60`}>No integrations yet. Click "New Integration" to start.</p>
                <p className="text-xs mt-2 opacity-50">(Visual workflow builder is a complex feature - this is a placeholder)</p>
              </div>
            </Card>
          )}
          <div className="space-y-4 overflow-y-auto" style={{ scrollbarWidth: 'thin' }}>
            {integrations.map(intg => (
                <Card key={intg.id}>
                    <div className="flex justify-between items-center">
                        <h3 className="font-semibold">{intg.name}</h3>
                        <label className="inline-flex items-center cursor-pointer">
                            <input type="checkbox" checked={intg.enabled} onChange={() => setIntegrations(prev => prev.map(i => i.id === intg.id ? {...i, enabled: !i.enabled} : i))} className="sr-only peer" />
                            <div className={`relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:${theme.accent.replace('text-','ring-')}/50 dark:bg-gray-700 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:${theme.accent.replace('text-','bg-')}`}></div>
                        </label>
                    </div>
                    <p className="text-xs opacity-70 mt-1">Trigger: {intg.trigger.action} ({intg.trigger.serviceId})</p>
                    <p className="text-xs opacity-70">Actions: {intg.actions.map(a => `${a.action} (${a.serviceId})`).join(', ')}</p>
                </Card>
            ))}
          </div>
        </div>

        {/* Service Connectors & Secrets */}
        <div className="flex flex-col space-y-6">
          <Card>
            <h2 className="text-xl font-semibold mb-3">Service Connectors</h2>
            <div className="max-h-60 overflow-y-auto space-y-2 pr-2" style={{ scrollbarWidth: 'thin' }}>
              {mockConnectors.map(connector => (
                <div key={connector.id} className={`p-2 rounded-md flex items-center hover:${theme.accent.replace('text-','bg-')}/10 cursor-pointer`}>
                  <img src={connector.logoUrl} alt={connector.name} className="w-8 h-8 rounded mr-3" />
                  <div>
                    <h4 className="font-medium text-sm">{connector.name}</h4>
                    <p className="text-xs opacity-70">{connector.category}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
          <Card>
            <h2 className="text-xl font-semibold mb-3">Secrets Management</h2>
            <p className="text-sm opacity-70 mb-3">Mama Bear will guide you in securely managing API keys and credentials.</p>
            <Button onClick={() => setShowSecretModal(true)} className="w-full" variant="secondary">Manage Secrets</Button>
          </Card>
          <Card>
            <h2 className="text-xl font-semibold mb-3">Testing Playground</h2>
             <div className="h-32 flex items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-md">
                <p className="text-sm opacity-60 italic">Integration testing area (mock)</p>
            </div>
          </Card>
        </div>
      </div>

      {/* Secrets Modal */}
      <Modal isOpen={showSecretModal} onClose={() => setShowSecretModal(false)} title="Manage Secrets">
        <p className="text-sm opacity-80 mb-4">Add a new secret. Mama Bear ensures it's handled securely (mocked).</p>
        <div className="space-y-4">
          <Input 
            label="Secret Name (e.g., GITHUB_API_KEY)" 
            value={secretName} 
            onChange={(e) => setSecretName(e.target.value)} 
            placeholder="MY_SERVICE_TOKEN"
          />
          <div className="relative">
            <Input 
              label="Secret Value" 
              type={showSecretValue ? 'text' : 'password'}
              value={secretValue} 
              onChange={(e) => setSecretValue(e.target.value)} 
              placeholder="Enter secret value"
            />
            <button 
              onClick={() => setShowSecretValue(!showSecretValue)} 
              className="absolute right-3 top-9 p-1 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              title={showSecretValue ? "Hide secret" : "Show secret"}
            >
              {showSecretValue ? <EyeSlashIcon className="w-5 h-5"/> : <EyeIcon className="w-5 h-5"/>}
            </button>
          </div>
          <Button onClick={handleSaveSecret} className="w-full">Save Secret</Button>
        </div>
        <div className="mt-6 border-t pt-4">
          <h4 className="font-semibold mb-2">Stored Secrets (mock)</h4>
          <ul className="text-sm space-y-1 list-disc list-inside opacity-70">
            <li>OPENAI_API_KEY</li>
            <li>SCRAPYBARA_TOKEN</li>
          </ul>
        </div>
      </Modal>
    </div>
  );
};

export default IntegrationWorkbenchPage;