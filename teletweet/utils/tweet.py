import logging
import tweepy
from typing import Optional, List, Dict, Union
import traceback
from ..config import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_KEY,
    ACCESS_SECRET
)

async def get_me(user_id) -> Union[str, Dict[str, str]]:
    """Get Twitter username or error details."""
    logging.info("Checking Twitter credentials...")
    try:
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_KEY,
            access_token_secret=ACCESS_SECRET
        )
        me = client.get_me()
        if not me or not me.data:
            return {"error": "Failed to get Twitter account info"}
        username = me.data.get("username")
        name = me.data.get("name", username)
        logging.info(f"Successfully connected as @{username}")
        return f"[{name}](https://twitter.com/{username})"
    except Exception as e:
        error_msg = f"Twitter authentication failed: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return {"error": error_msg}

async def send_tweet(message, text: str, pics: Optional[List[bytes]] = None) -> Dict:
    """Send a tweet with optional media."""
    try:
        if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET]):
            return {"error": "Twitter credentials are not properly configured"}

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
            
            try:
                for pic in pics:
                    media = api.media_upload(filename="media", file=pic)
                    media_ids.append(media.media_id)
            except Exception as e:
                error_msg = f"Failed to upload media: {str(e)}"
                logging.error(f"{error_msg}\n{traceback.format_exc()}")
                return {"error": error_msg}
        
        try:
            result = client.create_tweet(text=text, media_ids=media_ids if media_ids else None)
            logging.info(f"Tweet posted successfully: {result.data['id']}")
            return {"id": result.data["id"]}
        except Exception as e:
            if "Tweet text length exceeds limit" in str(e):
                try:
                    result = client.create_tweet(
                        text=text[:270] + "...",
                        media_ids=media_ids if media_ids else None
                    )
                    logging.info(f"Tweet posted with truncation: {result.data['id']}")
                    return {"id": result.data["id"]}
                except Exception as e2:
                    error_msg = f"Failed to post truncated tweet: {str(e2)}"
                    logging.error(f"{error_msg}\n{traceback.format_exc()}")
                    return {"error": error_msg}
            error_msg = f"Failed to post tweet: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            return {"error": error_msg}

    except Exception as e:
        error_msg = f"Twitter API error: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return {"error": error_msg}

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
        result = client.delete_tweet(tweet_id)
        if result.data.get("deleted"):
            logging.info(f"Tweet {tweet_id} deleted successfully")
            return {"success": True}
        return {"error": "Failed to delete tweet"}
    except Exception as e:
        error_msg = f"Error deleting tweet: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return {"error": error_msg}

def is_video_tweet(user_id, text: str) -> Optional[str]:
    """Check if text contains a tweet with video."""
    if not text or not text.startswith("https://twitter.com"):
        return None
        
    import re
    match = re.search(r"twitter\.com/\w+/status/(\d+)", text)
    if not match:
        return None
        
    return match.group(1)

async def get_video_download_link(chat_id, tweet_id: str) -> Optional[str]:
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
                    if mp4s:
                        # Sort by bitrate, highest first
                        best_video = sorted(mp4s, key=lambda x: x.get("bitrate", 0), reverse=True)[0]
                        logging.info(f"Found video URL for tweet {tweet_id}")
                        return best_video["url"]
    except Exception as e:
        error_msg = f"Error getting video link: {str(e)}"
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
    return None
