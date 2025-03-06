import os
import json
from pathlib import Path
from typing import Optional
from .schema import Config, ProviderConfig, Provider, Shell

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'git-commit-suggest'
        self.config_file = self.config_dir / 'config.json'
        self.config: Config = self._load_config()

    def _load_config(self) -> Config:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if self.config_file.exists():
            with open(self.config_file) as f:
                config_data = json.load(f)
        else:
            config_data = {}

        # Create default provider configs
        providers = {}
        for provider in Provider:
            api_key = (
                config_data.get('providers', {}).get(provider.value, {}).get('api_key') or
                os.getenv(f'{provider.value.upper()}_API_KEY')
            )
            providers[provider.value] = ProviderConfig(
                api_key=api_key,
                model=config_data.get('providers', {}).get(provider.value, {}).get('model')
            )

        return Config(
            provider=Provider(config_data.get('provider', Provider.ANTHROPIC.value)),
            shell=Shell(config_data.get('shell', self._detect_shell())),
            shortcut=config_data.get('shortcut', 'ctrl-g'),
            providers=providers,
            commit_template=config_data.get('commit_template', "{type}({scope}): {message}"),
            conventional_commits=config_data.get('conventional_commits', True),
            custom_prompt=config_data.get('custom_prompt'),
            debug=config_data.get('debug', False)
        )

    def _detect_shell(self) -> str:
        shell_path = os.environ.get('SHELL', '')
        shell_name = shell_path.split('/')[-1]
        return shell_name if shell_name in Shell.__members__ else Shell.BASH.value

    def save_config(self):
        config_dict = {
            'provider': self.config.provider.value,
            'shell': self.config.shell.value,
            'shortcut': self.config.shortcut,
            'providers': {
                name: vars(config) 
                for name, config in self.config.providers.items()
            },
            'commit_template': self.config.commit_template,
            'conventional_commits': self.config.conventional_commits,
            'custom_prompt': self.config.custom_prompt,
            'debug': self.config.debug
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)

    def get_provider_config(self, provider: Provider) -> Optional[ProviderConfig]:
        return self.config.providers.get(provider.value)