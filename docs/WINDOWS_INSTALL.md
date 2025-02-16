# Windows Installation Guide for TeleTweet Bot

## Prerequisites

### 1. Python Installation

1. Download Python 3.13.2:

   - Go to [Python Downloads](https://www.python.org/downloads/)
   - Download Python 3.13.2 (64-bit recommended)
   - Do NOT use versions lower than 3.13.2 as they're not compatible

2. During installation:

   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
   - ✅ Check "Install for all users" (recommended)

3. Verify installation:
   ```cmd
   python --version
   ```
   Should show Python 3.13.2 or higher

### 2. Visual C++ Build Tools

Some dependencies require Visual C++ Build Tools:

1. Download Build Tools:

   - Go to [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Click "Download Build Tools"

2. Install:
   - Run the installer
   - Select "Desktop development with C++"
   - Click Install

## Bot Installation

1. Download the Bot:

   - Download and extract the zip file
   - Or use Git:

   ```cmd
   git clone https://github.com/yourusername/teletweet.git
   cd teletweet
   ```

2. Run Installation Script:

   ```cmd
   double-click run.bat
   ```

   The script will:

   - Check Python version
   - Create virtual environment
   - Upgrade pip
   - Install dependencies
   - Create config files

3. Configure the Bot:
   - The script will open .env file
   - Fill in required credentials:
     - Telegram API credentials (required)
     - Twitter API credentials (required)
     - Channel/Group IDs (optional)

## Common Installation Issues

### 1. Python Not Found

```
'python' is not recognized as an internal or external command
```

Solution:

1. Reinstall Python with "Add to PATH" checked
2. Or manually add to PATH:
   - Open System Properties > Advanced > Environment Variables
   - Add Python paths to System PATH

### 2. Pip Installation Errors

```
error: Microsoft Visual C++ 14.0 or greater is required
```

Solution:

1. Install Visual Studio Build Tools
2. Restart your computer
3. Try installation again

### 3. Dependencies Installation Failed

```
Could not find a version that satisfies the requirement...
```

Solution:

1. Upgrade pip:

```cmd
python -m pip install --upgrade pip
```

2. Try installation again:

```cmd
pip install -r requirements.txt
```

### 4. Virtual Environment Issues

```
'venv' is not recognized as an internal or external command
```

Solution:

1. Install venv:

```cmd
python -m pip install virtualenv
```

2. Create manually:

```cmd
python -m venv venv
venv\Scripts\activate
```

## Manual Installation Steps

If the batch script fails, you can install manually:

1. Open Command Prompt as Administrator

2. Create Virtual Environment:

```cmd
python -m venv venv
venv\Scripts\activate
```

3. Upgrade Pip:

```cmd
python -m pip install --upgrade pip
```

4. Install Dependencies:

```cmd
pip install -r requirements.txt
```

5. Create Configuration:

```cmd
copy example.env .env
notepad .env
```

6. Run the Bot:

```cmd
python -m teletweet.tweetbot
```

## Post-Installation

1. Test the Bot:

   - Send /start to your bot
   - Try forwarding a message
   - Check if all platforms work

2. Monitor Logs:

   - Check teletweet.log for errors
   - Use Windows Event Viewer

3. Optional: Create Startup Task
   - Open Task Scheduler
   - Create Basic Task
   - Action: Start Program
   - Program/script: path\to\run.bat
   - Start in: path\to\bot\directory

## Updating

1. Stop the bot:

   - Close the command window
   - Or use Task Manager

2. Update code:

   ```cmd
   git pull
   ```

3. Update dependencies:

   ```cmd
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Restart:
   ```cmd
   run.bat
   ```

## Support

If you need help:

1. Check logs in teletweet.log
2. Review configuration
3. Create an issue with:
   - Windows version
   - Python version
   - Error messages
   - Configuration (without credentials)
