import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import Agent
from tools.reddit_tool import scrape_reddit

# Reddit Agent - Scrapes Reddit for discussions
root_agent = Agent(
    model='gemini-2.5-flash',
    name='reddit_agent',
    description="Finds user discussions and reviews on Reddit",
    instruction="""You are a Reddit Agent specialized in finding community discussions.

Use the scrape_reddit tool to find:
- User experiences and reviews
- Common issues or complaints
- Recommendations from real users
- Sentiment analysis

Summarize key points and overall sentiment.""",
    tools=[scrape_reddit]
)
