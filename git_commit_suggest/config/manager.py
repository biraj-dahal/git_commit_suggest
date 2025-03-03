import json
import os
from pathlib import Path
from schema import Config, ProviderConfig, Provider, Shell


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / "config" / "git-commit-suggest"
        self.config_file = self.config_dir / "config.json"
        print(self.config_dir)

config_obj = ConfigManager()
