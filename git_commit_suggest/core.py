from pathlib import Path
from .config import Config
from .providers import anthropic, openai, gemini
import subprocess

PROVIDERS = {
    'anthropic': anthropic.AnthropicProvider,
    'openai': openai.OpenAIProvider,
    'gemini': gemini.GeminiProvider
}

def get_staged_changes():
    """Get git diff of staged changes."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def generate_suggestion(diff):
    """Generate commit message using configured LLM provider."""
    config = Config()
    provider_name = config.config['provider']
    api_key = config.get_api_key(provider_name)
    
    if not api_key:
        return None
        
    provider_class = PROVIDERS.get(provider_name)
    if not provider_class:
        return None
        
    provider = provider_class(api_key)
    return provider.generate_commit_message(diff)

def main():
    diff = get_staged_changes()
    if diff:
        suggestion = generate_suggestion(diff)
        if suggestion:
            print(suggestion)