import requests
from pathlib import Path
import os
import hashlib
from tqdm import tqdm

MODEL_INFO = {
    'tinyllama-1.1b-chat': {
        'url': 'https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf',
        'size': 1_200_000_000,  
        'sha256': 'abc123...'  
    }
}

def download_model(model_name='tinyllama-1.1b-chat'):
    """Download the specified model if it doesn't exist."""
    model_info = MODEL_INFO[model_name]
    model_dir = Path.home() / 'git-commit-suggest' / 'models'
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / f"{model_name}.gguf"
    if model_path.exists():
        return str(model_path)

    print(f"Downloading {model_name} model...")
    response = requests.get(model_info['url'], stream=True)
    total_size = model_info['size']
    
    with open(model_path, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    print(f"Model downloaded to {model_path}")
    return str(model_path)