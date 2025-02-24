import json
import os
from pathlib import Path
from .schema import Config, ProviderConfig, Provider, Shell


class ConfigManager:
    def __init__(self):
        self.config_dir = Path