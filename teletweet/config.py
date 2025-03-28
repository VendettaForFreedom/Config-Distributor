#!/usr/local/bin/python3
# coding: utf-8

# TeleTweet - config.py
# 10/22/20 16:20
#

__author__ = "Benny <benny.think@gmail.com>"

import os

BOT_TOKEN = os.getenv("TOKEN", "")
APP_ID = int(os.getenv("APP_ID", ""))
APP_HASH = os.getenv("APP_HASH", "")

CONSUMER_KEY = os.getenv("CONSUMER_KEY", "")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET", "")
ACCESS_KEY = os.getenv("ACCESS_KEY", "")
ACCESS_SECRET = os.getenv("ACCESS_SECRET", "")
CONFIG_CHANNEL_ID = os.getenv("CONFIG_CHANNEL_ID", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID", "")
GROUP_ID = os.getenv("GROUP_ID", "")
SOURCE_REPOSITORY_CHANNEL_ID = int(os.getenv("SOURCE_REPOSITORY_CHANNEL_ID", "0"))
GROUP_TOPIC_ID = int(os.getenv("GROUP_TOPIC_ID", "0"))
CHANNEL_AD_MESSAGE_ID = int(os.getenv("CHANNEL_AD_MESSAGE_ID", "0"))
GROUP = os.getenv("GROUP", "")
# AUTH_STRING = os.getenv("AUTH_STRING", "")

DISCUSSION_GROUP = "\n\n@FreeVPNHomesDiscussion\n\n"
DISCUSSION_GROUP_URL = """\n\nhttps://t.me/FreeVPNHomesDiscussion\n\n"""
TWITTER = "توییتر:\n\nhttps://twitter.com/FreeVPNHomes"
FEEDBACK = "\n\nنظرات و پیشنهادات خودتون رو برامون تو گروه بنویسین:{0}".replace("{0}",DISCUSSION_GROUP) + TWITTER
TODAY_CONFIG = "کانفیگ های امروز:"
CHANNEL_URL = """\n\nhttps://t.me/FreeVPNHomes\n\n"""
CHANNEL = """\n\n@FreeVPNHomes\n\n"""
CONFIG_CHANNEL = "\nhttps://t.me/FreeVPNHomesConfigs/"
SOURCE_CHANNEL = "\nhttps://t.me/javeednaman/"
CONTINUE_READING = "ادامه مطلب رو در کانال زیر بخوانید:\n"

tweet_length = int(os.getenv("tweet_length", "300"))
tweet_format = "https://twitter.com/{screen_name}/status/{id}"
# remove ALLOW_USERS white spaces then split by comma
ALLOW_USERS = os.getenv("ALLOW_USERS", "").replace(" ", "").split(",") if os.getenv("ALLOW_USERS", "") else [""]
