from typing import Optional
from pathlib import Path
import subprocess
from .base import LLMProvider
from ..config.schema import LlamaConfig

class LlamaProvider(LLMProvider):
    def __init__(self, config: LlamaConfig):
        self.config = config
        self._ensure_model()
    
    def _ensure_model(self):
        """Ensure the model file exists, download if not."""
        model_path = Path(self.config.model_path).expanduser()
        if not model_path.exists():
            from ..models.download import download_model
            download_model()

    def generate_commit_message(self, diff: str) -> Optional[str]:
        try:
            from llama_cpp import Llama
            
            model_path = Path(self.config.model_path).expanduser()
            llm = Llama(
                model_path=str(model_path),
                n_ctx=self.config.context_length,
                n_gpu_layers=self.config.n_gpu_layers
            )

            prompt = f"""<system>You are a helpful assistant that generates git commit messages.</system>
<user>Generate a concise git commit message for this diff:
{diff}
Requirements:
- Be concise and descriptive
- Use present tense
- Start with a verb
- Maximum 50 characters
</user>
<assistant>"""

            output = llm(
                prompt,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stop=["</assistant>", "<user>"]
            )
            
            message = output['choices'][0]['text'].strip()
            return message.split('\n')[0]  # Return only the first line
            
        except Exception as e:
            if self.config.debug:
                print(f"Llama error: {e}")
            return None