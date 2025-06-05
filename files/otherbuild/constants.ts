
import { Themes, ThemeName, PageInfo, MamaBearVariantName, PageContext, MiniApp, GeminiModel } from './types';
import { HomeIcon, CpuChipIcon, MagnifyingGlassCircleIcon, ChatBubbleLeftRightIcon, SquaresPlusIcon, PuzzlePieceIcon, MicrophoneIcon, PlayCircleIcon, ServerStackIcon } from './components/icons'; // Assuming icons are in components/icons

export const APP_NAME = "Podplay Sanctuary";

export const THEMES: Themes = {
  [ThemeName.LIGHT]: {
    name: 'Sky Sanctuary',
    className: 'theme-light',
    background: 'bg-gradient-to-br from-sky-start to-sky-end',
    text: 'text-sky-text',
    accent: 'text-sky-accent',
    chatBubbleBg: 'bg-white',
    chatBubbleText: 'text-sky-text',
    animations: { clouds: true },
  },
  [ThemeName.PURPLE]: {
    name: 'Neon Sanctuary',
    className: 'theme-purple',
    background: 'bg-gradient-to-br from-neon-purple-start via-neon-pink-via to-neon-blue-end',
    text: 'text-neon-text',
    accent: 'text-neon-accent',
    interactiveNeon: 'shadow-neon-purple',
    chatBubbleBg: 'bg-purple-900/70 backdrop-blur-sm border border-silver-accent',
    chatBubbleText: 'text-neon-text',
    animations: { particles: true },
  },
  [ThemeName.DARK]: {
    name: 'Stellar Sanctuary',
    className: 'theme-dark',
    background: 'bg-stellar-bg',
    text: 'text-stellar-text',
    accent: 'text-stellar-accent-purple',
    secondaryAccent: 'text-stellar-accent-gold',
    chatBubbleBg: 'bg-gray-800 border border-gray-700',
    chatBubbleText: 'text-stellar-text',
    animations: { stars: true },
  },
};

export const DEFAULT_THEME: ThemeName = ThemeName.LIGHT;

export const PAGES: PageInfo[] = [
  { path: '/', name: 'Mama Bear Central', icon: HomeIcon, mamaBearVariant: MamaBearVariantName.RESEARCH_SPECIALIST, pageContext: 'main_chat' },
  { path: '/vm-hub', name: 'Scrapybara Command', icon: CpuChipIcon, mamaBearVariant: MamaBearVariantName.DEVOPS_SPECIALIST, pageContext: 'vm_hub' },
  { path: '/scout', name: 'Autonomous Explorer', icon: MagnifyingGlassCircleIcon, mamaBearVariant: MamaBearVariantName.SCOUT_COMMANDER, pageContext: 'scout' },
  { path: '/multi-modal-chat', name: 'Model Symposium', icon: ChatBubbleLeftRightIcon, mamaBearVariant: MamaBearVariantName.MODEL_COORDINATOR, pageContext: 'multi_modal_chat' },
  { path: '/mcp-marketplace', name: 'MCP Marketplace', icon: SquaresPlusIcon, mamaBearVariant: MamaBearVariantName.TOOL_CURATOR, pageContext: 'mcp_marketplace' },
  { path: '/integrations', name: 'Integration Workbench', icon: PuzzlePieceIcon, mamaBearVariant: MamaBearVariantName.INTEGRATION_ARCHITECT, pageContext: 'integration_workbench' },
  { path: '/live-api-studio', name: 'Live API Studio', icon: MicrophoneIcon, mamaBearVariant: MamaBearVariantName.LIVE_API_SPECIALIST, pageContext: 'live_api_studio' },
  { path: '/mini-apps', name: 'Mini Apps', icon: PlayCircleIcon, mamaBearVariant: MamaBearVariantName.DEFAULT, pageContext: 'mini_apps' },
];

export const MAMA_BEAR_VARIANTS: { [key in PageContext]: MamaBearVariantName } = {
  main_chat: MamaBearVariantName.RESEARCH_SPECIALIST,
  vm_hub: MamaBearVariantName.DEVOPS_SPECIALIST,
  scout: MamaBearVariantName.SCOUT_COMMANDER,
  multi_modal_chat: MamaBearVariantName.MODEL_COORDINATOR,
  mcp_marketplace: MamaBearVariantName.TOOL_CURATOR,
  integration_workbench: MamaBearVariantName.INTEGRATION_ARCHITECT,
  live_api_studio: MamaBearVariantName.LIVE_API_SPECIALIST,
  mini_apps: MamaBearVariantName.DEFAULT,
};

