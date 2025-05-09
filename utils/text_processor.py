"""Text processing utilities for handling descriptions."""
from typing import Tuple

def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace and newlines."""
    if not text:
        return ""
    return " ".join(text.split())

def find_sentence_boundary(text: str, max_length: int) -> int:
    """Find the best position to truncate text at a sentence boundary."""
    if len(text) <= max_length:
        return len(text)
    
    truncated = text[:max_length]
    sentence_endings = [
        truncated.rfind('.'),
        truncated.rfind('?'),
        truncated.rfind('!')
    ]
    
    # Find the last valid sentence-ending punctuation
    valid_endings = [pos for pos in sentence_endings if pos >= 0]
    if valid_endings:
        return max(valid_endings) + 1  # Include punctuation in truncation
    
    # Fallback to the last word boundary
    last_space = truncated.rfind(' ')
    return last_space if last_space > 0 else max_length

def smart_truncate(text: str, max_length: int) -> str:
    """Intelligently truncate text while preserving sentence structure."""
    text = clean_text(text)
    if not text:
        return ""  # Return an empty string if no text is provided or cleaned
    
    if len(text) <= max_length:
        return text
    
    boundary = find_sentence_boundary(text, max_length)
    truncated = text[:boundary].strip()
    
    # Ensure proper sentence ending if not already present
    if truncated and truncated[-1] not in '.!?':
        truncated += "."
    
    return truncated
