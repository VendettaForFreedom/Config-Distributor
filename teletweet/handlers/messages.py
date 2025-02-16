from pyrogram import Client, filters, types
from ..utils.message_store import MESSAGE_STORE
from ..utils.platform_options import ask_platform_options
from ..utils.auth import user_check

@user_check
async def message_handler(client: Client, message: types.Message):
    """Handle incoming messages (both forwarded and direct)."""
    if message.text is None and message.caption is None:
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
        else:
            buttons = [[
                types.InlineKeyboardButton(
                    "Single Message", 
                    callback_data=f"config_single_{message.id}"
                )
            ]]
            
        markup = types.InlineKeyboardMarkup(buttons)
        await message.reply_text(
            "How would you like to publish this config?",
            reply_markup=markup,
            quote=True
        )

@user_check
async def media_group_handler(client: Client, message: types.Message):
    """Handle media group messages."""
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
    
    MESSAGE_STORE[media_group_id] = True
    groups = await message.get_media_group()
    files = []
    
    for group in groups:
        img_data = await group.download(in_memory=True)
        setattr(img_data, "mode", "rb")
        caption = group.caption
        if caption:
            setattr(message, "text", caption)
        files.append(img_data)
    
    # Store the files for later use
    MESSAGE_STORE[f"media_{message.id}"] = files
    await ask_platform_options(message, is_forwarded=False)

@user_check
async def single_media_handler(client: Client, message: types.Message):
    """Handle single media messages."""
    message.reply_chat_action("upload_photo")
    
    # Check for attached message
    if message.reply_to_message:
        attached_text = message.reply_to_message.text or message.reply_to_message.caption
        if attached_text:
            MESSAGE_STORE[f"attached_{message.id}"] = attached_text
    
    img_data = await message.download(in_memory=True)
    setattr(img_data, "mode", "rb")
    MESSAGE_STORE[f"media_{message.id}"] = [img_data]
    
    await ask_platform_options(message, is_forwarded=False)

def get_attached_message(message_id: int) -> str:
    """Get attached message for a given message ID."""
    return MESSAGE_STORE.get(f"attached_{message_id}")
