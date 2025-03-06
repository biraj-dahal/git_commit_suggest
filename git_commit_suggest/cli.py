import click
from .config.manager import ConfigManager
from .shell.manager import ShellManager
from .core import generate_suggestion
from .config.schema import Provider, Shell

@click.group()
def cli():
    """Git Commit Suggest - AI-powered commit message generator"""
    pass

@cli.command()
def suggest():
    """Generate a commit message suggestion"""
    message = generate_suggestion()
    if message:
        click.echo(message)

@cli.command()
@click.option('--provider', type=click.Choice([p.value for p in Provider]))
@click.option('--shell', type=click.Choice([s.value for s in Shell]))
@click.option('--shortcut', help="Keyboard shortcut (e.g., ctrl-g)")
@click.option('--api-key', help="API key for the selected provider")
def configure(provider, shell, shortcut, api_key):
    """Configure Git Commit Suggest"""
    config_manager = ConfigManager()
    
    if provider:
        config_manager.config.provider = Provider(provider)
    if shell:
        config_manager.config.shell = Shell(shell)
    if shortcut:
        config_manager.config.shortcut = shortcut
    if api_key:
        provider_config = config_manager.config.providers[config_manager.config.provider.value]
        provider_config.api_key = api_key

    config_manager.save_config()
    click.echo("Configuration updated successfully!")

@cli.command()
def install():
    """Install shell integration"""
    config_manager = ConfigManager()
    shell_manager = ShellManager(config_manager.config)
    
    if shell_manager.install_shell_integration():
        click.echo("Shell integration installed successfully!")
    else:
        click.echo("Failed to install shell integration.")