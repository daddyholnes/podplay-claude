"""
Theme Manager Service
Manages the three sensory-friendly sanctuary themes and user customizations
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class ThemeColors:
    """Color scheme for a theme"""
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    border: str
    success: str
    warning: str
    error: str
    info: str

@dataclass
class SensorySettings:
    """Sensory-friendly settings for neurodivergent users"""
    reduce_motion: bool = False
    high_contrast: bool = False
    large_text: bool = False
    simplified_ui: bool = False
    focus_indicators: bool = True
    screen_reader_optimized: bool = False
    color_blind_friendly: bool = True
    reduce_transparency: bool = False

@dataclass
class ThemeConfiguration:
    """Complete theme configuration"""
    id: str
    name: str
    description: str
    colors: ThemeColors
    sensory_settings: SensorySettings
    css_variables: Dict[str, str]
    component_overrides: Dict[str, Any]
    accessibility_level: str  # 'standard', 'enhanced', 'maximum'

class ThemeManager:
    """Manages sanctuary themes and user customizations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.themes = self._initialize_themes()
        self.user_customizations = {}  # Store per-user theme customizations
        self.active_themes = {}  # Track active theme per user
        
        logger.info("Theme Manager initialized with 3 sanctuary themes")
    
    def _initialize_themes(self) -> Dict[str, ThemeConfiguration]:
        """Initialize the three sanctuary themes"""
        
        # Sky Sanctuary - Calming blues and whites
        sky_theme = ThemeConfiguration(
            id="sky",
            name="Sky Sanctuary",
            description="Calming sky blues and soft whites - perfect for focus and tranquility",
            colors=ThemeColors(
                primary="#4A90E2",          # Gentle sky blue
                secondary="#87CEEB",        # Light sky blue
                accent="#FFE4B5",           # Soft cream accent
                background="#F8FAFE",       # Very light blue-white
                surface="#FFFFFF",          # Pure white
                text_primary="#2C3E50",     # Dark blue-gray
                text_secondary="#5A6C7D",   # Medium blue-gray
                border="#E1E8ED",           # Light blue-gray border
                success="#52C41A",          # Gentle green
                warning="#FAAD14",          # Soft amber
                error="#FF7875",            # Gentle red
                info="#1890FF"              # Sky blue info
            ),
            sensory_settings=SensorySettings(
                reduce_motion=True,
                high_contrast=False,
                large_text=False,
                simplified_ui=False,
                focus_indicators=True,
                screen_reader_optimized=True,
                color_blind_friendly=True,
                reduce_transparency=False
            ),
            css_variables={
                "--border-radius": "8px",
                "--shadow-soft": "0 2px 8px rgba(74, 144, 226, 0.1)",
                "--transition-gentle": "all 0.3s ease",
                "--spacing-unit": "8px",
                "--font-family-primary": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
                "--font-size-base": "16px",
                "--line-height-relaxed": "1.6"
            },
            component_overrides={
                "chat_bubble": {
                    "background": "#FFFFFF",
                    "border": "1px solid #E1E8ED",
                    "shadow": "0 1px 3px rgba(0,0,0,0.1)"
                },
                "sidebar": {
                    "background": "#F8FAFE",
                    "border_right": "1px solid #E1E8ED"
                },
                "button_primary": {
                    "background": "#4A90E2",
                    "hover_background": "#357ABD"
                }
            },
            accessibility_level="enhanced"
        )
        
        # Neon Sanctuary - Vibrant but comfortable dark theme
        neon_theme = ThemeConfiguration(
            id="neon",
            name="Neon Sanctuary", 
            description="Energizing neon colors on a comfortable dark background - stimulating yet easy on the eyes",
            colors=ThemeColors(
                primary="#00FFFF",          # Cyan neon
                secondary="#FF00FF",        # Magenta neon
                accent="#FFFF00",           # Yellow neon
                background="#0D1117",       # Dark background
                surface="#161B22",          # Slightly lighter surface
                text_primary="#F0F6FC",     # Light text
                text_secondary="#8B949E",   # Gray text
                border="#30363D",           # Dark border
                success="#00FF88",          # Neon green
                warning="#FFAA00",          # Neon orange
                error="#FF4444",            # Neon red
                info="#00AAFF"              # Neon blue
            ),
            sensory_settings=SensorySettings(
                reduce_motion=False,
                high_contrast=True,
                large_text=False,
                simplified_ui=False,
                focus_indicators=True,
                screen_reader_optimized=True,
                color_blind_friendly=True,
                reduce_transparency=True
            ),
            css_variables={
                "--border-radius": "6px",
                "--shadow-neon": "0 0 10px rgba(0, 255, 255, 0.3)",
                "--transition-electric": "all 0.2s ease-out",
                "--spacing-unit": "8px",
                "--font-family-primary": "'JetBrains Mono', 'Consolas', monospace",
                "--font-size-base": "16px",
                "--line-height-relaxed": "1.5",
                "--glow-intensity": "0.8"
            },
            component_overrides={
                "chat_bubble": {
                    "background": "#161B22",
                    "border": "1px solid #30363D",
                    "shadow": "0 0 5px rgba(0, 255, 255, 0.2)"
                },
                "sidebar": {
                    "background": "#0D1117",
                    "border_right": "1px solid #30363D"
                },
                "button_primary": {
                    "background": "linear-gradient(45deg, #00FFFF, #FF00FF)",
                    "hover_background": "linear-gradient(45deg, #00CCCC, #CC00CC)"
                }
            },
            accessibility_level="enhanced"
        )
        
        # Stellar Sanctuary - Deep space theme with cosmic colors
        stellar_theme = ThemeConfiguration(
            id="stellar", 
            name="Stellar Sanctuary",
            description="Deep cosmic colors inspired by nebulae and starfields - mysterious and contemplative",
            colors=ThemeColors(
                primary="#8A2BE2",          # Blue violet
                secondary="#DA70D6",        # Orchid
                accent="#FFD700",           # Gold star
                background="#0B0B0F",       # Deep space black
                surface="#1A1A2E",          # Dark purple surface
                text_primary="#E6E6FA",     # Lavender text
                text_secondary="#B19CD9",   # Light purple text
                border="#3A3A5C",           # Purple-gray border
                success="#32CD32",          # Lime green
                warning="#FFA500",          # Orange
                error="#FF6347",            # Tomato
                info="#4169E1"              # Royal blue
            ),
            sensory_settings=SensorySettings(
                reduce_motion=True,
                high_contrast=False,
                large_text=False,
                simplified_ui=False,
                focus_indicators=True,
                screen_reader_optimized=True,
                color_blind_friendly=True,
                reduce_transparency=False
            ),
            css_variables={
                "--border-radius": "12px",
                "--shadow-cosmic": "0 4px 20px rgba(138, 43, 226, 0.2)",
                "--transition-stellar": "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                "--spacing-unit": "8px",
                "--font-family-primary": "'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif", 
                "--font-size-base": "16px",
                "--line-height-relaxed": "1.7",
                "--gradient-nebula": "linear-gradient(135deg, #8A2BE2, #DA70D6, #4169E1)"
            },
            component_overrides={
                "chat_bubble": {
                    "background": "#1A1A2E",
                    "border": "1px solid #3A3A5C",
                    "shadow": "0 2px 12px rgba(138, 43, 226, 0.15)",
                    "backdrop_filter": "blur(10px)"
                },
                "sidebar": {
                    "background": "linear-gradient(180deg, #0B0B0F, #1A1A2E)",
                    "border_right": "1px solid #3A3A5C"
                },
                "button_primary": {
                    "background": "linear-gradient(45deg, #8A2BE2, #DA70D6)",
                    "hover_background": "linear-gradient(45deg, #7B1FA2, #C458C4)"
                }
            },
            accessibility_level="standard"
        )
        
        return {
            "sky": sky_theme,
            "neon": neon_theme, 
            "stellar": stellar_theme
        }
    
    def get_theme(self, theme_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a theme configuration, optionally with user customizations"""
        if theme_id not in self.themes:
            return None
        
        theme = self.themes[theme_id]
        theme_dict = asdict(theme)
        
        # Apply user customizations if available
        if user_id and user_id in self.user_customizations:
            customizations = self.user_customizations[user_id].get(theme_id, {})
            self._apply_customizations(theme_dict, customizations)
        
        return theme_dict
    
    def get_all_themes(self, user_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get all available themes"""
        result = {}
        for theme_id in self.themes.keys():
            theme = self.get_theme(theme_id, user_id)
            if theme:  # Only include themes that are not None
                result[theme_id] = theme
        return result
    
    def set_active_theme(self, user_id: str, theme_id: str) -> Dict[str, Any]:
        """Set the active theme for a user"""
        if theme_id not in self.themes:
            return {'error': f'Unknown theme: {theme_id}'}
        
        self.active_themes[user_id] = theme_id
        
        logger.info(f"Set active theme for user {user_id}: {theme_id}")
        
        return {
            'user_id': user_id,
            'active_theme': theme_id,
            'theme_data': self.get_theme(theme_id, user_id),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_active_theme(self, user_id: str) -> Dict[str, Any]:
        """Get the active theme for a user"""
        theme_id = self.active_themes.get(user_id, 'sky')  # Default to sky
        return {
            'user_id': user_id,
            'active_theme_id': theme_id,
            'theme_data': self.get_theme(theme_id, user_id)
        }
    
    def customize_theme(self, user_id: str, theme_id: str, 
                       customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply custom settings to a theme for a specific user"""
        if theme_id not in self.themes:
            return {'error': f'Unknown theme: {theme_id}'}
        
        # Initialize user customizations if needed
        if user_id not in self.user_customizations:
            self.user_customizations[user_id] = {}
        
        if theme_id not in self.user_customizations[user_id]:
            self.user_customizations[user_id][theme_id] = {}
        
        # Apply customizations
        self.user_customizations[user_id][theme_id].update(customizations)
        
        logger.info(f"Applied theme customizations for user {user_id}, theme {theme_id}")
        
        return {
            'user_id': user_id,
            'theme_id': theme_id,
            'customizations_applied': customizations,
            'updated_theme': self.get_theme(theme_id, user_id),
            'timestamp': datetime.now().isoformat()
        }
    
    def update_sensory_settings(self, user_id: str, theme_id: str, 
                              sensory_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update sensory-friendly settings for a user's theme"""
        if theme_id not in self.themes:
            return {'error': f'Unknown theme: {theme_id}'}
        
        # Validate sensory settings
        valid_settings = {
            'reduce_motion', 'high_contrast', 'large_text', 'simplified_ui',
            'focus_indicators', 'screen_reader_optimized', 'color_blind_friendly',
            'reduce_transparency'
        }
        
        filtered_settings = {
            k: v for k, v in sensory_settings.items() 
            if k in valid_settings
        }
        
        # Apply as theme customization
        customizations = {'sensory_settings': filtered_settings}
        return self.customize_theme(user_id, theme_id, customizations)
    
    def get_css_variables(self, theme_id: str, user_id: Optional[str] = None) -> Dict[str, str]:
        """Get CSS variables for a theme"""
        theme_data = self.get_theme(theme_id, user_id)
        if not theme_data:
            return {}
        
        # Combine base CSS variables with color variables
        css_vars = theme_data['css_variables'].copy()
        
        # Add color variables
        colors = theme_data['colors']
        for color_name, color_value in colors.items():
            css_vars[f'--color-{color_name.replace("_", "-")}'] = color_value
        
        # Add sensory setting variables
        sensory = theme_data['sensory_settings']
        css_vars['--motion-duration'] = '0ms' if sensory['reduce_motion'] else '300ms'
        css_vars['--font-size-multiplier'] = '1.2' if sensory['large_text'] else '1.0'
        css_vars['--contrast-level'] = 'high' if sensory['high_contrast'] else 'normal'
        
        return css_vars
    
    def generate_theme_css(self, theme_id: str, user_id: Optional[str] = None) -> str:
        """Generate complete CSS for a theme"""
        css_vars = self.get_css_variables(theme_id, user_id)
        theme_data = self.get_theme(theme_id, user_id)
        
        if not theme_data:
            return ""
        
        # Start with CSS variables
        css_lines = [f":root.theme-{theme_id} {{"]
        
        for var_name, var_value in css_vars.items():
            css_lines.append(f"  {var_name}: {var_value};")
        
        css_lines.append("}")
        
        # Add component-specific styles
        component_overrides = theme_data.get('component_overrides', {})
        
        for component, styles in component_overrides.items():
            css_lines.append(f"\n.theme-{theme_id} .{component.replace('_', '-')} {{")
            
            for property_name, property_value in styles.items():
                css_property = property_name.replace('_', '-')
                css_lines.append(f"  {css_property}: {property_value};")
            
            css_lines.append("}")
        
        # Add accessibility enhancements
        sensory = theme_data['sensory_settings']
        
        if sensory['reduce_motion']:
            css_lines.extend([
                f"\n.theme-{theme_id} * {{",
                "  animation-duration: 0.01ms !important;",
                "  animation-iteration-count: 1 !important;", 
                "  transition-duration: 0.01ms !important;",
                "}"
            ])
        
        if sensory['high_contrast']:
            css_lines.extend([
                f"\n.theme-{theme_id} {{",
                "  filter: contrast(1.5);",
                "}"
            ])
        
        if sensory['large_text']:
            css_lines.extend([
                f"\n.theme-{theme_id} {{",
                "  font-size: calc(var(--font-size-base) * 1.2);",
                "}"
            ])
        
        return "\n".join(css_lines)
    
    def get_theme_recommendations(self, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend themes based on user preferences"""
        recommendations = []
        
        # Analyze preferences
        prefers_dark = user_preferences.get('prefers_dark_mode', False)
        needs_high_contrast = user_preferences.get('needs_high_contrast', False)
        prefers_minimal = user_preferences.get('prefers_minimal_ui', False)
        has_motion_sensitivity = user_preferences.get('motion_sensitivity', False)
        
        for theme_id, theme in self.themes.items():
            score = 0
            reasons = []
            
            # Dark mode preference
            if prefers_dark and theme_id in ['neon', 'stellar']:
                score += 3
                reasons.append("Dark theme as requested")
            elif not prefers_dark and theme_id == 'sky':
                score += 3
                reasons.append("Light theme as requested")
            
            # High contrast needs
            if needs_high_contrast and theme.sensory_settings.high_contrast:
                score += 2
                reasons.append("High contrast support")
            
            # Motion sensitivity
            if has_motion_sensitivity and theme.sensory_settings.reduce_motion:
                score += 2
                reasons.append("Reduced motion by default")
            
            # Accessibility level
            if theme.accessibility_level == 'enhanced':
                score += 1
                reasons.append("Enhanced accessibility features")
            
            recommendations.append({
                'theme_id': theme_id,
                'theme_name': theme.name,
                'score': score,
                'reasons': reasons,
                'description': theme.description
            })
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations
    
    def export_user_customizations(self, user_id: str) -> Dict[str, Any]:
        """Export user's theme customizations"""
        return {
            'user_id': user_id,
            'active_theme': self.active_themes.get(user_id, 'sky'),
            'customizations': self.user_customizations.get(user_id, {}),
            'export_timestamp': datetime.now().isoformat()
        }
    
    def import_user_customizations(self, user_id: str, 
                                 customization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import user's theme customizations"""
        try:
            if 'active_theme' in customization_data:
                self.active_themes[user_id] = customization_data['active_theme']
            
            if 'customizations' in customization_data:
                self.user_customizations[user_id] = customization_data['customizations']
            
            return {
                'user_id': user_id,
                'import_successful': True,
                'active_theme': self.active_themes.get(user_id),
                'customizations_count': len(self.user_customizations.get(user_id, {})),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error importing customizations for user {user_id}: {str(e)}")
            return {
                'user_id': user_id,
                'import_successful': False,
                'error': str(e)
            }
    
    def _apply_customizations(self, theme_dict: Dict[str, Any], 
                            customizations: Dict[str, Any]):
        """Apply user customizations to a theme dictionary"""
        for key, value in customizations.items():
            if key in theme_dict:
                if isinstance(theme_dict[key], dict) and isinstance(value, dict):
                    theme_dict[key].update(value)
                else:
                    theme_dict[key] = value
    
    def get_theme_statistics(self) -> Dict[str, Any]:
        """Get usage statistics for themes"""
        stats = {
            'total_users': len(self.active_themes),
            'theme_usage': {},
            'customization_usage': len(self.user_customizations),
            'most_popular_theme': None
        }
        
        # Count theme usage
        for theme_id in self.active_themes.values():
            stats['theme_usage'][theme_id] = stats['theme_usage'].get(theme_id, 0) + 1
        
        # Find most popular theme
        if stats['theme_usage']:
            stats['most_popular_theme'] = max(
                stats['theme_usage'], 
                key=stats['theme_usage'].get
            )
        
        return stats
