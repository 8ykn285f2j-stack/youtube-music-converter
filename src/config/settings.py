"""Configuration and settings management for YouTube Music Converter"""

import json
from pathlib import Path
from src.utils import get_config_dir, get_downloads_dir


class Settings:
    """Manages application settings and configuration."""
    
    DEFAULT_SETTINGS = {
        'output_directory': str(get_downloads_dir()),
        'default_format': 'mp3',
        'default_bitrate': '320k',
        'embed_artwork': True,
        'embed_metadata': True,
        'quality_threshold': 320,
        'theme': 'dark',
        'window_width': 900,
        'window_height': 700,
        'keep_temp_files': False,
    }
    
    def __init__(self):
        """Initialize settings manager."""
        self.config_dir = get_config_dir()
        self.settings_file = self.config_dir / 'config.json'
        self.settings = self.load()
    
    def load(self):
        """
        Load settings from file or create defaults.
        
        Returns:
            dict: Settings dictionary
        """
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to add any new settings
                    merged = self.DEFAULT_SETTINGS.copy()
                    merged.update(settings)
                    return merged
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.DEFAULT_SETTINGS.copy()
        
        return self.DEFAULT_SETTINGS.copy()
    
    def save(self):
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """
        Get setting value.
        
        Args:
            key (str): Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """
        Set setting value.
        
        Args:
            key (str): Setting key
            value: Setting value
        """
        self.settings[key] = value
        self.save()
    
    def update(self, settings_dict):
        """
        Update multiple settings.
        
        Args:
            settings_dict (dict): Dictionary of settings to update
        """
        self.settings.update(settings_dict)
        self.save()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()


# Global settings instance
settings = Settings()
