"""Message utility functions for TeleTweet."""

from typing import List, Tuple
from .constants import tweet_length, max_telegram_length

def check_message_length(text: str, platform: str = None, attached_text: str = None) -> Tuple[bool, str, int]:
    """Check if the message fits within platform limits."""
    if not text:
        return True, "", 0

    # Add attached text if present
    final_text = f"{text}\n{attached_text}" if attached_text else text

    # Get length limit based on platform
    limit = tweet_length if platform == "twitter" else max_telegram_length

    # Check if message fits
    if len(final_text) <= limit:
        return True, final_text, 0
    else:
        return False, final_text, len(final_text) - limit

def truncate_text(text: str, length: int = 300) -> str:
    """Truncate text to specified length with proper word boundaries."""
    if not text or len(text) <= length:
        return text

    # Try to truncate at word boundary
    last_space = text[:length].rfind(' ')
    if last_space > 0:
        return text[:last_space] + "..."
    
    return text[:length] + "..."

def calculate_total_length(message_parts: List[str]) -> int:
    """Calculate total length of all message parts."""
    return sum(len(part) for part in message_parts)

def split_message(text: str, limit: int = max_telegram_length, attached_text: str = None) -> List[str]:
    """Split long message into parts respecting word boundaries."""
    if not text:
        return []

    # If message fits, return as is
    if len(text) <= limit:
        if attached_text:
            return [f"{text}\n{attached_text}"]
        return [text]

    parts = []
    current_text = text

    while len(current_text) > limit:
        # Find last space within limit
        split_point = current_text[:limit].rfind(' ')
        if split_point == -1:
            split_point = limit

        # Add part
        parts.append(current_text[:split_point].strip())
        current_text = current_text[split_point:].strip()

    # Add remaining text
    if current_text:
        parts.append(current_text)

    # Add attached text to last part
    if attached_text and parts:
        parts[-1] = f"{parts[-1]}\n{attached_text}"

    return parts

def combine_messages(text: str, attached_text: str = None) -> str:
    """Combine main message with attached text."""
    if not text:
        return attached_text or ""
    if not attached_text:
        return text
    return f"{text}\n{attached_text}"
