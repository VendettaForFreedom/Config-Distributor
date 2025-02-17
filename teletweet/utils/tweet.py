import logging
import tweepy
from typing import Optional, List, Dict, Union
from ..config import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_KEY,
    ACCESS_SECRET
)

def get_me(user_id) -> Union[str, Dict[str, str]]:
    """Get Twitter username or error details."""
    try:
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_KEY,
            access_token_secret=ACCESS_SECRET
        )
        me = client.get_me()
        return me.data.username
    except Exception as e:
        return {"error": str(e)}

async def send_tweet(message, text: str, pics: Optional[List[bytes]] = None) -> Dict:
    """Send a tweet with optional media."""
    try:
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_KEY,
            access_token_secret=ACCESS_SECRET
        )
        
        media_ids = []
        if pics:
            auth = tweepy.OAuth1UserHandler(
                CONSUMER_KEY,
                CONSUMER_SECRET,
                ACCESS_KEY,
                ACCESS_SECRET
            )
            api = tweepy.API(auth)
            
            for pic in pics:
                media = api.media_upload(filename="media", file=pic)
                media_ids.append(media.media_id)
        
        result = client.create_tweet(text=text, media_ids=media_ids if media_ids else None)
        return {"id": result.data["id"]}
    except Exception as e:
        return {"error": str(e)}

async def delete_tweet(message) -> Dict:
    """Delete a tweet."""
    try:
        tweet_id = None
        if not message.reply_to_message:
            return {"error": "Reply to a message to delete its tweet"}
            
        text = message.reply_to_message.text
        if not text:
            return {"error": "No tweet ID found in the message"}
            
        # Try to find tweet ID
        import re
        match = re.search(r"twitter\.com/\w+/status/(\d+)", text)
        if match:
            tweet_id = match.group(1)
        else:
            return {"error": "No tweet URL found in the message"}

        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_KEY,
            access_token_secret=ACCESS_SECRET
        )
        client.delete_tweet(tweet_id)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def is_video_tweet(user_id, text: str) -> str:
    """Check if text contains a tweet with video."""
    if not text or not text.startswith("https://twitter.com"):
        return None
        
    import re
    match = re.search(r"twitter\.com/\w+/status/(\d+)", text)
    if not match:
        return None
        
    return match.group(1)

async def get_video_download_link(chat_id, tweet_id: str) -> str:
    """Get video download link for a tweet."""
    try:
        auth = tweepy.OAuth1UserHandler(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            ACCESS_KEY,
            ACCESS_SECRET
        )
        api = tweepy.API(auth)
        tweet = api.get_status(tweet_id, tweet_mode="extended")
        if hasattr(tweet, "extended_entities"):
            media = tweet.extended_entities.get("media", [])
            for m in media:
                if m.get("type") == "video":
                    variants = m.get("video_info", {}).get("variants", [])
                    mp4s = [v for v in variants if v.get("content_type") == "video/mp4"]
                    # Sort by bitrate, highest first
                    best_video = sorted(mp4s, key=lambda x: x.get("bitrate", 0), reverse=True)[0]
                    return best_video["url"]
    except Exception as e:
        logging.error(f"Error getting video link: {e}")
    return None
