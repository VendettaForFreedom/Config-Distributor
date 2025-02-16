@echo off
title TeleTweet Bot

:: Check Python version
python -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 13) else 1)" > nul 2>&1
if errorlevel 1 (
    echo Python 3.13.2 or higher is required!
    echo Current Python version:
    python --version
    pause
    exit /b 1
)

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.13.2 or higher.
    pause
    exit /b 1
)

:: Check for virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Check for .env file
if not exist .env (
    echo Creating .env file template...
    (
        echo # Telegram Credentials
        echo APP_ID=
        echo APP_HASH=
        echo BOT_TOKEN=
        echo.
        echo # Twitter Credentials
        echo CONSUMER_KEY=
        echo CONSUMER_SECRET=
        echo ACCESS_KEY=
        echo ACCESS_SECRET=
        echo.
        echo # Channel and Group IDs [Optional]
        echo CONFIG_CHANNEL_ID=
        echo CHANNEL_ID=
        echo GROUP_ID=
        echo SOURCE_CHANNEL_ID=
        echo SOURCE_REPOSITORY_CHANNEL_ID=
        echo.
        echo # Group Settings [Optional]
        echo GROUP_TOPIC_ID=
        echo CHANNEL_AD_MESSAGE_ID=
        echo.
        echo # Message Settings
        echo TWEET_LENGTH=280
        echo ALLOW_USERS=
    ) > .env
    echo Please fill in your credentials in .env file
    start notepad .env
    exit /b 1
)

:: Create tags directory if it doesn't exist
if not exist teletweet (
    mkdir teletweet
)

:: Create tags file if it doesn't exist
if not exist teletweet\tags.txt (
    echo Creating tags.txt file...
    type nul > teletweet\tags.txt
)

:: Run the bot
echo Starting TeleTweet bot...
python -m teletweet.tweetbot > teletweet.log 2>&1

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred! Check teletweet.log for details.
)
