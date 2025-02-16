"""
Utility modules for the TeleTweet bot.

This package contains utility modules that provide core functionality:

auth.py:
- User authentication and permission checking
- Authorization decorators

message_utils.py:
- Message content processing
- Length checking and truncation
- Text splitting utilities

message_store.py:
- Thread-safe message storage
- Temporary data management
- Message cleanup

publishing.py:
- Platform-specific message publishing
- Media handling
- Cross-platform posting

tags.py:
- Tag management and generation
- Tag file handling
- Random tag selection
"""

from .auth import user_check, get_auth_data, delete_tweet, is_admin
from .message_utils import (
    get_source_info,
    check_message_length,
    truncate_content,
    split_message
)
from .message_store import MESSAGE_STORE
from .publishing import (
    publish_to_channel,
    publish_to_group,
    publish_to_twitter,
    handle_publish
)
from .tags import generate_tags, add_tag, remove_tag

__all__ = [
    # Auth utilities
    'user_check',
    'get_auth_data',
    'delete_tweet',
    'is_admin',
    
    # Message utilities
    'get_source_info',
    'check_message_length',
    'truncate_content',
    'split_message',
    
    # Message store
    'MESSAGE_STORE',
    
    # Publishing utilities
    'publish_to_channel',
    'publish_to_group',
    'publish_to_twitter',
    'handle_publish',
    
    # Tag utilities
    'generate_tags',
    'add_tag',
    'remove_tag'
]
