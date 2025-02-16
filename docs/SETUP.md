# TeleTweet Bot Setup Guide

This guide will walk you through setting up and deploying the TeleTweet bot.

## Prerequisites

1. Python 3.8 or higher
2. A Telegram account
3. A Twitter Developer Account
4. pip (Python package installer)

## Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/teletweet.git
cd teletweet
```

2. Create a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix:
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Telegram Setup

1. Create a new bot:

   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command
   - Choose a name and username
   - Save the bot token

2. Get API credentials:
   - Visit [my.telegram.org](https://my.telegram.org)
   - Log in with your account
   - Go to 'API development tools'
   - Create an application
   - Save the `app_id` and `app_hash`

### 2. Twitter Setup

1. Create a Twitter Developer Account:
   - Visit [developer.twitter.com](https://developer.twitter.com)
   - Apply for developer access
   - Create a new project
   - Create new App credentials
2. Get OAuth 2.0 credentials:
   - Generate Consumer Keys
   - Create Access Token and Secret
   - Save all credentials

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
# Telegram Credentials
APP_ID=your_telegram_app_id
APP_HASH=your_telegram_app_hash
BOT_TOKEN=your_telegram_bot_token

# Twitter Credentials
CONSUMER_KEY=your_twitter_consumer_key
CONSUMER_SECRET=your_twitter_consumer_secret
ACCESS_KEY=your_twitter_access_key
ACCESS_SECRET=your_twitter_access_secret

# Channel and Group IDs
CONFIG_CHANNEL_ID=your_config_channel_id
CHANNEL_ID=your_main_channel_id
GROUP_ID=your_group_id
SOURCE_CHANNEL_ID=your_source_channel_id
SOURCE_REPOSITORY_CHANNEL_ID=your_repository_channel_id

# Group Settings
GROUP_TOPIC_ID=your_group_topic_id
CHANNEL_AD_MESSAGE_ID=your_ad_message_id

# Message Settings
TWEET_LENGTH=280
ALLOW_USERS=user_id1,user_id2
```

### 4. Channel and Group Setup

1. Create required channels:

   - Main channel for posts
   - Config channel for configurations
   - Source channel for forwarding

2. Add bot as admin to all channels with:

   - Delete messages permission
   - Post messages permission
   - Edit messages permission

3. Get channel and group IDs:
   - Forward a message from each channel to [@userinfobot](https://t.me/userinfobot)
   - Note down the IDs (they start with `-100`)

## Running the Bot

### Local Development

1. Start the bot:

```bash
python -m teletweet.tweetbot
```

2. Testing:

```bash
# Run tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_handlers.py
```

### Production Deployment

#### Using Docker

1. Build the image:

```bash
docker build -t teletweet .
```

2. Run the container:

```bash
docker run -d \
  --name teletweet \
  --restart unless-stopped \
  --env-file .env \
  teletweet
```

#### Using systemd (Linux)

1. Copy service file:

```bash
sudo cp TeleTweet.service /etc/systemd/system/
```

2. Edit service file:

```bash
sudo nano /etc/systemd/system/TeleTweet.service
```

Update paths and user in the service file.

3. Start the service:

```bash
sudo systemctl enable TeleTweet
sudo systemctl start TeleTweet
```

## Tag Management

1. Create tags file:

```bash
touch teletweet/tags.txt
```

2. Add default tags:

```bash
echo "#tag1\n#tag2" > teletweet/tags.txt
```

## Monitoring

### Logs

Logs are written to stdout and can be viewed:

```bash
# Docker
docker logs -f teletweet

# systemd
journalctl -u TeleTweet -f
```

### Health Checks

1. Monitor bot status:

   - Send `/ping` command to bot
   - Check response time

2. Check logs for errors:
   - Error messages are prefixed with `[ERROR]`
   - Warning messages with `[WARNING]`

## Troubleshooting

### Common Issues

1. **Authentication Errors**

   - Verify APP_ID and APP_HASH match
   - Check BOT_TOKEN validity
   - Ensure bot is admin in all channels

2. **Permission Errors**

   - Verify bot has required permissions
   - Check channel/group IDs are correct
   - Ensure user is in ALLOW_USERS list

3. **Message Processing Issues**
   - Check message length limits
   - Verify media file sizes
   - Ensure proper source channel setup

### Debug Mode

Enable debug logging:

```python
# In tweetbot.py
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s [%(levelname)s]: %(message)s"
)
```

## Security Considerations

1. **Environment Variables**

   - Never commit .env file
   - Use secure secrets management
   - Rotate credentials regularly

2. **Access Control**

   - Limit ALLOW_USERS strictly
   - Monitor authentication logs
   - Review permissions regularly

3. **Rate Limiting**
   - Respect platform API limits
   - Implement backoff strategies
   - Monitor usage patterns

## Maintenance

1. Regular Tasks:

   - Update dependencies
   - Rotate credentials
   - Backup configuration
   - Clean old message cache

2. Updates:

   - Check for bot updates
   - Test updates locally
   - Deploy in maintenance window

3. Monitoring:
   - Check system resources
   - Monitor error rates
   - Review access logs

## Support

For issues and questions:

1. Check documentation
2. Review error logs
3. Create GitHub issue
4. Contact maintainers

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style
- Pull requests
- Testing
- Documentation
