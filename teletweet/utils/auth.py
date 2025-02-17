import logging
import tweepy
from functools import wraps
from ..config import (
    CONFIG_CHANNEL_ID,
    CHANNEL_ID,
    GROUP_ID,
    SOURCE_CHANNEL_ID,
    ALLOW_USERS
)
from .tweet import get_me

def user_check(func):
    """Decorator to check if user is allowed to use the bot."""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = str(message.chat.id)
        
        logging.info("User %s is using the bot", user_id)
        
        if user_id not in [CONFIG_CHANNEL_ID, CHANNEL_ID, GROUP_ID]:
            logging.info("User %s got into the first if", user_id)
            if user_id in ALLOW_USERS or user_id == SOURCE_CHANNEL_ID:
                logging.info("User %s got into the second if", user_id)
                logging.info("User %s is authenticated!")
                return await func(client, message, *args, **kwargs)
            else:
                logging.info("User %s got into the else", user_id)
                logging.info("User %s is not authenticated!")
                await message.reply_text("You're not allowed to use this bot.")
                return
    return wrapper

def get_auth_data(chat_id: int) -> dict:
    """Get Twitter auth data for a chat."""
    try:
        result = get_me(chat_id)
        if isinstance(result, dict) and "error" in result:
            return None
        return result
    except tweepy.errors.TweepyException:
        return None
