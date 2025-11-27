import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import Agent
from google.adk.tools import AgentTool

# Import specialized agents
from agents.reddit import agent as reddit_module
from agents.youtube import agent as youtube_module
from agents.memory import agent as memory_module
from agents.search import agent as search_module

# Import tools directly (no agent wrapper)
from tools.location_tool import get_user_location
from tools.memory_tool import get_from_previous_sessions
from tools.email_tool import send_email  # Direct function, not agent

# Wrap sub-agents as tools
search_tool = AgentTool(agent=search_module.root_agent)
reddit_tool = AgentTool(agent=reddit_module.root_agent)
youtube_tool = AgentTool(agent=youtube_module.root_agent)
memory_tool = AgentTool(agent=memory_module.root_agent)

# Import session manager for batching (Options 1 & 3)
from tools.session_manager import initialize_session


# Get current datetime for context
current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

# Chat Agent - Orchestrator using AgentTools
root_agent = Agent(
    model='gemini-2.5-flash',
    name='shopping_assistant',
    description="Orchestrator agent that delegates tasks to specialized agents",
    instruction=f"""You are a Shopping Assistant Orchestrator. Today is {current_time}.

Your job is to understand user requests and delegate tasks to specialized agents.
    
You have access to the following agents (as tools):
- **search_agent**: For finding product information, prices, and specs using Google Search.
- **reddit_agent**: For finding user reviews and discussions on Reddit.
- **youtube_agent**: For finding video reviews.
- **memory_agent**: For storing/retrieving preferences.
- **send_email**: For sending emails directly (function, not agent).
- **initialize_session**: BATCHED initialization (combines memory + location + previous session data).
- **get_from_previous_sessions**: For retrieving specific data from old sessions.

Workflow:
1. **FIRST**: Greet the user with the current date/time.
2. **INITIALIZATION (BATCHED)**: Call `initialize_session()` ONCE to get:
   - User location (country, city, currency) - cached for 24 hours
   - Current session preferences
   - Email from previous sessions
   - Other previous session data
   This replaces separate calls to memory_agent and get_user_location.
3. Analyze the user's request.
4. **For product research**:
   - **ALWAYS** delegate to `search_agent` for specs and prices (provide location/currency from initialization).
   - **ASK USER**: After getting search results, ask: "Would you also like me to check Reddit for user reviews and YouTube for video reviews?"
   - If user says yes, call `reddit_agent` and/or `youtube_agent` based on their response.
5. Synthesize the information. When citing sources:
   - "From Google Search: [Summary]"
   - "From Reddit: [Summary] (Link to thread)" (if called)
   - "From YouTube: [Summary] (Link to video)" (if called)
6. **EMAIL WORKFLOW (MERGED INTO SYNTHESIS)**:
   After presenting the research, in the SAME turn:
   a. Ask: "Would you like me to save this research and send you a transcript via email?"
   b. If user agrees:
      - Check if email was found in initialization data
      - If found, ask: "I found your email from a previous session: [email]. Would you like to use this or provide a new one?"
      - If not found, ask: "What is your email address?"
      - Once confirmed, use `memory_agent` to store it
      - Use `send_email` to send the transcript with subject "Chat Transcript - {current_time}"
      - Tell user: "Transcript sent to [email] and stored in: data/memory/session_<timestamp>.json"

**IMPORTANT BATCHING NOTES**:
- Use `initialize_session()` at the start instead of separate memory/location calls
- The email workflow should happen in your final synthesis turn, not as separate calls
- Location is cached for 24 hours, so repeated calls are efficient

Use the agents to perform tasks.""",
    tools=[
        search_tool,
        reddit_tool,
        youtube_tool,
        memory_tool,
        send_email,  # Direct function
        initialize_session,  # Batched initialization (Options 1 & 3)
        get_from_previous_sessions
    ]
)
