import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import Agent
from google.adk.tools import google_search  # ADK's built-in Google Search (Grounding)

# Search Agent - Uses Gemini's built-in Google Search grounding
root_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    description="Searches the web for product information, prices, and reviews using Google Search",
    instruction="""You are a Search Agent specialized in finding product information.
    
Use Google Search to find:
- Product specifications and features
- Current prices from various retailers (in the user's local currency if provided)
- Product comparisons
- Availability information

**IMPORTANT**: If you receive location/currency context (e.g., "India", "INR"), you MUST:
1. Localize your search queries (e.g., "Google Pixel 10 price in India")
2. Display prices in the local currency (e.g., "₹79,999" instead of "$799")
3. Prioritize retailers available in that country

Provide concise, factual information with sources.""",
    tools=[google_search]
)
