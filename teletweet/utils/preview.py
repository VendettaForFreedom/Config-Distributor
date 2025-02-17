import logging
from typing import Dict, Optional
from pyrogram import types
from ..config import GROUP, CHANNEL_URL
from .message_format import format_content_with_ad, get_channel_ad_message
from .message_utils import check_message_length, combine_messages
from .tags import generate_tags
from .publishing import get_enabled_platforms

async def generate_preview(
    message: types.Message,
    attached_message: Optional[str] = None
) -> Dict[str, str]:
    """Generate preview text for each enabled platform."""
    content = message.text or message.caption
    enabled = get_enabled_platforms()
    previews = {}
    
    # Get channel ad message for previews
    channel_ad = await get_channel_ad_message(message._client)
    
    if "channel" in enabled:
        final_content = combine_messages(content, attached_message) if attached_message else content
        final_content = format_content_with_ad(final_content)
        channel_text = (
            final_content + "\n\n" + 
            (channel_ad if channel_ad else "") + "\n\n" + 
            generate_tags("random3")
        )
        fits, _, over = check_message_length(channel_text, "channel")
        previews["channel"] = f"Channel Preview{' (Too Long!)' if not fits else ''}:\n\n{channel_text[:4000]}"
        if not fits:
            previews["channel"] += f"\n\n[{over} characters over limit]"
    
    if "group" in enabled:
        final_content = combine_messages(content, attached_message) if attached_message else content
        final_content = format_content_with_ad(final_content)
        group_text = (
            final_content + "\n\n" +
            (channel_ad if channel_ad else "") + "\n\n" +
            GROUP + generate_tags("random3")
        )
        fits, _, over = check_message_length(group_text, "group")
        previews["group"] = f"Group Preview{' (Too Long!)' if not fits else ''}:\n\n{group_text[:4000]}"
        if not fits:
            previews["group"] += f"\n\n[{over} characters over limit]"
            
    if "twitter" in enabled:
        final_content = combine_messages(content, attached_message) if attached_message else content
        final_content = format_content_with_ad(final_content)
        tweet_text = (
            final_content + "\n" + 
            CHANNEL_URL + 
            generate_tags()
        )
        fits, _, over = check_message_length(tweet_text, "twitter")
        previews["twitter"] = f"Twitter Preview{' (Too Long!)' if not fits else ''}:\n\n{tweet_text[:280]}"
        if not fits:
            previews["twitter"] += f"\n\n[{over} characters over limit]"
    
    return previews

async def show_preview(message: types.Message, attached_message: Optional[str] = None):
    """Show preview of how message will look on each platform."""
    previews = await generate_preview(message, attached_message)
    
    if not previews:
        await message.reply_text(
            "No platforms configured to generate preview.",
            quote=True
        )
        return
    
    # Format preview text with proper section headers and Persian text
    preview_sections = []
    
    if "channel" in previews:
        preview_sections.append(f"📢 Channel Preview (Main Channel):\n{'-' * 40}\n{previews['channel']}")
    
    if "group" in previews:
        preview_sections.append(f"👥 Group Preview (Discussion Group):\n{'-' * 40}\n{previews['group']}")
    
    if "twitter" in previews:
        preview_sections.append(f"🐦 Twitter Preview:\n{'-' * 40}\n{previews['twitter']}")
    
    preview_text = "\n\n" + "\n\n".join(preview_sections)
    
    from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    buttons = [[
        InlineKeyboardButton(
            "🔄 Back to Options",
            callback_data=f"back_options_{message.id}"
        )
    ]]
    
    await message.reply_text(
        preview_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )
