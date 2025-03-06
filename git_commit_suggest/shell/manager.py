from pathlib import Path
from typing import Dict, Optional
from ..config.schema import Shell, Config

class ShellManager:
    def __init__(self, config: Config):
        self.config = config
        self.template_dir = Path(__file__).parent / 'templates'
        self.shell_config_files: Dict[Shell, str] = {
            Shell.BASH: '.bashrc',
            Shell.ZSH: '.zshrc',
            Shell.FISH: 'config.fish',
            Shell.NUSHELL: 'config.nu',
            Shell.XONSH: '.xonshrc',
            Shell.POWERSHELL: 'Microsoft.PowerShell_profile.ps1'
        }

    def get_config_path(self) -> Optional[Path]:
        shell_config = self.shell_config_files.get(self.config.shell)
        if not shell_config:
            return None

        if self.config.shell == Shell.POWERSHELL:
            return Path.home() / 'Documents' / 'WindowsPowerShell' / shell_config
        return Path.home() / shell_config

    def install_shell_integration(self) -> bool:
        config_path = self.get_config_path()
        if not config_path:
            print(f"Unsupported shell: {self.config.shell.value}")
            return False

        template_file = self.template_dir / f'{self.config.shell.value}.template'
        if not template_file.exists():
            print(f"Template not found for shell: {self.config.shell.value}")
            return False

        try:
            with open(template_file) as f:
                template = f.read()

            config_content = template.format(
                shortcut=self.config.shortcut,
                command="git-commit-suggest"
            )

            config_path.parent.mkdir(parents=True, exist_ok=True)

            mode = 'a' if config_path.exists() else 'w'
            with open(config_path, mode) as f:
                f.write(f"\n# Git Commit Suggest Configuration\n{config_content}\n")

            return True
        except Exception as e:
            if self.config.debug:
                print(f"Shell integration error: {e}")
            return False