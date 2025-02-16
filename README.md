# TeleTweet Bot

A Telegram bot that handles message forwarding to multiple platforms with advanced message management features.

## Features

### 1. Message Handling

#### Forwarded Messages

- Automatically detects messages forwarded from channels
- Preserves original source channel information
- Maintains correct message references
- Supports media (photos, documents, videos, stickers)

#### Direct Messages

- Single config messages
- Multiple config messages (line-separated)
- Media messages with captions
- Media groups (multiple photos)

### 2. Publishing Options

#### Platforms

- Telegram Channel
- Telegram Group
- Twitter
- All Platforms simultaneously

#### Message Formats

- Text only
- Photo with caption
- Multiple photos with caption
- Documents/Videos with caption

### 3. Length Management

When messages exceed platform limits (Twitter: 280 chars, Telegram: 4000 chars), the bot offers three options:

1. **Auto Truncate**: Simple truncation with "..."
2. **Smart Truncate**: Intelligent truncation at:
   - Sentence boundaries (., !, ?)
   - Paragraph breaks
   - Word boundaries
3. **Split Message**: Divides content into multiple messages while preserving:
   - Media attachments
   - Source references
   - Formatting

### 4. Source Attribution

- Preserves original channel references
- Format: https://t.me/username/message_id
- Handles both public and private channel forwards
- Maintains proper attribution in splits/truncations

### 5. Tag Management

- Random tag selection
- First 5 random tags option
- All tags option
- Tag file management (add/remove)
- Per-platform tag formatting

### 6. User Management

- Whitelist-based access control
- Channel/Group member verification
- Admin privileges
- User action logging
- Permission-based command access

## Commands

- `/start` - Start the bot and get introduction
- `/help` - Show available commands and features
- `/delete` - Delete a tweet (reply to message)

## Interactive Flow

1. **Message Reception**

   - Forward a message from channel
   - Send direct config(s)
   - Send media content

2. **Publishing Type Selection** (for configs)

   - Single Message
   - Multiple Messages (for multi-line content)

3. **Platform Selection**

   - Channel
   - Group
   - Twitter
   - All Platforms

4. **Length Management** (if needed)
   - Auto Truncate
   - Smart Truncate
   - Split Message

## Message Store

The bot implements a thread-safe message store for:

- Temporary message caching
- Media group handling
- Callback data storage
- Auto-cleanup after 1 hour

## Error Handling

- Platform-specific error handling
- Failed message retry options
- Error logging and reporting
- User-friendly error messages

## Technical Details

### Project Structure

```
teletweet/
├── __init__.py           # Package initialization
├── tweetbot.py           # Main bot class
├── config.py             # Configuration settings
├── handlers/             # Message handlers
│   ├── __init__.py
│   ├── commands.py       # Command handlers
│   ├── messages.py       # Message handlers
│   └── callbacks.py      # Callback handlers
└── utils/               # Utility modules
    ├── __init__.py
    ├── auth.py          # Authentication
    ├── message_utils.py # Message processing
    ├── message_store.py # Data storage
    ├── publishing.py    # Platform publishing
    └── tags.py         # Tag management
```

### Dependencies

- pyrogram: Telegram client library
- tweepy: Twitter API client
- python-dotenv: Environment configuration

### Configuration

Required environment variables:

```
APP_ID=your_telegram_app_id
APP_HASH=your_telegram_app_hash
BOT_TOKEN=your_telegram_bot_token
CHANNEL_ID=your_channel_id
GROUP_ID=your_group_id
SOURCE_CHANNEL_ID=source_channel_id
ALLOW_USERS=comma_separated_user_ids
```

## Usage Examples

1. Forward a channel post:

   ```
   1. Forward any message from a channel to the bot
   2. Select target platform(s)
   3. Bot handles length and publishing automatically
   ```

2. Send configs:

   ```
   1. Send single or multiple configs
   2. Choose publishing mode (single/multiple)
   3. Select target platform(s)
   4. Handle any length issues if prompted
   ```

3. Send media:
   ```
   1. Send photo/video/document
   2. Add caption if needed
   3. Select target platform(s)
   4. Bot handles media upload and caption formatting
   ```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
