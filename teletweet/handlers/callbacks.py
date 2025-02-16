import asyncio
import logging
from pyrogram import Client, filters, types
from ..utils.message_store import MESSAGE_STORE
from ..utils.publishing import (
    handle_publish,
    publish_to_channel,
    publish_to_group,
    publish_to_twitter,
    get_enabled_platforms
)
from ..utils.constants import tweet_length
from ..utils.platform_options import ask_platform_options, show_preview
from ..utils.message_utils import check_message_length, split_message
from .messages import get_attached_message

async def config_callback(client: Client, call: types.CallbackQuery, message, action):
    """Handle config type selection callback"""
    is_multiple = action == "multiple"
    await ask_platform_options(message, is_forwarded=False, is_multiple=is_multiple)

async def preview_callback(client: Client, call: types.CallbackQuery, message):
    """Handle preview request callback"""
    try:
        message_id = message.id
        attached_message = get_attached_message(message_id)
        await show_preview(message, attached_message)
        
    except Exception as e:
        error_msg = f"Error generating preview: {str(e)}"
        logging.error(error_msg)
        await call.message.edit_text(error_msg)

async def back_to_options_callback(client: Client, call: types.CallbackQuery, message):
    """Handle back to options callback"""
    try:
        # We pass is_forwarded=False and is_multiple=False since these are preserved in the message ID
        await ask_platform_options(message)
        
    except Exception as e:
        error_msg = f"Error returning to options: {str(e)}"
        logging.error(error_msg)
        await call.message.edit_text(error_msg)

async def platform_callback(client: Client, call: types.CallbackQuery, platform, is_forwarded, is_multiple, message):
    """Handle platform selection callback"""
    try:
        message_id = message.id
        msg_id_str = str(message_id)
        # Get attached message if exists
        attached_message = get_attached_message(message_id)
        
        # Get enabled platforms
        enabled_platforms = get_enabled_platforms()
        
        # Determine platforms to publish to
        platforms = []
        if platform == "channel" and "channel" in enabled_platforms:
            platforms = ["channel"]
        elif platform == "group" and "group" in enabled_platforms:
            platforms = ["group"]
        elif platform == "twitter":
            platforms = ["twitter"]
        elif platform == "all":
            platforms = enabled_platforms + ["twitter"]
        
        # If no platforms are enabled but Twitter was chosen, still allow it
        if not platforms and platform == "twitter":
            platforms = ["twitter"]
        
        # If no valid platforms, inform user
        if not platforms:
            await call.message.edit_text(
                "No platforms are currently configured for publishing. "
                "Please set up channels/groups in configuration or choose Twitter only."
            )
            return
        
        # Start publishing status message
        status_msg = await call.message.edit_text("Publishing in progress...")

        # First, try Twitter if selected
        if "twitter" in platforms:
            result = await publish_to_twitter(
                message,
                message.text or message.caption,
                None,  # media will be handled by handle_publish
                None,  # source info will be handled by handle_publish
                attached_message
            )
            if "error" in result:
                error_msg = f"Error publishing to Twitter: {result['error']}"
                logging.error(error_msg)
                await status_msg.edit_text(error_msg)
                return

        # Continue with other platforms
        await handle_publish(
            client,
            message,
            platforms,
            is_multiple=is_multiple,
            attached_message=attached_message
        )
        
        # Update status message
        await status_msg.edit_text("Publishing completed successfully!")

        # Clean up message store safely
        msg_id_str = str(message.id)
        truncation_keys = [k for k in MESSAGE_STORE.keys() if isinstance(k, str) and k.startswith(f"trunc_{msg_id_str}")]
        if not truncation_keys:
            MESSAGE_STORE.pop(message.id, None)
            MESSAGE_STORE.pop(f"attached_{msg_id_str}", None)

    except Exception as e:
        error_msg = f"Error in platform callback: {str(e)}"
        logging.error(error_msg)
        await call.message.edit_text(error_msg)

async def truncation_callback(client: Client, call: types.CallbackQuery, method, msg_id, platform, stored_data):
    """Handle truncation option callback"""
    try:
        content = stored_data["content"]
        options = stored_data["options"]
        picture = stored_data["picture"]
        img_data = stored_data["img_data"]
        source_info = stored_data["source_info"]
        
        # Get attached message if it exists
        attached_message = get_attached_message(int(msg_id))
        
        if method in ["auto", "smart"]:
            # Use pre-truncated content
            content_to_publish = options[0] if method == "auto" else options[1]
            
            result = None
            if platform == "channel":
                result = await publish_to_channel(
                    call.message,
                    content_to_publish,
                    picture,
                    source_info,
                    attached_message
                )
            elif platform == "group":
                result = await publish_to_group(
                    call.message,
                    content_to_publish,
                    picture,
                    source_info,
                    attached_message
                )
            elif platform == "twitter":
                result = await publish_to_twitter(
                    call.message,
                    content_to_publish,
                    img_data,
                    source_info,
                    attached_message
                )
                if "error" in result:
                    error_msg = f"Error publishing truncated message to Twitter: {result['error']}"
                    logging.error(error_msg)
                    await call.message.edit_text(error_msg)
                    return
            
            await call.message.edit_text(f"Truncated message published to {platform}!")
            MESSAGE_STORE.pop(f"trunc_{msg_id}_{platform}", None)
            
        elif method == "split":
            max_length = tweet_length if platform == "twitter" else 4000
            split_parts = split_message(content, max_length, attached_message)
            
            for part in split_parts:
                try:
                    if platform == "channel":
                        await publish_to_channel(
                            call.message,
                            part,
                            picture,
                            source_info,
                            attached_message if part == split_parts[-1] else None
                        )
                    elif platform == "group":
                        await publish_to_group(
                            call.message,
                            part,
                            picture,
                            source_info,
                            attached_message if part == split_parts[-1] else None
                        )
                    elif platform == "twitter":
                        result = await publish_to_twitter(
                            call.message,
                            part,
                            img_data,
                            source_info,
                            attached_message if part == split_parts[-1] else None
                        )
                        if "error" in result:
                            error_msg = f"Error publishing split message to Twitter: {result['error']}"
                            logging.error(error_msg)
                            await call.message.edit_text(error_msg)
                            return
                except Exception as e:
                    error_msg = f"Error publishing split part: {str(e)}"
                    logging.error(error_msg)
                    await call.message.edit_text(error_msg)
                    return
                await asyncio.sleep(1)
            
            await call.message.edit_text(f"Split message published to {platform}!")
            MESSAGE_STORE.pop(f"trunc_{msg_id}_{platform}", None)

        # Clean up message data if all processing is complete
        msg_id_str = str(msg_id)
        truncation_keys = [k for k in MESSAGE_STORE.keys() if isinstance(k, str) and k.startswith(f"trunc_{msg_id_str}")]
        if not truncation_keys:
            MESSAGE_STORE.pop(int(msg_id), None)
            MESSAGE_STORE.pop(f"attached_{msg_id}", None)

    except Exception as e:
        error_msg = f"Error in truncation callback: {str(e)}"
        logging.error(error_msg)
        await call.message.edit_text(error_msg)
