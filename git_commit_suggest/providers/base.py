from abc import ABC, abstractmethod
from typing import Optional
from ..config.schema import ProviderConfig

class LLMProvider(ABC):
    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    def generate_commit_message(self, diff: str) -> Optional[str]:
        pass

    def _format_prompt(self, diff: str) -> str:
        return f"""Generate a concise git commit message for this diff:

{diff}

Requirements:
- Follow conventional commits format if specified
- Be concise and descriptive
- Use present tense
- Start with a verb
- Maximum 50 characters for first line
- Optional: Include scope in parentheses
- Optional: Add detailed description after blank line"""