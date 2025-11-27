import json
import os
from pathlib import Path

import time

# Configuration
MEMORY_DIR = Path("data/memory")
SESSION_ID = str(int(time.time()))
MEMORY_FILE = MEMORY_DIR / f"session_{SESSION_ID}.json"

class InMemoryMemoryService:
    """
    A simple in-memory key-value store.
    """
    def __init__(self):
        self._store = {}

    def set(self, key: str, value: str):
        self._store[key] = value

    def get(self, key: str):
        return self._store.get(key)

    def load_from_dict(self, data: dict):
        self._store.update(data)

    def to_dict(self) -> dict:
        return self._store.copy()

class HybridMemoryManager:
    """
    Manages memory using both InMemoryMemoryService and a JSON file for persistence.
    """
    def __init__(self):
        self.memory_service = InMemoryMemoryService()
        self._load_from_disk()

    def _load_from_disk(self):
        """Loads data from the JSON file into the in-memory service."""
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                    self.memory_service.load_from_dict(data)
            except Exception as e:
                print(f"Warning: Failed to load memory file: {e}")

    def _save_to_disk(self):
        """Saves the current in-memory state to the JSON file."""
        # Ensure directory exists
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(MEMORY_FILE, 'w') as f:
                json.dump(self.memory_service.to_dict(), f, indent=4)
        except Exception as e:
            return f"Error saving memory: {str(e)}"

    def store(self, key: str, value: str):
        self.memory_service.set(key, value)
        self._save_to_disk()
        return f"Stored {key}: {value}"

    def retrieve(self, key: str):
        val = self.memory_service.get(key)
        if val is None:
            return "Key not found."
        return val

# Global instance
_memory_manager = HybridMemoryManager()

def store_preference(key: str, value: str):
    """
    Stores a user preference or data.
    """
    return _memory_manager.store(key, value)

def retrieve_preference(key: str):
    """
    Retrieves a user preference or data.
    """
    return _memory_manager.retrieve(key)

def get_from_previous_sessions(key: str):
    """
    Searches all previous session files for a specific key.
    Returns the most recently stored value, or None if not found.
    """
    if not MEMORY_DIR.exists():
        return None
    
    # Get all session files, sorted by modification time (newest first)
    session_files = sorted(
        MEMORY_DIR.glob("session_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                if key in data:
                    return data[key]
        except Exception:
            continue
    
    return None

def get_all_preferences() -> dict:
    """
    Returns all stored preferences in one call.
    Used for batching operations (Option 1).
    """
    return _memory_manager.memory_service.to_dict()

def get_session_summary() -> dict:
    """
    Returns summary of current + previous session data.
    Useful for initialization (Option 3).
    """
    current = _memory_manager.memory_service.to_dict()
    
    # Get commonly used keys from previous sessions
    previous = {}
    for key in ['user_email', 'user_preferences', 'favorite_categories', 'budget']:
        value = get_from_previous_sessions(key)
        if value:
            previous[key] = value
    
    return {
        'current_session': current,
        'previous_sessions': previous
    }

