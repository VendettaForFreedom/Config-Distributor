#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Telegram Credentials
APP_ID=
APP_HASH=
BOT_TOKEN=

# Twitter Credentials
CONSUMER_KEY=
CONSUMER_SECRET=
ACCESS_KEY=
ACCESS_SECRET=

# Channel and Group IDs
CONFIG_CHANNEL_ID=
CHANNEL_ID=
GROUP_ID=
SOURCE_CHANNEL_ID=
SOURCE_REPOSITORY_CHANNEL_ID=

# Group Settings
GROUP_TOPIC_ID=
CHANNEL_AD_MESSAGE_ID=

# Message Settings
TWEET_LENGTH=280
ALLOW_USERS=
EOF
    echo "Please fill in your credentials in .env file"
    exit 1
fi

# Create tags file if it doesn't exist
if [ ! -f "teletweet/tags.txt" ]; then
    echo "Creating tags.txt file..."
    mkdir -p teletweet
    touch teletweet/tags.txt
fi

# Run the bot
echo "Starting TeleTweet bot..."
python3 -m teletweet.tweetbot
