import asyncio
import logging
from typing import Optional, Dict
from pyrogram import Client, types
from ..config import (
    CHANNEL_ID,
    GROUP_ID,
    GROUP_TOPIC_ID,
    GROUP,
    CHANNEL_URL
)
from .tweet import send_tweet
from .message_utils import (
    check_message_length,
    split_message,
    combine_messages,
    calculate_total_length
)
from .tags import generate_tags

async def generate_preview(
    message: types.Message,
    attached_message: Optional[str] = None
) -> Dict[str, str]:
    """Generate preview text for each enabled platform."""
    content = message.text or message.caption
    enabled = get_enabled_platforms()
    previews = {}
    
    if "channel" in enabled:
        final_content = combine_messages(content, attached_message) if attached_message else content
        channel_text = final_content + "\n\n" + generate_tags("first5random")
        fits, _, over = check_message_length(channel_text, "channel")
        previews["channel"] = f"Channel Preview{' (Too Long!)' if not fits else ''}:\n\n{channel_text[:4000]}"
        if not fits:
            previews["channel"] += f"\n\n[{over} characters over limit]"
    
    if "group" in enabled:
        final_content = combine_messages(content, attached_message) if attached_message else content
        group_text = final_content + "\n\n" + (GROUP if GROUP else "") + generate_tags("first5random")
        fits, _, over = check_message_length(group_text, "group")
        previews["group"] = f"Group Preview{' (Too Long!)' if not fits else ''}:\n\n{group_text[:4000]}"
        if not fits:
            previews["group"] += f"\n\n[{over} characters over limit]"
            
    if "twitter" in enabled:
        final_content = combine_messages(content, attached_message) if attached_message else content
        tweet_text = final_content + "\n" + (CHANNEL_URL if CHANNEL_URL else "") + generate_tags()
        fits, _, over = check_message_length(tweet_text, "twitter")
        previews["twitter"] = f"Twitter Preview{' (Too Long!)' if not fits else ''}:\n\n{tweet_text[:280]}"
        if not fits:
            previews["twitter"] += f"\n\n[{over} characters over limit]"
    
    return previews
from .tags import generate_tags

def get_enabled_platforms() -> list:
    """Get list of enabled platforms based on configuration."""
    platforms = []
    if CHANNEL_ID:
        platforms.append("channel")
    if GROUP_ID:
        platforms.append("group")
    
    # Check Twitter credentials
    from ..config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
    if all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET]):
        platforms.append("twitter")
    
    return platforms

async def publish_to_channel(
    message: types.Message,
    content: str,
    picture=None,
    source_info=None,
    attached_message: Optional[str] = None
) -> types.Message:
    """Publish message to channel if configured."""
    if not CHANNEL_ID:
        logging.info("Channel publishing skipped - CHANNEL_ID not configured")
        return None
        
    try:
        final_content = combine_messages(content, attached_message) if attached_message else content
        if picture:
            return await message._client.send_photo(
                CHANNEL_ID,
                picture,
                caption=final_content + (source_info if source_info else "") + "\n\n" + generate_tags("first5random")
            )
        else:
            return await message._client.send_message(
                CHANNEL_ID,
                final_content + (source_info if source_info else "") + "\n\n" + generate_tags("first5random")
            )
    except Exception as e:
        logging.error(f"Error publishing to channel: {e}")
        return None

async def publish_to_group(
    message: types.Message,
    content: str,
    picture=None,
    source_info=None,
    attached_message: Optional[str] = None
) -> bool:
    """Publish message to group if configured."""
    if not GROUP_ID:
        logging.info("Group publishing skipped - GROUP_ID not configured")
        return False
        
    try:
        final_content = combine_messages(content, attached_message) if attached_message else content
        kwargs = {
            "chat_id": GROUP_ID,
            "reply_to_message_id": GROUP_TOPIC_ID if GROUP_TOPIC_ID else None
        }
        
        if picture:
            await message._client.send_photo(
                **kwargs,
                photo=picture,
                caption=final_content + (source_info if source_info else "") + "\n\n" + (GROUP if GROUP else "") + generate_tags("first5random")
            )
        else:
            await message._client.send_message(
                **kwargs,
                text=final_content + (source_info if source_info else "") + "\n\n" + (GROUP if GROUP else "") + generate_tags("first5random")
            )
        return True
    except Exception as e:
        logging.error(f"Error publishing to group: {e}")
        return False

