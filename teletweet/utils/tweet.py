#!/usr/local/bin/python3
# coding: utf-8

# TeleTweet - tweet.py
# 10/22/20 16:18
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import re
import traceback
from typing import Union
from ..helper import generate_tags

import tweepy

from ..config import (
    CONSUMER_KEY, 
    CONSUMER_SECRET,
    ACCESS_KEY, 
    ACCESS_SECRET, 
    CHANNEL_URL, 
    CHANNEL,
    DISCUSSION_GROUP,
    DISCUSSION_GROUP_URL,
    TWITTER
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s [%(levelname)s]: %(message)s")


def __connect_twitter(chat_id: int):
    logging.info("Connecting to twitter api...")
    
    # Verify credentials are present
    if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET]):
        logging.error("Missing Twitter credentials")
        raise ValueError("Twitter credentials are not properly configured")
        
    try:
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_KEY,
            access_token_secret=ACCESS_SECRET,
        )
        api = tweepy.API(
            tweepy.OAuth1UserHandler(
                consumer_key=CONSUMER_KEY,
                consumer_secret=CONSUMER_SECRET,
                access_token=ACCESS_KEY,
                access_token_secret=ACCESS_SECRET,
            )
        )
        
        # Verify credentials are valid
        me = client.get_me()
        if not me:
            raise ValueError("Failed to verify Twitter credentials")
            
        logging.info(f"Connected to Twitter as @{me.data['username']}")
        return client, api
        
    except Exception as e:
        logging.error(f"Failed to connect to Twitter: {str(e)}")
        raise ValueError(f"Twitter authentication failed: {str(e)}")


def upload_media(api, pic) -> Union[list, None]:
    if pic is None:
        return None
    ids = []
    for item in pic:
        item.seek(0)
        mid = api.media_upload(item.name, file=item)
        ids.append(mid)
    return [i.media_id for i in ids]

async def send_tweet(message, text = None, pics: Union[list, None] = None) -> dict:
    logging.info("Preparing tweet for...")
    chat_id = message.chat.id
    if not text:
        text = message.text or message.caption
        text = text.replace(CHANNEL, CHANNEL_URL).replace(DISCUSSION_GROUP, DISCUSSION_GROUP_URL).replace(TWITTER, "")

    try:
        tweet_id = __get_tweet_id_from_reply(message)
        client, api = __connect_twitter(chat_id)
        
        if not CONSUMER_KEY or not CONSUMER_SECRET or not ACCESS_KEY or not ACCESS_SECRET:
            return {"error": "Twitter credentials are not configured properly"}
            
        logging.info("Tweeting...")
        ids = upload_media(api, pics)
        
        try:
            status = client.create_tweet(text=text, media_ids=ids, in_reply_to_tweet_id=tweet_id)
            logging.info(f"Successfully tweeted: {status.data}")
            return {"success": True, "data": status.data}
        except Exception as e:
            if "Your Tweet text is too long." in str(e):
                logging.warning("Tweet too long, trying to make it shorter...")
                try:
                    status = client.create_tweet(text=text[:270] + "...", media_ids=ids, in_reply_to_tweet_id=tweet_id)
                    logging.info(f"Successfully tweeted with truncation: {status.data}")
                    return {"success": True, "data": status.data}
                except Exception as e2:
                    logging.error(f"Failed to tweet even after truncation: {e2}")
                    return {"error": f"Failed to tweet even after truncation: {str(e2)}"}
            else:
                error_msg = f"Failed to tweet: {str(e)}"
                logging.error(f"{error_msg}\n{traceback.format_exc()}")
                return {"error": error_msg}
                
    except Exception as e:
        error_msg = f"Error in tweet preparation: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return {"error": error_msg}


async def get_me(chat_id) -> str:
    logging.info("Get me!")
    try:
        client, api = __connect_twitter(chat_id)
        try:
            me = client.get_me()
            if not me or not me.data:
                return {"error": "Failed to get Twitter account info"}
            name = me.data["name"]
            username = me.data["username"]
            logging.info(f"Successfully retrieved Twitter info: @{username}")
            return f"[{name}](https://twitter.com/{username})"
        except Exception as e:
            error_msg = f"Error getting Twitter account info: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            return {"error": error_msg}
    except Exception as e:
        error_msg = f"Twitter connection error: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return {"error": error_msg}


def delete_tweet(message) -> dict:
    logging.info("Deleting tweet for someone...")
    chat_id = message.chat.id
    tweet_id = __get_tweet_id_from_reply(message)
    if not tweet_id:
        return {"error": "Which tweet do you want to delete? This does not seem like a valid tweet message."}

    try:
        client, api = __connect_twitter(chat_id)
        logging.info("Deleting......")
        response = client.delete_tweet(tweet_id).data
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {"error": str(e)}

    return response


def __get_tweet_id_from_reply(message) -> int:
    reply_to = message.reply_to_message
    if reply_to:
        tweet_id = __get_tweet_id_from_url(reply_to.entities[0].url or "")
    else:
        tweet_id = None
    logging.info("Replying to %s", tweet_id)
    return tweet_id


def __get_tweet_id_from_url(url) -> int:
    try:
        # https://twitter.com/williamwoo7/status/1326147700425809921?s=20
        tweet_id = re.findall(r"https?://twitter\.com/.+/status/(\d+)", url)[0]
    except IndexError:
        tweet_id = None
    return tweet_id


def get_video_download_link(chat_id, tweet_id):
    client, api = __connect_twitter(chat_id)
    logging.info("Getting video tweets......")
    status = client.get_tweet(tweet_id).data
    return __get_video_url(status.AsDict())


def is_video_tweet(chat_id, text) -> str:
    # will return an id
    tweet_id = __get_tweet_id_from_url(text)
    logging.info("tweet id is %s", tweet_id)
    client, api = __connect_twitter(chat_id)
    logging.info("Getting video tweets......")
    try:
        # TODO I don't have permission to this. Thank you Elon Musk.
        status = client.get_tweet(tweet_id)
        if __get_video_url(status.data):
            return str(tweet_id)
    except Exception as e:
        logging.debug(traceback.format_exc())


def __get_video_url(json_dict: dict) -> str:
    logging.info("Downloading video...")
    # video/gif is the first one. photo could be four
    media = json_dict.get("media")
    if media:
        media = media[0]
        if media["type"] == "video":
            variants = media["video_info"]["variants"]
            rates = [i.get("bitrate", 0) for i in variants]
            index = rates.index(max(rates))
            url = variants[index]["url"]
            logging.info("Real download url found.")
            return url


if __name__ == "__main__":
    print(__get_tweet_id_from_url("https://twitter.com/williamwoo7/status/1326147700425809921?s=20"))
    print(__get_tweet_id_from_url("http://twitter.com/nixcraft/status/1326077772117078018?s=09"))
