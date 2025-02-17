"""Message storage utility for TeleTweet."""

from typing import Dict, Any

class MessageStore:
    """Message store to hold messages and related data during processing."""
    def __init__(self):
        self._store: Dict[Any, Any] = {}

    def __getitem__(self, key):
        return self._store.get(key)

    def __setitem__(self, key, value):
        self._store[key] = value
    
    def get(self, key, default=None):
        return self._store.get(key, default)

    def pop(self, key, default=None):
        return self._store.pop(key, default)
    
    def keys(self):
        return self._store.keys()

# Global message store instance
MESSAGE_STORE = MessageStore()
