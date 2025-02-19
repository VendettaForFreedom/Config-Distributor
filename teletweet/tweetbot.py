#!/usr/local/bin/python3
# coding: utf-8

# TeleTweet - bot.py
# 10/22/20 16:25
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import os
import tempfile
import time
import json
import random
from datetime import timedelta
from threading import Lock

import requests
from pyrogram import Client, enums, filters, types

from config import (
    APP_HASH, 
    APP_ID, 
    BOT_TOKEN, 
    CONFIG_CHANNEL_ID, 
    CHANNEL_ID, 
    SOURCE_CHANNEL_ID,
    SOURCE_REPOSITORY_CHANNEL_ID,
    ALLOW_USERS, 
    FEEDBACK, 
    TODAY_CONFIG, 
    CONFIG_CHANNEL, 
    SOURCE_CHANNEL,
    CONTINUE_READING,
    CHANNEL, 
    GROUP_ID, 
    GROUP,
    GROUP_TOPIC_ID,
    CHANNEL_AD_MESSAGE_ID,
    CHANNEL_URL,
    tweet_format,
    tweet_length
)

from tweet import (
    delete_tweet,
    get_me,
    get_video_download_link,
    is_video_tweet,
    send_tweet,
    generate_tags
)

lock = Lock()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s [%(levelname)s]: %(message)s")
logging.getLogger("apscheduler.executors.default").propagate = False
media_group = {}
bot = Client("teletweet", APP_ID, APP_HASH, bot_token=BOT_TOKEN)

STEP = {}
Multi_message = {}

def user_check(func):
    def wrapper(client, message):
        user_id = message.chat.id
        logging.info("User %s is using the bot", user_id)
        
        if str(user_id) not in [CONFIG_CHANNEL_ID, CHANNEL_ID, GROUP_ID]:
            logging.info("User %s got into the first if", user_id)
            if str(user_id) in ALLOW_USERS or str(user_id) == SOURCE_CHANNEL_ID:
                logging.info("User %s got into the second if", user_id)
                logging.info("User %s is authenticated!")
                return func(client, message)
            else:
                logging.info("User %s got into the else", user_id)
                logging.info("User %s is not authenticated!")
                bot.send_message(message.chat.id, "You're not allowed to use this bot.")
                return
    return wrapper

@bot.on_message(filters.command(["start"]))
@user_check
def start_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)
    bot.send_message(message.chat.id, "Start by sending me a message?")
    msg = "Welcome to Config-Distributor. " "This bot will connect you from Telegram Bot to Twitter "
    if ALLOW_USERS != [""]:
        msg += "\n\nTHIS BOT IS ONLY AVAILABLE TO CERTAIN USERS. Contact creator for help."
    bot.send_message(message.chat.id, msg)


@bot.on_message(filters.command(["help"]))
def help_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)
    bot.send_message(message.chat.id, "Author: @BennyThink\nGitHub: https://github.com/tgbot-collection/TeleTweet")


@bot.on_message(filters.command(["delete"]))
def delete_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "Reply to some message and delete.")
        return
    result = delete_tweet(message)
    if result.get("error"):
        resp = f"❌ Error: `{result['error']}`"
        message.reply_text(resp, quote=True, parse_mode=enums.ParseMode.MARKDOWN)
    else:
        resp = f"🗑 Your tweet has been deleted.\n"
        message.reply_to_message.edit_text(resp, parse_mode=enums.ParseMode.MARKDOWN)

@bot.on_message(filters.command(["ping"]))
@user_check
def help_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)

    try:
        userinfo = "Hello👋 " + get_me(message.chat.id) + "\n\n"
    except TypeError:
        userinfo = "Hello👋 unknown user! Want to `/sign_in` now?\n\n"

    # info = get_runtime("botsrunner_teletweet_1")[:500]
    bot.send_message(message.chat.id, userinfo, parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True)

@bot.on_message(filters.command(["single_config"]))
@user_check
def config_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)
    bot.send_message(message.chat.id, "Send me a single config I send it without any ad.")
    STEP[message.chat.id] = "single_config"

@bot.on_message(filters.command(["multiple_configs"]))
@user_check
def config_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)
    bot.send_message(message.chat.id, "Send me a list of configs I send them with an ad.")
    STEP[message.chat.id] = "multiple_configs"

@bot.on_message(filters.command(["all_in_one"]))
@user_check
def config_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.TYPING)
    bot.send_message(message.chat.id, "Send me a list of configs I send them with an ad.")
    STEP[message.chat.id] = "all_in_one"

