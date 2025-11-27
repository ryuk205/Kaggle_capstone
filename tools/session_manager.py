import json
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta

from tools.memory_tool import _memory_manager, get_from_previous_sessions
from tools.location_tool import get_user_location as _get_location_raw

# Configuration
# Location data is kept in memory only, not persisted to disk
LOCATION_CACHE_HOURS = 24


class SessionManager:
    """
    Centralized session management that combines multiple operations
    to reduce API calls (Batching Options 1 & 3).
    
    Note: Location data is kept in memory during the session only
    and is NOT persisted to disk for privacy reasons.
    """
    
    def __init__(self):
        # In-memory cache only - location data not persisted
        self.cache = {
            'location': None  # Will be populated during session
        }
    
    def get_cached_location(self) -> Optional[Dict]:
        """
        Returns cached location if exists in current session and < 24 hours old.
        Location is kept in memory only, not persisted to disk.
        """
        if 'location' not in self.cache or self.cache['location'] is None:
            return None
        
        location_data = self.cache['location']
        cached_time = location_data.get('timestamp', 0)
        
        # Check if cache is still valid (< 24 hours)
        if time.time() - cached_time < LOCATION_CACHE_HOURS * 3600:
            return location_data
        
        return None
    
    def update_location_cache(self, location_data: Dict):
        """
        Update location cache with timestamp.
        Location is stored in memory only for the current session.
        """
        location_data['timestamp'] = time.time()
        location_data['cached'] = True
        self.cache['location'] = location_data
        # Note: Location data is NOT saved to disk for privacy
    
    def get_location(self, use_cache: bool = True) -> Dict:
        """
        Get user location with caching support.
        Returns structured dict instead of formatted string.
        """
        # Try cache first
        if use_cache:
            cached = self.get_cached_location()
            if cached:
                return cached
        
        # Fetch fresh location
        location_str = _get_location_raw()
        
        # Parse the string response into structured data
        location_data = self._parse_location_string(location_str)
        location_data['cached'] = False
        
        # Cache it
        self.update_location_cache(location_data)
        
        return location_data
    
    def _parse_location_string(self, location_str: str) -> Dict:
        """Parse location string into structured dict."""
        lines = location_str.strip().split('\n')
        data = {
            'country': 'Unknown',
            'city': 'Unknown',
            'timezone': 'Unknown',
            'currency': 'USD'
        }
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().replace('- ', '').lower()
                value = value.strip()
                if key in data:
                    data[key] = value
        
        return data
    
    def initialize_session(self) -> Dict:
        """
        OPTION 1: Combine Memory + Location Check
        
        Single call that returns all initialization data:
        - Current session preferences
        - Location (in-memory cache only, not persisted)
        - Email from previous sessions
        
        This reduces 2+ API calls to 1 operation.
        
        Note: Location data is kept in memory during session only
        and deleted when session closes (not saved to disk).
        """
        result = {
            'preferences': {},
            'location': {},
            'email': None,
            'previous_session_data': {}
        }
        
        # Get all current session preferences
        result['preferences'] = _memory_manager.memory_service.to_dict()
        
        # Get location (with caching)
        result['location'] = self.get_location(use_cache=True)
        
        # Check for email in previous sessions
        email = get_from_previous_sessions('user_email')
        if email:
            result['email'] = email
        
        # Get other useful data from previous sessions
        for key in ['user_preferences', 'favorite_categories', 'budget']:
            value = get_from_previous_sessions(key)
            if value:
                result['previous_session_data'][key] = value
        
        return result
    
    def prefetch_session_data(self) -> Dict:
        """
        OPTION 3: Pre-fetch Common Data
        
        Called on startup to load all common data that might be needed.
        This reduces repeated calls throughout the session.
        """
        return self.initialize_session()


# Global instance
_session_manager = SessionManager()


def initialize_session() -> str:
    """
    Initialize session with all common data (Options 1 & 3).
    Returns formatted string for agent consumption.
    """
    data = _session_manager.initialize_session()
    
    # Format for agent
    output = ["=== Session Initialized ===\n"]
    
    # Location info
    loc = data['location']
    cache_status = "(cached)" if loc.get('cached') else "(fresh)"
    output.append(f"[LOCATION] {cache_status}:")
    output.append(f"  - Country: {loc.get('country', 'Unknown')}")
    output.append(f"  - City: {loc.get('city', 'Unknown')}")
    output.append(f"  - Currency: {loc.get('currency', 'USD')}")
    output.append(f"  - Timezone: {loc.get('timezone', 'Unknown')}\n")
    
    # Current session preferences
    if data['preferences']:
        output.append("[CURRENT SESSION DATA]:")
        for key, value in data['preferences'].items():
            output.append(f"  - {key}: {value}")
        output.append("")
    
    # Previous session data
    if data['email']:
        output.append(f"[EMAIL] From previous session: {data['email']}\n")
    
    if data['previous_session_data']:
        output.append("[PREVIOUS SESSION DATA]:")
        for key, value in data['previous_session_data'].items():
            output.append(f"  - {key}: {value}")
        output.append("")
    
    if not data['preferences'] and not data['email'] and not data['previous_session_data']:
        output.append("[INFO] No previous session data found (new user)\n")
    
    return '\n'.join(output)


def prefetch_session_data() -> Dict:
    """
    Pre-fetch all common session data on startup.
    Returns raw dict for programmatic use.
    """
    return _session_manager.prefetch_session_data()
