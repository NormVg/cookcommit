"""
Text processing utilities.
"""

from typing import List
from ..config import MAX_CHUNK_SIZE


def chunk_text(text: str, max_chunk_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Split text into chunks that fit within the model's context window.

    Args:
        text: Text to chunk
        max_chunk_size: Maximum size per chunk

    Returns:
        List of text chunks
    """
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0

    for line in lines:
        line_size = len(line) + 1  # +1 for newline

        if current_size + line_size > max_chunk_size and current_chunk:
            # Start a new chunk
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks
