from typing import Optional
from pyrogram import types
from .publishing import get_enabled_platforms, generate_preview

async def ask_platform_options(message: types.Message, is_forwarded=False, is_multiple=False):
    """Ask user where to publish the message."""
    msg_id = message.id
    enabled_platforms = get_enabled_platforms()
    buttons = []
    
    # Add channel/group buttons only if configured
    platform_row = []
    if "channel" in enabled_platforms:
        platform_row.append(
            types.InlineKeyboardButton(
                "Channel", 
                callback_data=f"pub_channel_{is_forwarded}_{is_multiple}_{msg_id}"
            )
        )
    if "group" in enabled_platforms:
        platform_row.append(
            types.InlineKeyboardButton(
                "Group", 
                callback_data=f"pub_group_{is_forwarded}_{is_multiple}_{msg_id}"
            )
        )
    
    # Add platform row if any platforms are configured
    if platform_row:
        buttons.append(platform_row)
        
        # Add "All Platforms" button if both channel and group are available
        if len(platform_row) > 1:
            buttons.append([
                types.InlineKeyboardButton(
                    "All Platforms", 
                    callback_data=f"pub_all_{is_forwarded}_{is_multiple}_{msg_id}"
                )
            ])
    
    # Add Twitter button if configured
    if "twitter" in enabled_platforms:
        twitter_button = [
            types.InlineKeyboardButton(
                "Twitter Only", 
                callback_data=f"pub_twitter_{is_forwarded}_{is_multiple}_{msg_id}"
            )
        ]
        buttons.append(twitter_button)
        
    markup = types.InlineKeyboardMarkup(buttons) if buttons else None
    
    # Customize message based on available platforms
    # Add preview button if any platforms are enabled
    if enabled_platforms:
        preview_button = [
            types.InlineKeyboardButton(
                "📝 Preview", 
                callback_data=f"preview_{is_forwarded}_{is_multiple}_{msg_id}"
            )
        ]
        buttons.append(preview_button)
    
    if not enabled_platforms:
        msg_text = "No platforms are configured. Please configure Twitter credentials or Telegram channels/groups."
    elif "twitter" not in enabled_platforms and not buttons:
        msg_text = "Twitter is not configured and no Telegram channels/groups are set up."
    else:
        msg_text = "Where would you like to publish this message?"
        
    await message.reply_text(
        msg_text,
        reply_markup=markup,
        quote=True
    )

async def show_preview(message: types.Message, attached_message: Optional[str] = None):
    """Show preview of how message will look on each platform."""
    previews = await generate_preview(message, attached_message)
    
    if not previews:
        await message.reply_text(
            "No platforms configured to generate preview.",
            quote=True
        )
        return
        
    preview_text = "\n\n---\n\n".join(previews.values())
    
    buttons = [[
        types.InlineKeyboardButton(
            "🔄 Back to Options",
            callback_data=f"back_options_{message.id}"
        )
    ]]
    
    await message.reply_text(
        preview_text,
        reply_markup=types.InlineKeyboardMarkup(buttons),
        quote=True
    )