def show_source_preview(message: types.Message):
    """Show preview for a single source channel message"""
    text = message.text or message.caption or ""
    photo = message.photo
    
    preview = "📝 Preview of forwarded message:\n\n"
    if text:
        preview += f"Text: {truncate_content(text, 300)}\n\n"
    if photo:
        preview += "📸 Contains photo\n\n"
        
    confirm_btn = types.InlineKeyboardButton("✅ Forward Message", callback_data="forward_single")
    cancel_btn = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_forward")
    preview_markup = types.InlineKeyboardMarkup([[confirm_btn, cancel_btn]])
    
    # Store message for later forwarding
    STEP[message.chat.id] = {
        "original_message": message,
        "type": "single"
    }
    
    message.reply_text(preview, reply_markup=preview_markup)

def show_multi_message_preview(content: str, picture: str, chat_id: str, message: types.Message):
    """Show preview for multi-message forward"""
    preview = "📝 Preview of combined messages:\n\n"
    if content:
        preview += f"Text: {truncate_content(content, 300)}\n\n"
    if picture:
        preview += "📸 Contains photo\n\n"
        
    confirm_btn = types.InlineKeyboardButton("✅ Forward Messages", callback_data="forward_multi")
    cancel_btn = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_forward")
    preview_markup = types.InlineKeyboardMarkup([[confirm_btn, cancel_btn]])
    
    # Store messages for later forwarding
    STEP[message.chat.id] = {
        "content": content,
        "picture": picture,
        "chat_id": chat_id,
        "type": "multi"
    }
    
    message.reply_text(preview, reply_markup=preview_markup)

