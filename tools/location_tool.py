import requests

def get_user_location():
    """
    Gets the user's approximate location using IP geolocation.
    Uses ip-api.com (free, open-source, no API key required).
    Returns country, city, timezone, and currency information.
    """
    try:
        # Use ip-api.com - free and open source
        response = requests.get('http://ip-api.com/json/', timeout=5)
        
        if response.status_code != 200:
            return """Location detection failed.
- Country: Unknown
- Currency: USD (fallback)"""
        
        data = response.json()
        
        if data.get('status') == 'fail':
            return f"""Location detection failed: {data.get('message', 'Unknown error')}
- Currency: USD (fallback)"""
        
        # Extract location info
        country = data.get('country', 'Unknown')
        city = data.get('city', 'Unknown')
        timezone_name = data.get('timezone', 'Unknown')
        currency = data.get('currency', 'USD')  # USD fallback
        
        return f"""Location detected (via IP geolocation):
- Country: {country}
- City: {city}
- Timezone: {timezone_name}
- Currency: {currency}"""
        
    except requests.exceptions.Timeout:
        return """Location detection timed out.
- Currency: USD (fallback)"""
    except requests.exceptions.RequestException as e:
        return f"""Error detecting location: {str(e)}
- Currency: USD (fallback)"""
    except Exception as e:
        return f"""Unexpected error: {str(e)}
- Currency: USD (fallback)"""

