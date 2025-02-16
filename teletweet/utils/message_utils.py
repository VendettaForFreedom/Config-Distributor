from typing import Tuple, Union, List, Optional
from pyrogram import types
from ..config import SOURCE_CHANNEL, tweet_length

def get_source_info(message: types.Message) -> Tuple[str, str]:
    """Extract source channel information from a message."""
    if message.forward_from_chat:
        chat = message.forward_from_chat
        username = chat.username
        chat_id = str(chat.id)
        msg_id = str(message.forward_from_message_id)
        source_url = f"\nhttps://t.me/{username}/" if username else ""
        reference = f"{chat_id}/{msg_id}"
        return source_url, reference
    return SOURCE_CHANNEL, ""

def combine_messages(original: str, attached: str) -> str:
    """Combine original and attached messages with proper formatting."""
    if not original or not attached:
        return original or attached or ""
    
    # Add double newline between messages for better readability
    return f"{original}\n\n{attached}"

def calculate_total_length(content: str, platform: str, attached_message: Optional[str] = None) -> int:
    """Calculate total message length including attachments and formatting."""
    total_content = content

    if attached_message:
        total_content = combine_messages(content, attached_message)
        
    # Add length for source info and platform-specific additions
    if platform == "twitter":
        # Account for URL shortening, hashtags, etc.
        additional_length = len("\n\n") + 23  # Twitter URL shortening to 23 chars
    else:
        # Telegram formatting
        additional_length = len("\n\n")
        
    return len(total_content) + additional_length

def check_message_length(content: str, platform: str, attached_message: Optional[str] = None) -> Tuple[bool, Union[str, List[str]], Optional[int]]:
    """Check if message fits platform limits and provide truncation options."""
    if platform == "twitter":
        max_length = tweet_length
    else:  # telegram has a 4096 char limit
        max_length = 4000
    
    total_length = calculate_total_length(content, platform, attached_message)
    combined_content = combine_messages(content, attached_message) if attached_message else content
        
    if total_length <= max_length:
        return True, combined_content, None
        
    # Generate truncation options
    auto_truncated = combined_content[:max_length-3] + "..."
    smart_truncated = truncate_at_sentence(combined_content, max_length-3) + "..."
    return False, [auto_truncated, smart_truncated], total_length - max_length

def truncate_at_sentence(text: str, limit: int) -> str:
    """Truncate text at the last sentence boundary before limit."""
    if len(text) <= limit:
        return text
        
    # Try to find the last sentence boundary
    last_boundary = max(
        text[:limit].rfind("."),
        text[:limit].rfind("!"),
        text[:limit].rfind("?")
    )
    
    if last_boundary == -1:
        # No sentence boundary found, try paragraph
        last_boundary = text[:limit].rfind("\n")
        if last_boundary == -1:
            # No paragraph boundary, try word boundary
            last_boundary = text[:limit].rfind(" ")
            if last_boundary == -1:
                # No word boundary, just cut at limit
                return text[:limit]
    
    return text[:last_boundary+1].strip()

def split_message(content: str, max_length: int, attached_message: Optional[str] = None) -> List[str]:
    """Split message into parts that fit the length limit."""
    if attached_message:
        content = combine_messages(content, attached_message)
    
    parts = []
    current_part = ""
    
    for line in content.split("\n"):
        if len(current_part + line + "\n") > max_length:
            if current_part:
                parts.append(current_part.strip())
                current_part = line + "\n"
            else:
                # Single line is too long, truncate it
                parts.append(line[:max_length-3] + "...")
        else:
            current_part += line + "\n"
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts

def truncate_content(content: str, limit: int = 500, attached_message: Optional[str] = None) -> str:
    """Truncate content to given limit while preserving meaning."""
    if attached_message:
        content = combine_messages(content, attached_message)
        
    if len(content) <= limit:
        return content
        
    truncated = truncate_at_sentence(content, limit-3)
    return truncated + "..."
