from enum import Enum
from dataclasses import dataclass
from collections import defaultdict

class Provider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GEMINI = "gemini"

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
    provider = Provider.OPENAI 
    shell = Shell.ZSH
    shortcut = "ctrl-m"
    providers = {}
    commit_template = "{type}({scope}): {message}"
    follow_template = True
    custom_prompt = None
    debug = False