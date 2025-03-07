from enum import Enum
from dataclasses import dataclass
from collections import defaultdict

class Provider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GEMINI = "gemini"
    HUGGINGFACE = "huggingface"
    LLAMA = "llama"

@dataclass
class LlamaConfig:
    model_path: str = "~/git-commit-suggest/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    context_length: int = 2048
    n_gpu_layers: int = 0 
    temperature: float = 0.7
    max_tokens: int = 100

class Shell(str, Enum):
    BASH = "bash"
    ZSH = "zsh"
    POWERSHELL = "fish"

@dataclass
class ProviderConfig:
    api_key = None
    model = None
    temperature = 0.7
    max_tokens = 100

@dataclass
class Config:
    provider = Provider.LLAMA
    shell = Shell.ZSH
    shortcut = "ctrl-m"
    providers = {}
    commit_template = "{type}({scope}): {message}"
    follow_template = True
    custom_prompt = None
    debug = False