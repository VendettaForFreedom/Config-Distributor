import asyncio
import logging
from pyrogram import Client, errors
from ..config import GROUP_ID, CHANNEL_ID, CHANNEL_AD_MESSAGE_ID

async def forward_ad_message(client: Client):
    """Forward ad message from channel to group after delay."""
    try:
        # Wait for 1 hour
        await asyncio.sleep(3600)

        # Forward the ad message
        await client.forward_messages(
            chat_id=GROUP_ID,
            from_chat_id=CHANNEL_ID,
            message_ids=[CHANNEL_AD_MESSAGE_ID]
        )
        logging.info(f"Successfully forwarded ad message to group {GROUP_ID}")
    except errors.FloodWait as e:
        logging.warning(f"Rate limit hit, waiting {e.value} seconds")
        await asyncio.sleep(e.value)
        await forward_ad_message(client)
    except Exception as e:
        logging.error(f"Error forwarding ad message from {CHANNEL_ID} to {GROUP_ID}: {e}")
