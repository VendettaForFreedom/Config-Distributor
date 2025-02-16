# Running TeleTweet Bot on Windows

This guide explains how to run the TeleTweet bot on Windows systems.

## Prerequisites

1. Install Python 3.8 or higher:

   - Download from [Python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation: Open Command Prompt and type `python --version`

2. Download the bot code:
   - Download and extract the zip file
   - Or use Git: `git clone https://github.com/yourusername/teletweet.git`

## Quick Start

1. Double-click `run.bat`

   - It will automatically:
     - Create virtual environment
     - Install dependencies
     - Set up configuration files
     - Start the bot

2. First Run Setup:
   - The script will create a `.env` file
   - Notepad will open automatically
   - Fill in your credentials:
     - Telegram API credentials
     - Twitter API credentials
     - Channel and Group IDs

## Manual Setup

If you prefer to set up manually:

1. Open Command Prompt in the bot directory:

```batch
cd path\to\teletweet
```

2. Create virtual environment:

```batch
python -m venv venv
```

3. Activate virtual environment:

```batch
venv\Scripts\activate
```

4. Install dependencies:

```batch
pip install -r requirements.txt
```

5. Create and edit .env file:

```batch
copy example.env .env
notepad .env
```

6. Run the bot:

```batch
python -m teletweet.tweetbot
```

## Testing on Windows

1. Install test dependencies:

```batch
pip install pytest pytest-asyncio pytest-mock
```

2. Run tests:

```batch
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. Python not found:

   ```
   'python' is not recognized as an internal or external command
   ```

   - Solution: Reinstall Python with "Add to PATH" checked
   - Or add Python to PATH manually

2. Permission errors:

   ```
   Error: Access is denied
   ```

   - Run Command Prompt as Administrator
   - Check folder permissions

3. Module not found:

   ```
   ModuleNotFoundError: No module named 'teletweet'
   ```

   - Make sure you're in the correct directory
   - Verify virtual environment is activated

4. Installation errors:
   ```
   Error: Microsoft Visual C++ 14.0 is required
   ```
   - Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

## Using Docker on Windows

1. Install Docker Desktop for Windows

2. Open PowerShell and run:

```powershell
docker-compose up -d
```

3. View logs:

```powershell
docker-compose logs -f
```

## Development Setup

1. Install VSCode:

   - Download from [code.visualstudio.com](https://code.visualstudio.com)
   - Install Python extension

2. Open project:

   ```batch
   code .
   ```

3. Select Python interpreter:
   - Press Ctrl+Shift+P
   - Type "Python: Select Interpreter"
   - Choose the venv Python

## Updating the Bot

1. Stop the bot (Ctrl+C in Command Prompt)

2. Update code:

```batch
git pull
```

3. Update dependencies:

```batch
pip install -r requirements.txt
```

4. Restart the bot:
   - Double-click `run.bat`
   - Or run manually: `python -m teletweet.tweetbot`

## Running in Background

1. Using Windows Task Scheduler:

   - Open Task Scheduler
   - Create Basic Task
   - Action: Start a program
   - Program: path\to\run.bat
   - Run whether user is logged in or not

2. Using PowerShell:

```powershell
Start-Process -FilePath "run.bat" -WindowStyle Hidden
```

## Support

If you encounter issues:

1. Check the logs:

   - Look for error messages in the Command Prompt
   - Check Windows Event Viewer for Python errors

2. Common problems:

   - Path issues: Use full paths in configurations
   - Permission issues: Run as Administrator
   - Network issues: Check firewall settings

3. Getting help:
   - Check documentation in docs/
   - Create an issue on GitHub
   - Contact support team