async def publish_to_twitter(
    message: types.Message,
    content: str,
    media=None,
    source_info=None,
    attached_message: Optional[str] = None
) -> dict:
    """Publish message to Twitter."""
    try:
        final_content = combine_messages(content, attached_message) if attached_message else content
        tweet_text = final_content + (source_info if source_info else "") + "\n" + (CHANNEL_URL if CHANNEL_URL else "") + generate_tags()
        result = await send_tweet(
            message,
            tweet_text,
            [media] if media else None
        )
        if "error" in result:
            error_msg = f"Error publishing to Twitter: {result['error']}"
            logging.error(error_msg)
            await message.reply_text(error_msg)
            return result
        return result
    except Exception as e:
        error_msg = f"Error publishing to Twitter: {str(e)}"
        logging.error(error_msg)
        await message.reply_text(error_msg)
        return {"error": str(e)}

async def handle_publish(
    client: Client,
    message: types.Message,
    platforms: list,
    is_multiple: bool = False,
    attached_message: Optional[str] = None
):
    """Handle publishing to multiple platforms with length checks."""
    content = message.text or message.caption
    picture = message.photo.file_id if message.photo else None
    img_data = None
    
    if picture:
        img_data = await message.download(in_memory=True)
        setattr(img_data, "mode", "rb")
    
    # Get source information
    from .message_utils import get_source_info
    source_url, reference = await get_source_info(message)
    source_info = source_url + reference if source_url else None
    
    # Function to publish content to a specific platform
    async def publish_content(content_to_pub: str, platform: str):
        if platform == "channel" and CHANNEL_ID:
            result = await publish_to_channel(
                message, content_to_pub, picture, source_info, attached_message
            )
            # If publishing to Twitter is also requested, use channel message as reference
            if result and "twitter" in platforms:
                await publish_to_twitter(
                    result, content_to_pub, img_data, source_info, attached_message
                )
        elif platform == "group" and GROUP_ID:
            await publish_to_group(
                message, content_to_pub, picture, source_info, attached_message
            )
        elif platform == "twitter":
            await publish_to_twitter(
                message, content_to_pub, img_data, source_info, attached_message
            )
    
    # Filter out disabled platforms
    enabled_platforms = get_enabled_platforms()
    if "twitter" not in platforms:  # Always allow Twitter if requested
        platforms = [p for p in platforms if p in enabled_platforms]
    
    if not platforms:
        logging.warning("No enabled platforms to publish to")
        return
    
    # Handle multiple messages
    if is_multiple and "\n" in content:
        parts = [p.strip() for p in content.split("\n") if len(p.strip()) > 10]
        for part in parts:
            for platform in platforms:
                # Check message length for each platform
                fits, result, _ = check_message_length(
                    part, platform, attached_message
                )
                if fits:
                    await publish_content(result, platform)
                else:
                    # If message is too long, split it
                    max_length = 280 if platform == "twitter" else 4000
                    split_parts = split_message(
                        part, max_length, attached_message
                    )
                    for split_part in split_parts:
                        await publish_content(split_part, platform)
                        await asyncio.sleep(1)
            await asyncio.sleep(1)
    else:
        # Handle single message
        for platform in platforms:
            fits, result, _ = check_message_length(
                content, platform, attached_message
            )
            if fits:
                await publish_content(result, platform)
            else:
                # If message is too long, split it
                max_length = 280 if platform == "twitter" else 4000
                split_parts = split_message(
                    content, max_length, attached_message
                )
                for split_part in split_parts:
                    await publish_content(split_part, platform)
                    await asyncio.sleep(1)