export const MINI_APPS_LIST: MiniApp[] = [
  { id: 'scout', name: 'Scout.new', logoUrl: 'https://scout.new/favicon.ico', appUrl: 'https://scout.new/', description: 'Autonomous AI agent platform.' },
  { id: 'notebooklm', name: 'NotebookLM', logoUrl: 'https://notebooklm.google.com/favicon.ico', appUrl: 'https://notebooklm.google/', description: 'AI-powered research assistant.' },
  { id: 'grok', name: 'Grok', logoUrl: 'https://grok.x.ai/favicon.ico', appUrl: 'https://grok.x.ai/', description: 'AI by xAI.' },
  { id: 'chatgpt', name: 'ChatGPT', logoUrl: 'https://chat.openai.com/favicon.ico', appUrl: 'https://chat.openai.com/', description: 'OpenAI\'s ChatGPT.' },
  { id: 'jules', name: 'Jules.Google', logoUrl: 'https://jules.google.com/favicon.ico', appUrl: 'https://jules.google.com', description: 'Google\'s experimental AI.' },
  { id: 'aistudio', name: 'AI Studio', logoUrl: 'https://aistudio.google.com/favicon.ico', appUrl: 'https://aistudio.google.com/prompts/new_chat?lfhs=2', description: 'Google AI Studio.' },
  { id: 'perplexity', name: 'Perplexity AI', logoUrl: 'https://www.perplexity.ai/favicon.ico', appUrl: 'https://www.perplexity.ai/', description: 'Conversational search engine.' },
  { id: 'github', name: 'GitHub', logoUrl: 'https://github.githubassets.com/favicons/favicon.svg', appUrl: 'https://github.com/', description: 'Code hosting platform.' },
  { id: 'firebase', name: 'Firebase Studio', logoUrl: 'https://firebase.google.com/favicon.ico', appUrl: 'https://console.firebase.google.com/', description: 'Firebase console.' },
  { id: 'mem0', name: 'Mem0.ai', logoUrl: 'https://mem0.ai/favicon.ico', appUrl: 'https://mem0.ai/', description: 'Persistent memory service.' },
  { id: 'claude', name: 'Claude AI', logoUrl: 'https://claude.ai/favicon.ico', appUrl: 'https://claude.ai/', description: 'Anthropic\'s Claude.' },
  { id: 'gcp', name: 'Google Cloud', logoUrl: 'https://cloud.google.com/favicon.ico', appUrl: 'https://console.cloud.google.com/', description: 'Google Cloud Platform.' },
  { id: 'gemini', name: 'Gemini', logoUrl: 'https://gemini.google.com/favicon.ico', appUrl: 'https://gemini.google.com/', description: 'Google\'s Gemini.' },
];

export const LIVE_API_GEMINI_MODELS: GeminiModel[] = [
  { id: 'gemini-2.5-flash-preview-native-audio-dialog', name: 'Gemini 2.5 Flash (Native Audio Dialog)' },
  { id: 'gemini-2.5-flash-exp-native-audio-thinking-dialog', name: 'Gemini 2.5 Flash Exp (Native Audio Thinking Dialog)' },
  { id: 'gemini-2.0-flash-live-001', name: 'Gemini 2.0 Flash Live' },
  // For general text tasks, if needed elsewhere, not necessarily for Live API studio directly but good to have:
  { id: 'gemini-2.5-flash-preview-04-17', name: 'Gemini 2.5 Flash Preview (Text)' },
];

export const AI_MODELS_FOR_MULTIMODAL_CHAT: { id: string, name: string, provider: string }[] = [
  { id: 'gemini-2.5-flash-preview-04-17', name: 'Gemini 2.5 Flash', provider: 'Google' },
  { id: 'gemini-2.0-pro', name: 'Gemini 2.0 Pro (mock)', provider: 'Google' }, // Example, actual model might vary
  { id: 'claude-3-opus', name: 'Claude 3 Opus (mock)', provider: 'Anthropic' },
  { id: 'gpt-4o', name: 'GPT-4o (mock)', provider: 'OpenAI' },
];

export const LOCAL_STORAGE_THEME_KEY = 'podplaySanctuaryTheme';
export const LOCAL_STORAGE_USER_ID_KEY = 'podplaySanctuaryUserId';