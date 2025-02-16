# TeleTweet Bot API Documentation

## Core Functions and Classes

### TeleTweetBot (tweetbot.py)

Main bot class that initializes and runs the Telegram bot.

```python
class TeleTweetBot:
    def __init__(self)
    """Initialize bot with API credentials and setup handlers."""

    def setup_handlers(self)
    """Configure message, command, and callback handlers."""

    def run(self)
    """Start the bot and begin processing messages."""
```

## Message Handlers (handlers/)

### Command Handlers (commands.py)

```python
async def start_handler(client: Client, message: Message)
"""Handle /start command. Introduces bot functionality."""

async def help_handler(client: Client, message: Message)
"""Handle /help command. Shows available commands and features."""

async def delete_handler(client: Client, message: Message)
"""Handle /delete command. Deletes a tweet when replying to a message."""
```

### Message Handlers (messages.py)

```python
async def message_handler(client: Client, message: Message)
"""Handle incoming text messages and forwards.
- Detects forwarded messages
- Handles direct config messages
- Provides publishing options
"""

async def media_group_handler(client: Client, message: Message)
"""Handle media groups (multiple photos).
- Groups media together
- Maintains captions
- Provides publishing options
"""

async def single_media_handler(client: Client, message: Message)
"""Handle single media messages.
- Supports photos, documents, videos, stickers
- Preserves captions
- Provides publishing options
"""
```

### Callback Handlers (callbacks.py)

```python
async def config_callback(client: Client, call: CallbackQuery, message: Message, action: str)
"""Handle config type selection.
- Single message handling
- Multiple message handling
"""

async def platform_callback(client: Client, call: CallbackQuery, platform: str, is_forwarded: bool, is_multiple: bool, message: Message)
"""Handle platform selection for publishing.
- Channel publishing
- Group publishing
- Twitter publishing
- Multi-platform publishing
"""

async def truncation_callback(client: Client, call: CallbackQuery, method: str, msg_id: int, platform: str, stored_data: dict)
"""Handle message truncation options.
- Auto truncation
- Smart truncation
- Message splitting
"""
```

## Utility Functions (utils/)

### Message Utilities (message_utils.py)

```python
def get_source_info(message: Message) -> Tuple[str, str]
"""Extract source channel information from forwarded message.
Returns: (source_url, reference)
"""

def check_message_length(content: str, platform: str) -> Tuple[bool, Union[str, List[str]], Optional[int]]
"""Check if message fits platform limits.
Returns: (fits, content/options, excess_length)
"""

def truncate_at_sentence(text: str, limit: int) -> str
"""Truncate text at nearest sentence boundary.
Uses: periods, exclamation marks, question marks
"""

def split_message(content: str, max_length: int) -> List[str]
"""Split message into parts that fit length limit.
Preserves: word boundaries, formatting
"""
```

### Publishing Utilities (publishing.py)

```python
async def publish_to_channel(message: Message, content: str, picture=None, source_info=None) -> Message
"""Publish message to Telegram channel.
- Supports media
- Adds source attribution
- Handles tags
"""

async def publish_to_group(message: Message, content: str, picture=None, source_info=None) -> bool
"""Publish message to Telegram group.
- Supports media
- Adds source attribution
- Handles tags
- Uses topic if specified
"""

async def publish_to_twitter(message: Message, content: str, media=None, source_info=None) -> dict
"""Publish message to Twitter.
- Handles media upload
- Respects character limit
- Adds source attribution
- Returns tweet data
"""
```

### Tag Management (tags.py)

```python
def load_tags() -> List[str]
"""Load tags from tags file."""

def generate_tags(mode: Optional[str] = None) -> str
"""Generate tag string based on mode.
Modes:
- first5random: Random selection of 5 tags
- None: All tags
"""

def add_tag(tag: str) -> bool
"""Add new tag to tags file."""

def remove_tag(tag: str) -> bool
"""Remove tag from tags file."""
```

### Message Store (message_store.py)

```python
class MessageStore:
    """Thread-safe message storage.

    Methods:
    - __getitem__(key): Get stored message
    - __setitem__(key, value): Store message
    - get(key, default=None): Get with default
    - pop(key, default=None): Remove and return
    - cleanup_expired(max_age=3600): Remove old messages
    """
```

### Authentication (auth.py)

```python
def user_check(func: Callable) -> Callable
"""Decorator to check user permissions.
- Checks channel membership
- Verifies whitelist
- Logs access attempts
"""

def get_auth_data(user_id: int) -> dict
"""Get stored authentication data for user."""

def is_admin(user_id: int) -> bool
"""Check if user has admin privileges."""

def check_user_permissions(user_id: int, required_permissions: list) -> bool
"""Check if user has specific permissions."""
```

## Events and Flow

1. Message Reception:

   ```
   message_handler -> check permissions -> store message -> process type
   ```

2. Config Processing:

   ```
   config selection -> platform selection -> length check -> publishing
   ```

3. Media Handling:

   ```
   media detection -> group check -> store files -> publishing options
   ```

4. Length Management:
   ```
   content check -> offer options -> handle selection -> publish parts
   ```

## Error Handling

Errors are logged and handled at multiple levels:

1. Handler level - Catches message processing errors
2. Publishing level - Handles platform-specific errors
3. Storage level - Manages data consistency
4. Network level - Handles connection issues

Each error is:

- Logged with context
- Reported appropriately
- Handled gracefully
- Cleaned up properly

## Best Practices

1. Message Storage:

   - Store only necessary data
   - Clean up regularly
   - Use thread-safe operations

2. Publishing:

   - Verify content before sending
   - Handle platform limits
   - Maintain attributions

3. Error Handling:

   - Log comprehensive details
   - Provide user feedback
   - Clean up resources

4. Performance:
   - Avoid redundant operations
   - Clean up temporary data
   - Use async operations appropriately
