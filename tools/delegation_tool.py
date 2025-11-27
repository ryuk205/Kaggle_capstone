import requests
import json

def call_search_agent(query: str):
    """
    Delegates a search task to the Search Agent.
    Use this to find product information, prices, and specs.
    """
    return _call_agent("search_agent", query)

def call_reddit_agent(query: str):
    """
    Delegates a task to the Reddit Agent.
    Use this to find user reviews, discussions, and sentiment.
    """
    return _call_agent("reddit_agent", query)

def call_youtube_agent(query: str):
    """
    Delegates a task to the YouTube Agent.
    Use this to find video reviews and summaries.
    """
    return _call_agent("youtube_agent", query)

def call_email_agent(query: str):
    """
    Delegates a task to the Email Agent.
    Use this to send emails with summaries or lists.
    """
    return _call_agent("email_agent", query)

def call_memory_agent(query: str):
    """
    Delegates a task to the Memory Agent.
    Use this to store or retrieve user preferences.
    """
    return _call_agent("memory_agent", query)

def _call_agent(agent_name: str, query: str):
    """Helper to call an agent via HTTP."""
    url = f"http://127.0.0.1:8000/agents/{agent_name}/chat" # Assumed endpoint
    # Note: The actual endpoint might vary. 
    # If ADK doesn't expose easy endpoints, we might need a different approach.
    # But let's try this standard pattern.
    
    # Alternative: If ADK exposes a single /chat endpoint with agent selection?
    # Or maybe we just use the 'query' endpoint?
    
    # Let's assume a simple POST structure.
    try:
        # Trying to guess the ADK API structure.
        # Usually: POST /agent/{name}/chat with json={"prompt": query}
        response = requests.post(url, json={"prompt": query}, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", response.text)
        else:
            return f"Error calling {agent_name}: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Failed to communicate with {agent_name}: {e}"
