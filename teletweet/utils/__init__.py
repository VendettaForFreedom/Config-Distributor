"""
TeleTweet utility functions
"""

# Authentication and user management
from .auth import user_check, get_auth_data

# Message formatting and handling
from .message_format import (
    format_repository_message,
    format_content_with_ad,
    get_channel_ad_message,
    handle_source_message,
    format_config_message,
    format_config_channel_message,
    truncate_content
)

# Publishing functionality
from .publishing import (
    handle_publish,
    publish_to_channel,
    publish_to_group,
    publish_to_twitter,
    get_enabled_platforms
)

# Platform specific options
from .platform_options import ask_platform_options

# Preview functionality
from .preview import show_preview, generate_preview

# Repository management
from .repository import get_random_message_pair

# Tag management
from .tags import generate_tags, add_tag, remove_tag

# Task management
from .delayed_tasks import forward_ad_message

# Message storage
from .message_store import MESSAGE_STORE

# Message utilities
from .message_utils import (
    check_message_length,
    split_message,
    combine_messages,
    calculate_total_length
)

__all__ = [
    # Auth
    'user_check',
    'get_auth_data',

    # Message format
    'format_repository_message',
    'format_content_with_ad',
    'get_channel_ad_message',
    'handle_source_message',
    'format_config_message',
    'format_config_channel_message',
    'truncate_content',

    # Publishing
    'handle_publish',
    'publish_to_channel',
    'publish_to_group',
    'publish_to_twitter',
    'get_enabled_platforms',

    # Platform options
    'ask_platform_options',

    # Preview
    'show_preview',
    'generate_preview',

    # Repository
    'get_random_message_pair',

    # Tags
    'generate_tags',
    'add_tag',
    'remove_tag',

    # Tasks
    'forward_ad_message',

    # Storage
    'MESSAGE_STORE',

    # Utils
    'check_message_length',
    'split_message',
    'combine_messages',
    'calculate_total_length'
]
