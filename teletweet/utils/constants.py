"""Constants used throughout the bot."""

# Platform limits
tweet_length = 280  # Maximum tweet length
message_window = 300  # Time window (in seconds) for considering messages as multi-part
max_telegram_length = 4000  # Maximum Telegram message length

# Message formatting
line_separator = "\n\n"  # Standard line separator between sections
bullet_point = "• "  # Bullet point for lists
truncation_indicator = "..."  # Indicator for truncated text

# Time constants
ad_forward_delay = 3600  # Delay before forwarding ad message (1 hour)
message_spacing = 1  # Delay between messages in seconds
media_group_timeout = 5  # Time to wait for all media group messages

__all__ = [
    'tweet_length',
    'message_window',
    'max_telegram_length',
    'line_separator',
    'bullet_point',
    'truncation_indicator',
    'ad_forward_delay',
    'message_spacing',
    'media_group_timeout'
]
