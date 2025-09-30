"""
File operations utilities.
"""

from pathlib import Path
from typing import Optional


def save_to_file(content: str, filepath: str) -> bool:
    """
    Save content to a file.

    Args:
        content: Content to save
        filepath: Path to save file

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False


def read_from_file(filepath: str) -> Optional[str]:
    """
    Read content from a file.

    Args:
        filepath: Path to read from

    Returns:
        File content or None if failed
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return Path(filepath).exists()
