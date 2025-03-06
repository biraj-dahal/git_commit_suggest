import subprocess
from typing import Optional

def get_staged_changes() -> Optional[str]:
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
    except Exception as e:
        print(f"Git error: {e}")
        return None

def is_git_repository() -> bool:
    """Check if current directory is a git repository."""
    try:
        subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False