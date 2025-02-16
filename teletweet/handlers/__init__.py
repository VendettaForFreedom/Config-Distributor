"""
Message handlers for the TeleTweet bot.

This package contains handler modules for different types of messages:
- commands.py: Handles bot commands (/start, /help, /delete)
- messages.py: Handles incoming messages (text, media, forwards)
- callbacks.py: Handles callback queries from inline buttons

The handlers implement the bot's core functionality:
- Command processing
- Message forwarding
- Platform selection
- Message length management
- Media handling
"""

from .commands import start_handler, help_handler, delete_handler
from .messages import message_handler, media_group_handler, single_media_handler
from .callbacks import config_callback, platform_callback, truncation_callback

__all__ = [
    'start_handler',
    'help_handler',
    'delete_handler',
    'message_handler',
    'media_group_handler',
    'single_media_handler',
    'config_callback',
    'platform_callback',
    'truncation_callback'
]
