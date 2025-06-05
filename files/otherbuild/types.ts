
export enum ThemeName {
  LIGHT = 'light',
  PURPLE = 'purple',
  DARK = 'dark',
}

export interface Theme {
  name: string;
  className: string; // Root class for theme application
  background: string;
  text: string;
  accent: string;
  secondaryAccent?: string;
  chatBubbleBg: string;
  chatBubbleText: string;
  interactiveNeon?: string; // For neon outlines/shadows
  animations: {
    clouds?: boolean;
    particles?: boolean;
    stars?: boolean;
  };
}

export type Themes = {
  [key in ThemeName]: Theme;
};

export enum MamaBearVariantName {
  RESEARCH_SPECIALIST = 'Research Specialist',
  DEVOPS_SPECIALIST = 'DevOps Specialist',
  SCOUT_COMMANDER = 'Scout Commander',
  MODEL_COORDINATOR = 'Model Coordinator',
  TOOL_CURATOR = 'Tool Curator',
  INTEGRATION_ARCHITECT = 'Integration Architect',
  LIVE_API_SPECIALIST = 'Live API Specialist',
  DEFAULT = 'Mama Bear',
}

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'mama_bear' | 'system';
  timestamp: string;
  avatar?: string; // URL or identifier
  variant?: MamaBearVariantName;
  attachments?: File[]; // For multi-modal
  metadata?: Record<string, any>; // For special message types like search results
}

export type PageContext = 
  | 'main_chat' 
  | 'vm_hub' 
  | 'scout' 
  | 'multi_modal_chat' 
  | 'mcp_marketplace' 
  | 'integration_workbench' 
  | 'live_api_studio'
  | 'mini_apps';

export interface PageInfo {
  path: string;
  name: string;
  icon?: React.FC<React.SVGProps<SVGSVGElement>>;
  mamaBearVariant: MamaBearVariantName;
  pageContext: PageContext;
}

export interface MiniApp {
  id: string;
  name:string;
  logoUrl: string;
  appUrl: string;
  description: string;
}

export interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

export interface GeminiModel {
  id: string;
  name: string;
  description?: string;
}