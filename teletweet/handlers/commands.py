from pyrogram import Client, filters, types, enums
from ..utils.auth import get_auth_data
from ..utils.tweet import get_me, delete_tweet

# Help message
HELP_TEXT = """
<b>Available Commands</b>
/start - Start the bot
/help - Show this help message
/delete - Delete a tweet (reply to a tweet)
/status - Check Twitter connection status
"""
from ..config import ALLOW_USERS

async def start_handler(client: Client, message: types.Message):
    """Handle /start command"""
    message.reply_chat_action("typing")
    if get_auth_data(message.chat.id):
        await message.reply_text("Send me a message or forward one from a channel!")
        return
    msg = "Welcome to Config-Distributor. " "This bot will connect you from Telegram Bot to Twitter "
    if ALLOW_USERS != [""]:
        msg += "\n\nTHIS BOT IS ONLY AVAILABLE TO CERTAIN USERS. Contact creator for help."
    await message.reply_text(msg)

async def help_handler(client: Client, message: types.Message):
    """Handle /help command"""
    message.reply_chat_action("typing")
    help_text = """<b>Available Commands</b>:
    
/start - Start the bot
/help - Show this help message
/delete - Delete a tweet (reply to a tweet)
/status - Check Twitter connection status

<b>You can</b>:
1. Forward a message from any channel
2. Send configs directly to publish them

For configs, you can:
- Send a single config
- Send multiple configs in separate lines
"""
    await message.reply_text(help_text, parse_mode=enums.ParseMode.HTML)

async def status_handler(client: Client, message: types.Message):
    """Handle /status command to check Twitter connection"""
    message.reply_chat_action("typing")
    try:
        result = await get_me(message.chat.id)
        if isinstance(result, dict) and "error" in result:
            await message.reply_text(
                f"❌ Twitter connection failed:\n<code>{result['error']}</code>",
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                f"✅ Successfully connected to Twitter!\nAccount: {result}",
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        await message.reply_text(
            f"❌ Error checking Twitter status:\n<code>{str(e)}</code>",
                parse_mode=enums.ParseMode.HTML
        )

async def delete_handler(client: Client, message: types.Message):
    """Handle /delete command"""
    message.reply_chat_action("typing")
    if not message.reply_to_message:
        await message.reply_text("Reply to some message and delete.")
        return
    result = await delete_tweet(message)
    if result.get("error"):
        resp = f"❌ Error: `{result['error']}`"
        await message.reply_text(resp, quote=True, parse_mode=enums.ParseMode.HTML)
    else:
        resp = f"🗑 Your tweet has been deleted.\n"
        await message.reply_to_message.edit_text(resp, parse_mode=enums.ParseMode.HTML)