@bot.on_message(filters.incoming)
@user_check
def tweet_text_handler(client, message: types.Message):
    if str(message.chat.id) == SOURCE_CHANNEL_ID:
        auto_ad_message(message, preview_only=True)
        return
    message_text = message.text or message.caption
    if not message_text:
        return
    
    message.reply_chat_action(enums.ChatAction.TYPING)
    # first check if the user want to download video, gif
    tweet_id = is_video_tweet(message.chat.id, message_text)
    if tweet_id and message_text.startswith("https://twitter.com"):
        btn1 = types.InlineKeyboardButton("Download", callback_data=tweet_id)
        btn2 = types.InlineKeyboardButton("Tweet", callback_data="tweet")
        markup = types.InlineKeyboardMarkup(
            [
                [btn1, btn2],
            ]
        )
        message.reply_text("Do you want to download video or just tweet this?", quote=True, reply_markup=markup)
        return
    
    # Show preview for messages
    text = message.text or message.caption
    preview = f"Preview of your message:\n\n{text}"
    if len(preview) > 500:
        preview = preview[:497] + "..."
    
    # Add inline keyboard for confirm/edit
    confirm_btn = types.InlineKeyboardButton("✅ Confirm & Send", callback_data="confirm")
    edit_btn = types.InlineKeyboardButton("✏️ Edit", callback_data="edit")
    preview_markup = types.InlineKeyboardMarkup([[confirm_btn, edit_btn]])
    
    # Store original message for later use
    STEP[message.chat.id] = {
        "original_message": message,
        "text": text,
        "send_ad": True,
        "divide": True
    }
    
    message.reply_text(preview, quote=True, reply_markup=preview_markup)
    
    if STEP.get(message.chat.id) == "single_config":
        handle_message(message, False, False)
        STEP.pop(message.chat.id)
    elif STEP.get(message.chat.id) == "multiple_configs":
        handle_message(message, True, True)
        STEP.pop(message.chat.id)
    elif STEP.get(message.chat.id) == "all_in_one":
        handle_message(message, True, False)
        STEP.pop(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Send me a command first.")
    
def truncate_content(content, limit=500):
    if len(content) > limit:
        return content[:limit] + "..."
    else:
        return content

def is_multi_message(message):
    time_difference = message.date - Multi_message[SOURCE_CHANNEL_ID].date
    if time_difference.total_seconds() < 0:
        time_difference = -time_difference
    return time_difference < timedelta(minutes=5)

def auto_ad_message(message:types.Message, preview_only=False):
    if str(message.chat.id) == SOURCE_CHANNEL_ID:
        logging.info("Message received from %s", message.chat.id)
        if not Multi_message or not is_multi_message(message):
            Multi_message[SOURCE_CHANNEL_ID] = message
            if preview_only:
                show_source_preview(message)
            return
        
        content = ""
        picture = ""
        chat_id = ""
        if (message.photo is not None and (Multi_message[SOURCE_CHANNEL_ID].text is not None or Multi_message[SOURCE_CHANNEL_ID].caption is not None)):
            content = Multi_message[SOURCE_CHANNEL_ID].text or Multi_message[SOURCE_CHANNEL_ID].caption
            picture = message.photo.file_id
            chat_id = Multi_message[SOURCE_CHANNEL_ID].forward_from_message_id
        elif (Multi_message[SOURCE_CHANNEL_ID].photo is not None and (message.text is not None or message.caption is not None)):
            content = message.text or message.caption
            picture = Multi_message[SOURCE_CHANNEL_ID].photo.file_id
            chat_id = message.forward_from_message_id
        else:
            if preview_only:
                show_source_preview(message)
            return
        
        if chat_id is None:
            chat_id = ""
            
        if preview_only:
            show_multi_message_preview(content, picture, chat_id, message)
            return

        messageNew = None  
        img_data = None 
        try:
            del Multi_message[SOURCE_CHANNEL_ID]
            # https://t.me/FreeVPNHomes/324
            channel_message = bot.get_messages(CHANNEL_ID, CHANNEL_AD_MESSAGE_ID)
            stop_string = CHANNEL
            if stop_string in channel_message.text:
                channel_message.text = channel_message.text.split(stop_string)[0] + stop_string
            messageNew = bot.send_photo(
                CHANNEL_ID, 
                picture,
                truncate_content(content,300) + "\n\n" + 
                CONTINUE_READING +
                SOURCE_CHANNEL + f"{chat_id}" + "\n\n" +
                # contains everything except tags
                channel_message.text + "\n\n" +
                generate_tags("first5random")
            )
            img_data = messageNew.download(in_memory=True)
            setattr(img_data, "mode", "rb")
        except Exception as e:
            logging.error(f"Error while sending message from {message.chat.id} to {CHANNEL_ID}: {e}")
        
        time.sleep(1)
        
        try:
            bot.send_photo(
                GROUP_ID, 
                picture,
                truncate_content(content) + "\n\n" + 
                CONTINUE_READING +
                SOURCE_CHANNEL + f"{chat_id}" + "\n\n" +
                GROUP + generate_tags("first5random"),
                reply_to_message_id = GROUP_TOPIC_ID
            )
        except Exception as e:
            logging.error(f"Error while sending message from {message.chat.id} to {GROUP_ID}: {e}")
        
        time.sleep(1)

        try:
            bot.send_photo(
                GROUP_ID, 
                picture,
                truncate_content(content) + "\n\n" + 
                CONTINUE_READING +
                SOURCE_CHANNEL + f"{chat_id}" + "\n\n" +
                GROUP + generate_tags("first5random")
            )
        except Exception as e:
            logging.error(f"Error while sending message from {message.chat.id} to {GROUP_ID}: {e}")

        try:
            send_tweet(messageNew,
            truncate_content(content, tweet_length) + "\n" + 
            CONTINUE_READING +
            SOURCE_CHANNEL + f"{chat_id}" + "\n" +
            CHANNEL_URL + generate_tags(),
            [img_data])
        except Exception as e:
            logging.error(f"Error while sending tweet from {CHANNEL_ID}: {e}")
        
        time.sleep(3600)
        
        try:
            # https://t.me/FreeVPNHomes/324
            bot.forward_messages(
                chat_id = GROUP_ID, 
                from_chat_id = CHANNEL_ID,
                message_ids = [CHANNEL_AD_MESSAGE_ID]
            )
        except Exception as e:
            logging.error(f"Error while sending message from {CHANNEL_ID} to {GROUP_ID}: {e}")

def send_ad_message(message):
    try:
        messageNew = bot.send_message(
            CONFIG_CHANNEL_ID, 
            TODAY_CONFIG + FEEDBACK + CHANNEL + generate_tags()
        )
    except:
        bot.send_message(
            message.chat.id, 
            "I can't send the message to the config channel:" + CONFIG_CHANNEL_ID
        )
        return
    time.sleep(1)

    try:
        config_channel = CONFIG_CHANNEL + f"{messageNew.id}"
        messageNew = bot.send_message(
            CHANNEL_ID, 
            TODAY_CONFIG + config_channel + FEEDBACK + CHANNEL + generate_tags()
        )
    except:
        bot.send_message(
            message.chat.id, 
            "I can't send the message to the main channel:" + CHANNEL_ID
        )
        return

    time.sleep(1)
    try:
        bot.send_message(
            GROUP_ID, 
            TODAY_CONFIG + CONFIG_CHANNEL + FEEDBACK + CHANNEL + generate_tags()
        )
    except:
        bot.send_message(
            message.chat.id, 
            "I can't send the message to the group:" + GROUP_ID
        )

    result = send_tweet(messageNew)
    notify_result(result, message)
    return messageNew

def send_config_message(part):
    try:
        # read message_id_pairs from file randomly
        # Open and read the text file
        with open('message_id_pairs.txt', 'r') as file:
            message_id_pairs = [list(map(int, line.strip().split())) for line in file.readlines()]

        # Randomly select one pair of message IDs
        selected_pair = random.choice(message_id_pairs)
        logging.info("selected_pair: %s", selected_pair)

        logging.info("fetched_messages before")
        content, picture, chat_id, img_data = "", "", "", None
        if selected_pair is not None:
            fetched_messages = bot.get_messages(SOURCE_REPOSITORY_CHANNEL_ID, selected_pair)
            for msg in fetched_messages:
                if msg.text is not None or msg.caption is not None:
                    content = msg.text or msg.caption
                    chat_id = msg.forward_from_message_id
                elif msg.photo is not None:
                    picture = msg.photo.file_id
                    img_data = msg.download(in_memory=True)
                    setattr(img_data, "mode", "rb")
        logging.info("fetched_messages after")
        
        message_body = ""
        if chat_id is not None:
            message_body = truncate_content(content,300) + "\n\n" + CONTINUE_READING + \
                SOURCE_CHANNEL + f"{chat_id}" + "\n\n"
    
        bot.send_photo(
            CONFIG_CHANNEL_ID, 
            picture,
            message_body + 
            "`" + part + "`" + 
            CHANNEL + generate_tags("first5random"))
        
    except Exception as e:
        logging.error(f"Error while sending message to {CONFIG_CHANNEL_ID}: {e}")

def handle_message(message, send_ad=True, divide=True):
    """Handle incoming messages with optional ad and message splitting."""
    if not hasattr(message, 'text') and not hasattr(message, 'caption'):
        return
        
    text = message.text or message.caption
    if not text:
        return
        
    # First handle advertisement if needed
    if send_ad:
        send_ad_message(message)
        
    # Then handle the actual message
    try:
        if divide:
            parts = text.split("\n")
            for part in parts:
                if len(part) > 10:
                    send_config_message(part)
                    time.sleep(1)
        else:
            send_config_message(text)
    except Exception as e:
        logging.error(f"Error in handle_message: {str(e)}")
        # If message handling fails, notify the user
        error_msg = f"Error sending message: {str(e)}"
        if len(error_msg) > 200:  # Truncate long error messages
            error_msg = error_msg[:197] + "..."
        message.reply_text(error_msg, quote=True)

@bot.on_message(filters.media_group)
@user_check
def tweet_group_photo_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
    # this method will be called multiple times
    # so we need to check if the group has been received
    media_group_id = message.media_group_id
    if STEP.get(media_group_id):
        return
    logging.info("Media group %s received", message.media_group_id)
    STEP[media_group_id] = True
    groups = message.get_media_group()
    files = []
    for group in groups:
        img_data = group.download(in_memory=True)
        setattr(img_data, "mode", "rb")
        caption = group.caption
        if caption:
            setattr(message, "text", caption)
        files.append(img_data)
    # handle_message(message)
    result = send_tweet(message, pics=files)
    notify_result(result, message)
    STEP.pop(media_group_id)


@bot.on_message(filters.photo | filters.document | filters.video | filters.sticker)
@user_check
def tweet_single_photo_handler(client, message: types.Message):
    message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
    logging.info("Normal one media message")
    img_data = message.download(in_memory=True)
    setattr(img_data, "mode", "rb")
    # handle_message(message)
    result = send_tweet(message, pics=[img_data])
    notify_result(result, message)


def notify_result(result, message: types.Message):
    if result.get("error"):
        resp = f"❌ Error: `{result['error']}`"
    else:
        url = tweet_format.format(screen_name="x", id=result["id"])
        resp = f"✅ Your [tweet]({url}) has been sent.\n"
    message.reply_text(resp, quote=True, parse_mode=enums.ParseMode.MARKDOWN)


@bot.on_callback_query(filters.regex("tweet"))
def tweet_callback(client, call: types.CallbackQuery):
    # handle_message(call.message)
    result = send_tweet(call.message.reply_to_message)
    notify_result(result, call.message)


@bot.on_callback_query(filters.regex("confirm"))
def confirm_callback(client, call: types.CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id not in STEP:
        bot.answer_callback_query(call.id, "Session expired. Please send your message again.")
        return
    
    stored_data = STEP[chat_id]
    original_message = stored_data["original_message"]
    send_ad = stored_data.get("send_ad", True)
    divide = stored_data.get("divide", True)
    
    # Process message as originally intended
    handle_message(original_message, send_ad, divide)
    
    # Clean up stored data
    STEP.pop(chat_id)
    
    # Update preview message
    call.message.edit_text(
        call.message.text + "\n\n✅ Message sent!",
        reply_markup=None
    )
    bot.answer_callback_query(call.id, "Message sent successfully!")

@bot.on_callback_query(filters.regex("edit"))
def edit_callback(client, call: types.CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id not in STEP:
        bot.answer_callback_query(call.id, "Session expired. Please send your message again.")
        return
    
    # Tell user to send the edited message
    call.message.edit_text(
        "Please send your edited message now.",
        reply_markup=None
    )
    bot.answer_callback_query(call.id, "Send your edited message")

@bot.on_callback_query(filters.regex("^forward_"))
def forward_callback(client, call: types.CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id not in STEP:
        bot.answer_callback_query(call.id, "Session expired. Please try again.")
        return

    stored_data = STEP[chat_id]
    forward_type = stored_data.get("type")
    
    try:
        if forward_type == "single":
            # Forward single message
            message = stored_data["original_message"]
            auto_ad_message(message, preview_only=False)
            success_text = "✅ Message forwarded successfully!"
        elif forward_type == "multi":
            # Forward multi-message combination
            content = stored_data["content"]
            picture = stored_data["picture"]
            chat_id = stored_data["chat_id"]
            
            # Create temp message with combined data
            temp_message = types.Message(
                message_id=0,
                date=0,
                chat=types.Chat(id=SOURCE_CHANNEL_ID, type="channel"),
            )
            if picture:
                temp_message.photo = types.Photo(file_id=picture)
            if content:
                temp_message.text = content
            
            auto_ad_message(temp_message, preview_only=False)
            success_text = "✅ Combined messages forwarded successfully!"
            
        # Update preview message
        call.message.edit_text(
            call.message.text + "\n\n" + success_text,
            reply_markup=None
        )
        bot.answer_callback_query(call.id, "Messages forwarded!")
        
    except Exception as e:
        error_msg = f"Error forwarding message: {str(e)}"
        if len(error_msg) > 200:
            error_msg = error_msg[:197] + "..."
        call.message.edit_text(
            call.message.text + f"\n\n❌ {error_msg}",
            reply_markup=None
        )
        bot.answer_callback_query(call.id, "Failed to forward messages")
    
    finally:
        # Clean up stored data
        STEP.pop(chat_id, None)

@bot.on_callback_query(filters.regex("cancel_forward"))
def cancel_forward_callback(client, call: types.CallbackQuery):
    chat_id = call.message.chat.id
    # Clean up stored data
    if chat_id in STEP:
        STEP.pop(chat_id)
    # Update message
    call.message.edit_text(
        call.message.text + "\n\n❌ Forwarding cancelled.",
        reply_markup=None
    )
    bot.answer_callback_query(call.id, "Forwarding cancelled")

@bot.on_callback_query()
def video_callback(client, call: types.CallbackQuery):
    # Skip if this is a known callback
    if call.data in ["confirm", "edit", "tweet", "forward_single", "forward_multi", "cancel_forward"]:
        return
        
    chat_id = call.message.chat.id
    message = call.message
    message.reply_chat_action(enums.ChatAction.TYPING)
    bot.answer_callback_query(call.id, "Sure, wait a second.")
    link = get_video_download_link(chat_id, call.data)
    logging.info("Downloading %s ...", link)
    r = requests.get(link, stream=True)
    logging.info("Download complete")
    message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_file:
        video_file.write(r.content)
        message.reply_video(video_file.name, quote=True)


if __name__ == "__main__":
    banner = """
▀▛▘  ▜     ▀▛▘         ▐
 ▌▞▀▖▐ ▞▀▖  ▌▌  ▌▞▀▖▞▀▖▜▀
 ▌▛▀ ▐ ▛▀   ▌▐▐▐ ▛▀ ▛▀ ▐ ▖
 ▘▝▀▘ ▘▝▀▘  ▘ ▘▘ ▝▀▘▝▀▘ ▀
 by BennyThink
    """
    print(f"\033[1;35m {banner}\033[0m")
    print("\033[1;36mTeletweet is running...\033[0m")
    bot.run()
