from typing import Dict, Any
from threading import Lock

class MessageStore:
    """Thread-safe message store for handling message data."""
    
    def __init__(self):
        self._store: Dict[Any, Any] = {}
        self._lock = Lock()
        
    def __getitem__(self, key: Any) -> Any:
        with self._lock:
            return self._store[key]
            
    def __setitem__(self, key: Any, value: Any):
        with self._lock:
            self._store[key] = value
            
    def __delitem__(self, key: Any):
        with self._lock:
            del self._store[key]
            
    def get(self, key: Any, default: Any = None) -> Any:
        with self._lock:
            return self._store.get(key, default)
            
    def pop(self, key: Any, default: Any = None) -> Any:
        with self._lock:
            return self._store.pop(key, default)
            
    def clear(self):
        with self._lock:
            self._store.clear()
            
    def keys(self):
        with self._lock:
            return list(self._store.keys())

    def items(self):
        """Get all items in the store."""
        with self._lock:
            return list(self._store.items())
    
    def values(self):
        """Get all values in the store."""
        with self._lock:
            return list(self._store.values())
    
    def cleanup_expired(self, max_age: int = 3600):
        """Remove messages older than max_age seconds."""
        import time
        current_time = time.time()
        
        with self._lock:
            to_remove = []
            for key, value in self._store.items():
                if isinstance(value, dict) and 'timestamp' in value:
                    if current_time - value['timestamp'] > max_age:
                        to_remove.append(key)
            
            for key in to_remove:
                del self._store[key]

# Global message store instance
MESSAGE_STORE = MessageStore()
