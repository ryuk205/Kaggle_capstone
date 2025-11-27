Problem Statement --
We've all been there. You want to buy a new laptop or a pair of headphones. You start by Googling "best gaming laptop 2024". Then you open 10 tabs to check prices. Then you go to Reddit to see what actual people are saying because you don't trust the sponsored articles. Finally, you watch three 20-minute YouTube reviews to make sure the screen doesn't wobble.

Why agents? -- Why are agents the right solution to this problem
You might ask: "Why not just use ChatGPT or a simple script?"

The problem with a simple script is that it's brittle. If the Google search fails, the script crashes. If the user asks a follow-up question, the script has no memory.

The problem with a single LLM call is that it can't browse the live web effectively or browse deeply. It might hallucinate a product that doesn't exist.

Agents are the right solution because:

Specialization: Just like in a real company, you don't want your CEO (Chat Agent) doing the janitorial work. By splitting tasks into specialized agents (Search, Reddit, YouTube), each one can be prompted and optimized for its specific job.
Resilience: If the Reddit agent finds no results, the system doesn't fail—it just reports that and relies on the other sources.
Tool Use: Agents can use tools (like a calculator or an API) to get accurate data, whereas a raw LLM is just guessing next tokens.
What you created --
Think of the Shopping Assistant as a team of experts working for you. When you ask for a recommendation, it doesn't just guess. It orchestrates a team of specialized AI agents to find the answer.

The "Team" (Architecture)
I used a Hub-and-Spoke Orchestrator Pattern to keep things organized:

The Boss (Chat Agent): This is the main brain. It understands what you want (e.g., "I need a cheap laptop for school") and delegates tasks.
The Researcher (Search Agent): Scours Google for specs, prices, and "best of" lists.
The Skeptic (Reddit Agent): Dives into Reddit threads to find user complaints and real-world experiences.
The Viewer (YouTube Agent): Finds video reviews to see the product in action.
The Memory Keeper (Memory Agent): Remembers that you hate HP printers or that your budget is $500, so you don't have to repeat yourself.
Key Features
It Reads the Internet for You: Combines professional reviews (Google), community gossip (Reddit), and visual proof (YouTube).
It Knows You: Remembers your preferences across conversations.
It Delivers: Can email you a full transcript of its research so you can read it later.
It Knows Where You Are: Automatically detects your location to give you local currency and availability.
Demo -- Show your solution
A Typical Conversation Me: "I'm looking for a noise-cancelling headset for travel. Budget is around $300."

Agent: Thinking…

Checks Memory: "User prefers Sony over Bose."
Search Agent: Finds the Sony WH-1000XM5 and Bose QC45.
Reddit Agent: Finds a thread saying the Sony XM5s get hot on ears.
YouTube Agent: Finds a flight test video.
Agent: "Based on your preference for Sony, the WH-1000XM5 is a strong contender. However, Reddit users mention they can get warm during long flights. Here's a video review comparing them to the Bose QC45…"

Me: "Email me the details."

Agent: Sends email transcript.

The Build -- How you created it, what tools or technologies you used.
If I had more time, this is what I'd do
I'd love to add:

Price Alerts: A background agent that watches for price drops.
One-Click Buy: Integration with shopping carts.
Voice Mode: So I can ask for advice while driving.