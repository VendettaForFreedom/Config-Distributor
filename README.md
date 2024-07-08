# Config-Distributor Project

## Introduction
Config-Distributor seamlessly connects Telegram with Twitter, empowering admins to distribute vpn configs to different telegram channels and group as well twitter. This integration is facilitated by a sophisticated Telegram bot, built on Python, which handles Twitter operations securely and efficiently.

## Features
- **Direct Twitter Integration**: Link your Twitter account with Telegram for direct tweeting, retweeting, and more.
- **Media Tweeting**: Supports tweeting text, images, videos, and GIFs directly from Telegram.
- **Secure Authentication**: Ensures a secure sign-in process to connect your Twitter account with the Telegram bot.
- **Interactive Bot Commands**: Use simple bot commands to control your Twitter account functionalities.

## Installation
1. Clone the project repository to your local machine.
2. Install Python 3.x, if not already installed.
3. Install necessary Python dependencies by executing `pip install -r requirements.txt`.

## Configuration (`config.py`)
Before launching the Teletweet bot, you must accurately configure it with your API keys and settings in `config.py`. This configuration involves setting up both Telegram and Twitter API credentials, along with additional settings specific to the bot's operation:

- **Telegram Configuration**:
  - `APP_ID` and `APP_HASH`: These are your Telegram application ID and hash, obtainable after creating a new application at [my.telegram.org](https://my.telegram.org).
  - `BOT_TOKEN`: The token for your Telegram bot, provided by BotFather when you create a new bot on Telegram.

- **Twitter Configuration**:
  - `ACCESS_KEY` and `ACCESS_SECRET`: Your Twitter API key and secret key, obtained when you create a new application on the Twitter Developer portal.
  - Additional Twitter-specific configurations may include tokens for user authentication: `CONSUMER_KEY` and `CONSUMER_SECRET`, which are typically obtained through the OAuth process when a user authenticates their account with your application.

- **Bot Settings**:
  - `CHANNEL_ID` and `CONFIG_CHANNEL_ID`: Telegram channel IDs used for specific functionalities by the bot, if required.
  - `ALLOW_USERS`: A list of Telegram user IDs permitted to use this bot. Leave as `[""]` to allow open access.
  - `FEEDBACK`: Optionally, set a Telegram username or channel ID to receive feedback.
  - Configuration constants like `TODAY_CONFIG`, `SIGN`, `LAST_MESSAGE`, and `tweet_format` define operational details for the bot.

Ensure that you replace placeholder values in `config.py` with your actual API keys and settings. Proper configuration is crucial for the bot's operation, as it needs to authenticate and interact with both Telegram and Twitter APIs successfully.

Bot Commands
The bot recognizes commands for user interaction, allowing management of Twitter activities via Telegram. Here's a reminder of the commands and their functionalities:

`/start`: Greets the user and provides initial instructions or the authentication link for Twitter.

`/sign_in`: Initiates Twitter authentication, guiding the user through obtaining and submitting an authentication code.

`/sign_off`: Logs the user out, disconnecting their Twitter account from the bot.

Direct Messaging: Users can send tweets (text or media) directly by messaging the bot.

## Usage
After configuring `config.py` with your API keys and other settings, run `tweetbot.py` to start the Telegram bot. Follow the bot's instructions for signing in to Twitter and using the available commands to tweet.

## Contributing
We encourage contributions to the Teletweet project. If you've identified a bug, have suggestions for improvements, or want to add new features, please fork the repository, make your changes, and submit a pull request.

- We have deployment on feature-* branches that has an open pull request with build tag
- Production deployment when there is a merge on deployment branch

## License
GPL 2.0__
