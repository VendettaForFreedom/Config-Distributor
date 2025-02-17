"""
TeleTweet - A Telegram bot to publish content across multiple platforms
"""

from . import utils
from . import handlers
from .config import (
    APP_ID,
    APP_HASH,
    BOT_TOKEN,
    CHANNEL_ID,
    GROUP_ID,
    GROUP_TOPIC_ID,
    CONFIG_CHANNEL_ID,
    SOURCE_CHANNEL_ID,
    SOURCE_REPOSITORY_CHANNEL_ID,
    ALLOW_USERS
)

__version__ = "2.0.0"
__author__ = "Benny <benny.think@gmail.com>"

__all__ = [
    'utils',
    'handlers',
    'APP_ID',
    'APP_HASH',
    'BOT_TOKEN',
    'CHANNEL_ID',
    'GROUP_ID',
    'GROUP_TOPIC_ID',
    'CONFIG_CHANNEL_ID',
    'SOURCE_CHANNEL_ID',
    'SOURCE_REPOSITORY_CHANNEL_ID',
    'ALLOW_USERS'
]
