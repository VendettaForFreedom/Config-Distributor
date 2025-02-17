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
from .delayed_tasks import forward_ad_message

async def handle_publish(
    client: Client,
    message: types.Message,
    platforms: list,
    is_multiple: bool = False,
    attached_message: Optional[str] = None,
    use_repository: bool = False
):
    """Handle publishing to multiple platforms with length checks."""
    from .message_format import (
        format_repository_message,
        get_channel_ad_message,
        format_content_with_ad,
        format_config_message,
        format_config_channel_message,
        handle_source_message
    )

    # Initialize variables
    content = message.text or message.caption
    picture = None
    img_data = None
    chat_id = None
    source_info = None

    # Handle different message sources
    if use_repository:
        # Handle repository message
        from .repository import get_random_message_pair
        selected_pair = get_random_message_pair()
        if selected_pair:
            content, picture, chat_id, img_data = await format_repository_message(client, selected_pair)
    elif message.forward_from_chat:
        # Handle forwarded message
        source_data = await handle_source_message(client, message)
        if source_data:
            content = source_data['content']
            picture = source_data['picture']
            chat_id = source_data['chat_id']
            img_data = source_data['img_data']
    else:
        # Handle direct message
        picture = message.photo.file_id if message.photo else None
        if picture:
            img_data = await message.download(in_memory=True)
            setattr(img_data, "mode", "rb")
    
    # Get channel ad message
    channel_ad = await get_channel_ad_message(client)
    
    # Function to publish content to a specific platform
    async def publish_content(content_to_pub: str, platform: str, pic=None, img=None):
        try:
            if platform == "channel" and CHANNEL_ID:
                result = await publish_to_channel(
                    message, content_to_pub, pic, channel_ad, attached_message
                )
                if result:
                    # Schedule ad message forwarding if published to channel
                    asyncio.create_task(forward_ad_message(client))
                    
                # If publishing to Twitter is also requested, use channel message as reference
                if result and "twitter" in platforms:
                    await publish_to_twitter(
                        result, content_to_pub, img, channel_ad, attached_message
                    )
                return result
            elif platform == "group" and GROUP_ID:
                return await publish_to_group(
                    message, content_to_pub, pic, channel_ad, attached_message
                )
            elif platform == "twitter":
                return await publish_to_twitter(
                    message, content_to_pub, img, channel_ad, attached_message
                )
        except Exception as e:
            logging.error(f"Error publishing to {platform}: {str(e)}")
            return None

    # Filter enabled platforms
    enabled_platforms = get_enabled_platforms()
    if "twitter" not in platforms:  # Always allow Twitter if requested
        platforms = [p for p in platforms if p in enabled_platforms]
    
    if not platforms:
        logging.warning("No enabled platforms to publish to")
        return

    # Handle multiple config messages
    if is_multiple:
        parts = [p.strip() for p in content.split("\n") if len(p.strip()) > 10]
        for part in parts:
            # Format each config with new repository content and publish
            formatted_content = await format_config_message(client, part)
            for platform in platforms:
                await publish_content(formatted_content, platform, None, None)
            await asyncio.sleep(1)
    
    # Handle single message
    else:
        if use_repository:
            formatted_content = format_content_with_ad(content, chat_id) if content else ""
        else:
            formatted_content = format_content_with_ad(content) if content else ""
        
        # Publish to each platform
        for platform in platforms:
            fits, result, _ = check_message_length(formatted_content, platform, attached_message)
            if fits:
                await publish_content(result, platform, picture, img_data)
            else:
                # Split long messages
                max_length = 280 if platform == "twitter" else 4000
                split_parts = split_message(formatted_content, max_length, attached_message)
                for split_part in split_parts:
                    await publish_content(split_part, platform, picture, img_data)
                    await asyncio.sleep(1)

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
                caption=final_content + "\n\n" + (source_info if source_info else "") + "\n\n" + generate_tags("random3")
            )
        else:
            return await message._client.send_message(
                CHANNEL_ID,
                final_content + "\n\n" + (source_info if source_info else "") + "\n\n" + generate_tags("random3")
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
                caption=final_content + "\n\n" + (source_info if source_info else "") + "\n\n" + GROUP + generate_tags("random3")
            )
        else:
            await message._client.send_message(
                **kwargs,
                text=final_content + "\n\n" + (source_info if source_info else "") + "\n\n" + GROUP + generate_tags("random3")
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
        tweet_text = final_content + "\n" + (CHANNEL_URL if CHANNEL_URL else "") + generate_tags()
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
