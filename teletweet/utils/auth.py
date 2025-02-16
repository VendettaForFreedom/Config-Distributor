import functools
from typing import Callable, Any
import logging
from pyrogram import Client, types
from ..config import (
    CONFIG_CHANNEL_ID,
    CHANNEL_ID,
    GROUP_ID,
    SOURCE_CHANNEL_ID,
    ALLOW_USERS
)

def user_check(func: Callable) -> Callable:
    """Decorator to check if user is allowed to use the bot."""
    @functools.wraps(func)
    async def wrapper(client: Client, message: types.Message, *args: Any, **kwargs: Any):
        user_id = str(message.chat.id)
        logging.info("User %s is using the bot", user_id)
        
        # Check if user is in allowed list
        if user_id not in [CONFIG_CHANNEL_ID, CHANNEL_ID, GROUP_ID]:
            logging.info("User %s not in primary channels", user_id)
            if user_id not in ALLOW_USERS and user_id != SOURCE_CHANNEL_ID:
                logging.info("User %s not in allowed users", user_id)
                await message.reply_text("You're not allowed to use this bot.")
                return None
        
        logging.info("User %s is authenticated", user_id)
        return await func(client, message, *args, **kwargs)
    return wrapper

def get_auth_data(user_id: int) -> dict:
    """Get stored authentication data for a user."""
    try:
        # This is a placeholder - implement actual auth data storage/retrieval
        # Could use Redis, SQLite, or other storage methods
        return {}
    except Exception as e:
        logging.error(f"Error getting auth data for user {user_id}: {e}")
        return None

async def delete_tweet(message: types.Message) -> dict:
    """Delete a tweet."""
    try:
        # This is a placeholder - implement actual tweet deletion
        # Using the Twitter API
        return {"success": True}
    except Exception as e:
        logging.error(f"Error deleting tweet: {e}")
        return {"error": str(e)}

def is_admin(user_id: int) -> bool:
    """Check if user is an admin."""
    # You could expand this to check against a list of admin IDs
    # or check channel/group admin status
    return str(user_id) in ALLOW_USERS

def log_user_action(user_id: int, action: str):
    """Log user actions for monitoring."""
    logging.info(f"User {user_id} performed action: {action}")

def check_user_permissions(user_id: int, required_permissions: list) -> bool:
    """Check if user has required permissions."""
    # This is a placeholder - implement actual permission checking
    # Could be based on roles, group membership, etc.
    return is_admin(user_id)
