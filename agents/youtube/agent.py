import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import Agent
from tools.youtube_tool import search_youtube, summarize_video

# YouTube Agent - Finds and summarizes video reviews
root_agent = Agent(
    model='gemini-2.5-flash',
    name='youtube_agent',
    description="Finds video reviews and provides summaries",
    instruction="""You are a YouTube Agent specialized in video content.

Use your tools to:
- search_youtube: Find relevant product review videos
- summarize_video: Provide video summaries

Focus on:
- Professional reviews
- Unboxing videos
- Comparison videos
- User testimonials""",
    tools=[search_youtube, summarize_video]
)
