import logging
import traceback
from pyrogram import Client, filters, types, enums
from ..utils.message_store import MESSAGE_STORE
from ..utils.platform_options import ask_platform_options
from ..utils.auth import user_check

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s [%(levelname)s]: %(message)s"
)

@user_check
async def message_handler(client: Client, message: types.Message):
    """Handle incoming messages (both forwarded and direct)."""
    try:
        if message.text is None and message.caption is None:
            await message.reply_text("❌ Please send a message with text or caption.")
            return
        
        message.reply_chat_action("typing")
        
        # Store message for later use
        MESSAGE_STORE[message.id] = message
        
        # If message is a reply to another message, store both
        if message.reply_to_message:
            attached_text = message.reply_to_message.text or message.reply_to_message.caption
            if attached_text:
                MESSAGE_STORE[f"attached_{message.id}"] = attached_text
        
        # Handle forwarded messages from channels
        if message.forward_from_chat and message.forward_from_chat.type == "channel":
            await ask_platform_options(message, is_forwarded=True)
            return
        
        # Handle direct config messages
        text = message.text or message.caption
        if text:
            # Check if it has multiple lines (might be multiple configs)
            if "\n" in text:
                buttons = [
                    [
                        types.InlineKeyboardButton(
                            "Single Message", 
                            callback_data=f"config_single_{message.id}"
                        ),
                        types.InlineKeyboardButton(
                            "Multiple Messages", 
                            callback_data=f"config_multiple_{message.id}"
                        )
                    ]
                ]
                msg_type = "multiple messages"
            else:
                buttons = [[
                    types.InlineKeyboardButton(
                        "Single Message", 
                        callback_data=f"config_single_{message.id}"
                    )
                ]]
                msg_type = "single message"
                
            markup = types.InlineKeyboardMarkup(buttons)
            await message.reply_text(
                f"How would you like to publish this {msg_type}?",
                reply_markup=markup,
                quote=True
            )
        else:
            await message.reply_text("❌ Message must contain text to be published.")
            
    except Exception as e:
        error_msg = f"❌ Error processing message: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        await message.reply_text(
            f"{error_msg}\n\nPlease try again or contact support if the issue persists.",
            parse_mode=enums.ParseMode.HTML
        )

@user_check
async def media_group_handler(client: Client, message: types.Message):
    """Handle media group messages."""
    try:
        message.reply_chat_action("upload_photo")
        
        # This method will be called multiple times
        # so we need to check if the group has been received
        media_group_id = message.media_group_id
        if media_group_id in MESSAGE_STORE:
            return
        
        # Check for attached message
        if message.reply_to_message:
            attached_text = message.reply_to_message.text or message.reply_to_message.caption
            if attached_text:
                MESSAGE_STORE[f"attached_{message.id}"] = attached_text
        
        # Process media group
        MESSAGE_STORE[media_group_id] = True
        groups = await message.get_media_group()
        
        # Validate media count
        if len(groups) > 4:
            await message.reply_text("❌ Maximum 4 media items allowed per message.")
            return
            
        files = []
        status_message = await message.reply_text("📥 Processing media files...")
        
        try:
            for i, group in enumerate(groups, 1):
                await status_message.edit_text(f"📥 Processing media {i}/{len(groups)}...")
                img_data = await group.download(in_memory=True)
                setattr(img_data, "mode", "rb")
                caption = group.caption
                if caption:
                    setattr(message, "text", caption)
                files.append(img_data)
            
            # Store the files for later use
            MESSAGE_STORE[f"media_{message.id}"] = files
            await status_message.edit_text("✅ Media processed successfully!")
            await ask_platform_options(message, is_forwarded=False)
            
        except Exception as e:
            error_msg = f"❌ Error processing media: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            await status_message.edit_text(
                f"{error_msg}\n\nPlease try again with different media files.",
                parse_mode=enums.ParseMode.HTML
            )
            
    except Exception as e:
        error_msg = f"❌ Error handling media group: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        await message.reply_text(
            f"{error_msg}\n\nPlease try again or contact support if the issue persists.",
                parse_mode=enums.ParseMode.HTML
        )

@user_check
async def single_media_handler(client: Client, message: types.Message):
    """Handle single media messages."""
    try:
        message.reply_chat_action("upload_photo")
        
        # Validate media type
        if not message.photo and not message.video and not message.document:
            await message.reply_text(
                "❌ Only photos, videos, and documents are supported.",
                parse_mode=enums.ParseMode.HTML
            )
            return
            
        # Check for attached message
        if message.reply_to_message:
            attached_text = message.reply_to_message.text or message.reply_to_message.caption
            if attached_text:
                MESSAGE_STORE[f"attached_{message.id}"] = attached_text
        
        status_message = await message.reply_text("📥 Processing media file...")
        try:
            img_data = await message.download(in_memory=True)
            setattr(img_data, "mode", "rb")
            MESSAGE_STORE[f"media_{message.id}"] = [img_data]
            
            await status_message.edit_text("✅ Media processed successfully!")
            await ask_platform_options(message, is_forwarded=False)
            
        except Exception as e:
            error_msg = f"❌ Error processing media: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            await status_message.edit_text(
                f"{error_msg}\n\nPlease try again with a different file.",
                parse_mode=enums.ParseMode.HTML
            )
            
    except Exception as e:
        error_msg = f"❌ Error handling media: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        await message.reply_text(
            f"{error_msg}\n\nPlease try again or contact support if the issue persists.",
            parse_mode=enums.ParseMode.HTML
        )

def get_attached_message(message_id: int) -> str:
    """Get attached message for a given message ID."""
    return MESSAGE_STORE.get(f"attached_{message_id}")
