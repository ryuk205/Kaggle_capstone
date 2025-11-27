import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import Agent
from tools.memory_tool import store_preference, retrieve_preference

# Memory Agent - Manages user preferences (exclusive storage access)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='memory_agent',
    description="Stores and retrieves user preferences and shopping history",
    instruction="""You are a Memory Agent with exclusive access to user data storage.

Use your tools to:
- store_preference: Save user preferences (budget, sizes, brands, etc.)
- retrieve_preference: Recall saved preferences

Manage:
- Shopping preferences
- Budget constraints
- Size information
- Brand preferences
- Past purchases""",
    tools=[store_preference, retrieve_preference]
)
