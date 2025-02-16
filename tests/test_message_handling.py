import pytest
from unittest.mock import MagicMock, patch
from pyrogram import types
from teletweet.utils.message_utils import (
    check_message_length,
    combine_messages,
    split_message,
    truncate_content
)
from teletweet.utils.message_store import MESSAGE_STORE

@pytest.fixture
def mock_message():
    message = MagicMock(spec=types.Message)
    message.text = "Main message content"
    message.caption = None
    message.id = 1
    return message

@pytest.fixture
def mock_reply_message():
    message = MagicMock(spec=types.Message)
    message.text = "Attached message content"
    message.caption = None
    message.id = 2
    return message

def test_combine_messages():
    main = "Main content"
    attached = "Attached content"
    combined = combine_messages(main, attached)
    assert combined == "Main content\n\nAttached content"
    
    # Test with empty messages
    assert combine_messages("", attached) == attached
    assert combine_messages(main, "") == main
    assert combine_messages("", "") == ""

def test_check_message_length():
    # Test Twitter length
    content = "x" * 280
    fits, result, excess = check_message_length(content, "twitter")
    assert fits is True
    assert result == content
    assert excess is None

    # Test with attached message
    main = "x" * 200
    attached = "y" * 100
    fits, result, excess = check_message_length(main, "twitter", attached)
    assert fits is False
    assert isinstance(result, list)  # Should return truncation options
    assert excess > 0

def test_split_message():
    content = "Line 1\nLine 2\nLine 3"
    attached = "Attached content"
    
    # Test without attached message
    parts = split_message(content, max_length=20)
    assert len(parts) > 0
    assert all(len(p) <= 20 for p in parts)
    
    # Test with attached message
    parts = split_message(content, max_length=20, attached_message=attached)
    assert len(parts) > 0
    assert all(len(p) <= 20 for p in parts)
    # Check if last part contains attached message
    assert "Attached content" in parts[-1]

def test_message_store():
    # Test storing messages
    message_id = 1
    MESSAGE_STORE[message_id] = "Original message"
    MESSAGE_STORE[f"attached_{message_id}"] = "Attached message"
    
    assert MESSAGE_STORE[message_id] == "Original message"
    assert MESSAGE_STORE[f"attached_{message_id}"] == "Attached message"
    
    # Test cleanup
    MESSAGE_STORE.pop(message_id)
    MESSAGE_STORE.pop(f"attached_{message_id}")
    assert message_id not in MESSAGE_STORE
    assert f"attached_{message_id}" not in MESSAGE_STORE

@pytest.mark.asyncio
async def test_message_handling(mock_message, mock_reply_message):
    from teletweet.handlers.messages import message_handler
    
    # Set up reply relationship
    mock_message.reply_to_message = mock_reply_message
    
    # Create mock client
    client = MagicMock()
    
    # Test message handling
    with patch('teletweet.utils.auth.user_check', lambda x: x):  # Mock auth decorator
        await message_handler(client, mock_message)
        
        # Verify messages were stored
        assert MESSAGE_STORE.get(mock_message.id) == mock_message
        assert MESSAGE_STORE.get(f"attached_{mock_message.id}") == mock_reply_message.text

def test_truncation():
    # Test normal truncation
    content = "This is a sample sentence. And another one. And a third."
    truncated = truncate_content(content, limit=30)
    assert len(truncated) <= 30
    assert truncated.endswith("...")
    
    # Test with attached message
    main = "Main message."
    attached = "Attached message."
    truncated = truncate_content(main, limit=20, attached_message=attached)
    assert len(truncated) <= 20
    assert truncated.endswith("...")

if __name__ == "__main__":
    pytest.main([__file__])
