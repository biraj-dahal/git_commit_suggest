import anthropic
from typing import Optional
from .base import LLMProvider

class AnthropicProvider(LLMProvider):
    def generate_commit_message(self, diff: str) -> Optional[str]:
        if not self.config.api_key:
            return None

        client = anthropic.Anthropic(api_key=self.config.api_key)
        
        try:
            response = client.messages.create(
                model=self.config.model or "claude-3-haiku-20240307",
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{
                    "role": "user",
                    "content": self._format_prompt(diff)
                }]
            )
            return response.content[0].text.strip()
        except Exception as e:
            if self.config.debug:
                print(f"Anthropic API error: {e}")
            return None