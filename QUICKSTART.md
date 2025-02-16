# TeleTweet Bot Quick Start Guide

## Setup Steps

1. Make the run script executable:

```bash
chmod +x run.sh
```

2. Run the setup script:

```bash
./run.sh
```

3. When prompted, edit the `.env` file with your credentials:

### Getting Telegram Credentials:

1. Go to https://my.telegram.org/apps
2. Create a new application
3. Copy APP_ID and APP_HASH
4. Get BOT_TOKEN from @BotFather

### Getting Channel/Group IDs:

1. Forward a message from each channel/group to @userinfobot
2. Note the IDs (they start with `-100`)
3. Fill in the IDs in `.env`:
   - CONFIG_CHANNEL_ID: Channel for configs
   - CHANNEL_ID: Main channel
   - GROUP_ID: Discussion group
   - SOURCE_CHANNEL_ID: Source channel
   - SOURCE_REPOSITORY_CHANNEL_ID: Repository channel

### Setting Up Twitter:

1. Go to https://developer.twitter.com
2. Create a new app
3. Generate API keys and tokens
4. Fill in the Twitter credentials in `.env`

### Adding Allowed Users:

- Add comma-separated Telegram user IDs to ALLOW_USERS
- Get your ID by sending a message to @userinfobot

## Running the Bot

1. Start the bot:

```bash
./run.sh
```

2. Test the bot:
   - Send /start to your bot
   - Forward a message to test forwarding
   - Send a config to test config publishing

## Troubleshooting

If you encounter issues:

1. Check logs for errors

```bash
tail -f teletweet.log
```

2. Verify permissions:

   - Bot is admin in all channels
   - Bot has post/edit permissions
   - Your user ID is in ALLOW_USERS

3. Common issues:
   - Invalid credentials: Check .env values
   - Permission errors: Verify bot admin status
   - Connection errors: Check internet connection

## Quick Commands

- `/start` - Initialize the bot
- `/help` - Show help message
- `/delete` - Delete a tweet (reply to message)

## Testing Attached Messages

1. Forward a message from any channel
2. Reply to the forwarded message with additional text
3. Bot will:
   - Calculate combined length
   - Offer truncation options if needed
   - Publish both messages together

## Support

If you need help:

1. Check the full documentation in docs/
2. Create an issue on GitHub
3. Contact the maintainers

## Stopping the Bot

To stop the bot:

```bash
pkill -f "teletweet.tweetbot"
```

To restart:

```bash
./run.sh
```
