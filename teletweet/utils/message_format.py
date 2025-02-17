import logging
import asyncio
from typing import Optional, Tuple, Dict
from pyrogram import Client, types
from ..config import (
    CONTINUE_READING,
    SOURCE_CHANNEL,
    SOURCE_REPOSITORY_CHANNEL_ID,
    CHANNEL_AD_MESSAGE_ID,
    CHANNEL,
    CHANNEL_ID,
    FEEDBACK,
    TODAY_CONFIG,
    CONFIG_CHANNEL
)

async def format_repository_message(client: Client, selected_pair: list) -> Tuple[str, str, str, Optional[bytes]]:
    """Format message from repository channel with specific formatting."""
    content, picture, chat_id, img_data = "", "", "", None
    try:
        if selected_pair:
            fetched_messages = await client.get_messages(SOURCE_REPOSITORY_CHANNEL_ID, selected_pair)
            for msg in fetched_messages:
                if msg.text is not None or msg.caption is not None:
                    content = msg.text or msg.caption
                    chat_id = msg.forward_from_message_id
                elif msg.photo is not None:
                    picture = msg.photo.file_id
                    img_data = await msg.download(in_memory=True)
                    setattr(img_data, "mode", "rb")
    except Exception as e:
        logging.error(f"Error fetching repository message: {e}")
    
    return content, picture, chat_id or "", img_data

async def get_channel_ad_message(client: Client) -> Optional[str]:
    """Get channel ad message with specific formatting."""
    try:
        channel_message = await client.get_messages(CHANNEL_ID, CHANNEL_AD_MESSAGE_ID)
        if channel_message and channel_message.text:
            # Only include text up to the channel tag
            stop_string = CHANNEL
            if stop_string in channel_message.text:
                channel_msg = channel_message.text.split(stop_string)[0] + stop_string
                return channel_msg
    except Exception as e:
        logging.error(f"Error fetching channel ad message: {e}")
    return None

async def handle_source_message(client: Client, message: types.Message) -> Optional[Dict]:
    """Handle source message and append channel ad message."""
    try:
        content = ""
        picture = ""
        chat_id = ""
        img_data = None
        source_message = message

        # If this is a multi-message forward from source channel
        if source_message.forward_from_chat and source_message.forward_from_chat.type == "channel":
            multi_message = source_message
            # Wait briefly for potential second part
            await asyncio.sleep(1)
            # Fetch subsequent message
            next_message = await client.get_messages(
                source_message.chat.id,
                message.message_id + 1
            )
            
            if next_message and (message.date - next_message.date).total_seconds() < 300:
                if (message.photo is not None and 
                    (multi_message.text is not None or multi_message.caption is not None)):
                    content = multi_message.text or multi_message.caption
                    picture = message.photo.file_id
                    chat_id = multi_message.forward_from_message_id
                    img_data = await message.download(in_memory=True)
                    setattr(img_data, "mode", "rb")
                elif (multi_message.photo is not None and 
                      (message.text is not None or message.caption is not None)):
                    content = message.text or message.caption
                    picture = multi_message.photo.file_id
                    chat_id = message.forward_from_message_id
                    img_data = await multi_message.download(in_memory=True)
                    setattr(img_data, "mode", "rb")

        return {
            "content": content,
            "picture": picture,
            "chat_id": chat_id or "",
            "img_data": img_data
        } if any([content, picture]) else None

    except Exception as e:
        logging.error(f"Error handling source message: {e}")
        return None

def format_content_with_ad(content: str, chat_id: str = "", truncate_length: int = 300) -> str:
    """Format content with continuation notice and channel information."""
    if not content:
        return ""
    
    truncated = truncate_content(content, truncate_length)
    message_body = (
        f"{truncated}\n\n"
        f"{CONTINUE_READING}"
        f"{SOURCE_CHANNEL}{chat_id}\n\n"
    )
    return message_body

def truncate_content(content: str, limit: int = 300) -> str:
    """Truncate content with ellipsis if needed."""
    if len(content) > limit:
        return content[:limit] + "..."
    return content

async def get_random_repository_content(client: Client) -> Optional[str]:
    """Get random content from repository channel."""
    try:
        # Get random message pair from repository
        from .repository import get_random_message_pair
        selected_pair = get_random_message_pair()
        if selected_pair:
            content, _, _, _ = await format_repository_message(client, selected_pair)
            return content
    except Exception as e:
        logging.error(f"Error getting repository content: {e}")
    return None

from .tags import generate_tags

async def format_config_message(client: Client, part: str) -> str:
    """Format config message with specific formatting and repository content."""
    from .repository import get_random_message_pair

    # Get random repository content
    selected_pair = get_random_message_pair()
    if selected_pair:
        content, picture, chat_id, _ = await format_repository_message(client, selected_pair)
        # Format repository content first
        message_body = (
            truncate_content(content, 300) + "\n\n" + 
            CONTINUE_READING +
            SOURCE_CHANNEL + f"{chat_id}\n\n"
        )
    else:
        message_body = ""

    # Add config part in monospace format with proper spacing
    formatted_content = (
        message_body + 
        f"`{part}`" + "\n\n" +
        CHANNEL + "\n\n" +
        generate_tags("random3")
    )
    
    return formatted_content

def format_config_channel_message(message_id: int) -> str:
    """Format config channel message with specific formatting."""
    return (
        f"{CONFIG_CHANNEL}{message_id}"
    )
