#!/usr/local/bin/python3
# coding: utf-8

__author__ = "Benny <benny.think@gmail.com>"

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

from pyrogram import Client, filters
from teletweet.config import APP_HASH, APP_ID, BOT_TOKEN
from teletweet.handlers.commands import start_handler, help_handler, delete_handler, status_handler
from teletweet.handlers.messages import (
    message_handler, 
    media_group_handler,
    single_media_handler
)
from teletweet.handlers.callbacks import (
    config_callback,
    platform_callback,
    truncation_callback,
    preview_callback,
    back_to_options_callback
)
from teletweet.utils.message_store import MESSAGE_STORE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/teletweet.log", mode='a')
    ]
)
logging.getLogger("apscheduler.executors.default").propagate = False

class TeleTweetBot:
    def __init__(self):
        """Initialize the bot."""
        # Ensure logs directory exists
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        self.bot = Client(
            "teletweet_bot",  # name as first positional argument
            api_id=APP_ID,
            api_hash=APP_HASH,
            bot_token=BOT_TOKEN,
            workdir=str(current_dir)
        )
        self.setup_handlers()

    def wrap_handler(self, handler):
        """Wrap a handler function to ensure it's async."""
        async def wrapper(client, update):
            if asyncio.iscoroutinefunction(handler):
                return await handler(client, update)
            else:
                return handler(client, update)
        return wrapper

    def setup_handlers(self):
        """Set up message and callback handlers."""
        # Command handlers
        self.bot.on_message(filters.command(["start"]))(self.wrap_handler(start_handler))
        self.bot.on_message(filters.command(["help"]))(self.wrap_handler(help_handler))
        self.bot.on_message(filters.command(["delete"]))(self.wrap_handler(delete_handler))
        self.bot.on_message(filters.command(["status"]))(self.wrap_handler(status_handler))
        
        # Message handlers
        self.bot.on_message(filters.media_group)(self.wrap_handler(media_group_handler))
        self.bot.on_message(filters.photo | filters.document | filters.video | filters.sticker)(self.wrap_handler(single_media_handler))
        self.bot.on_message(filters.incoming & ~filters.media_group & ~filters.command(["start", "help", "delete", "status"]))(self.wrap_handler(message_handler))

        # Callback handlers
        @self.bot.on_callback_query()
        async def callback_handler(client, call):
            data = call.data
            message_id = None
            
            try:
                if data.startswith("config_"):
                    # Config type selection
                    _, action, msg_id = data.split("_")
                    message = MESSAGE_STORE.get(int(msg_id))
                    if message:
                        await config_callback(client, call, message, action)

                elif data.startswith("pub_"):
                    # Platform selection
                    _, platform, is_forwarded, is_multiple, msg_id = data.split("_")
                    message = MESSAGE_STORE.get(int(msg_id))
                    if not message:
                        await call.answer("Message not found!")
                        return

                    await platform_callback(
                        client, call, platform,
                        is_forwarded.lower() == "true",
                        is_multiple.lower() == "true",
                        message
                    )

                elif data.startswith("preview_"):
                    # Preview handling
                    _, is_forwarded, is_multiple, msg_id = data.split("_")
                    message = MESSAGE_STORE.get(int(msg_id))
                    if not message:
                        await call.answer("Message not found!")
                        return
                    
                    await preview_callback(client, call, message)

                elif data.startswith("back_options_"):
                    # Back to options handling
                    _, msg_id = data.split("_")
                    message = MESSAGE_STORE.get(int(msg_id))
                    if not message:
                        await call.answer("Message not found!")
                        return
                        
                    await back_to_options_callback(client, call, message)

                elif data.startswith("trunc_"):
                    # Truncation option handling
                    _, method, msg_id, platform = data.split("_")
                    stored_data = MESSAGE_STORE.get(f"trunc_{msg_id}_{platform}")
                    if not stored_data:
                        await call.answer("Message data not found!")
                        return

                    await truncation_callback(client, call, method, msg_id, platform, stored_data)

                # Clean up stored message if no truncation options are pending
                if data.startswith("pub_"):
                    _, _, _, _, msg_id = data.split("_")
                    if not any(k.startswith(f"trunc_{msg_id}") for k in MESSAGE_STORE.keys()):
                        MESSAGE_STORE.pop(int(msg_id), None)

                await call.answer()
                
            except Exception as e:
                logging.error(f"Error handling callback: {e}")
                if message_id:
                    MESSAGE_STORE.pop(int(message_id), None)
                await call.answer("An error occurred processing your request.")

    def run(self):
        """Start the bot."""
        banner = """
 _____    _    _____               _   
|_   _|  | |  |_   _|             | |  
  | | ___| | ___ | |_      _____  | |_ 
  | |/ _ \ |/ _ \| \ \ /\ / / _ \ | __|
  | |  __/ |  __/| |\ V  V /  __/ | |_ 
  \_/\___|_|\___|\__| \_/\_/ \___|  \__|
        by BennyThink
        """
        print(banner)
        print("Teletweet is running...")
        
        # Start bot
        try:
            self.bot.run()
        except Exception as e:
            logging.error(f"Bot crashed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    bot = TeleTweetBot()
    bot.run()
