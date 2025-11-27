# Shopping Assistant Agent - Kaggle Agents Intensive Capstone

## 1. The Problem: Why Shopping is Exhausting
We've all been there. You want to buy a new laptop or a pair of headphones. You start by Googling "best gaming laptop 2024". Then you open 10 tabs to check prices. Then you go to Reddit to see what *actual* people are saying because you don't trust the sponsored articles. Finally, you watch three 20-minute YouTube reviews to make sure the screen doesn't wobble.

By the time you're done, you've spent three hours and you're more confused than when you started.

**I built the Shopping Assistant Agent to fix this.** It's not just a search engine; it's a concierge that does the grunt work for you. It researches, watches videos, reads Reddit threads, and gives you a simple, backed-up recommendation.

## 2. Why Agents?
You might ask: *"Why not just use ChatGPT or a simple script?"*

The problem with a simple script is that it's brittle. If the Google search fails, the script crashes. If the user asks a follow-up question, the script has no memory.

The problem with a single LLM call is that it can't browse the live web effectively or browse *deeply*. It might hallucinate a product that doesn't exist.

**Agents are the right solution because:**
1.  **Specialization:** Just like in a real company, you don't want your CEO (Chat Agent) doing the janitorial work. By splitting tasks into specialized agents (Search, Reddit, YouTube), each one can be prompted and optimized for its specific job.
2.  **Resilience:** If the Reddit agent finds no results, the system doesn't fail—it just reports that and relies on the other sources.
3.  **Tool Use:** Agents can use tools (like a calculator or an API) to get accurate data, whereas a raw LLM is just guessing next tokens.

## 3. How It Works
Think of the Shopping Assistant as a team of experts working for you. When you ask for a recommendation, it doesn't just guess. It orchestrates a team of specialized AI agents to find the answer.

### The "Team" (Architecture)
I used a **Hub-and-Spoke Orchestrator Pattern** to keep things organized:

-   **The Boss (Chat Agent):** This is the main brain. It understands what you want (e.g., "I need a cheap laptop for school") and delegates tasks.
-   **The Researcher (Search Agent):** Scours Google for specs, prices, and "best of" lists.
-   **The Skeptic (Reddit Agent):** Dives into Reddit threads to find user complaints and real-world experiences.
-   **The Viewer (YouTube Agent):** Finds video reviews to see the product in action.
-   **The Memory Keeper (Memory Agent):** Remembers that you hate HP printers or that your budget is $500, so you don't have to repeat yourself.

### Key Features
-   **It Reads the Internet for You:** Combines professional reviews (Google), community gossip (Reddit), and visual proof (YouTube).
-   **It Knows You:** Remembers your preferences across conversations.
-   **It Delivers:** Can email you a full transcript of its research so you can read it later.
-   **It Knows Where You Are:** Automatically detects your location to give you local currency and availability.

## 4. Technical Highlights
Building this wasn't just about chaining prompts. Here are some of the cool technical details:

-   **Powered by Gemini 2.5 Flash:** I chose this model because it's fast and smart enough to handle complex reasoning without keeping the user waiting.
-   **Smart Batching:** To make the agent feel snappy, I implemented a "Session Manager" that batches initialization tasks (like loading memory and detecting location) so they happen in parallel. This cut startup time by ~50%.
-   **Privacy First:** Location data is used for context but never saved to disk.

## 5. A Typical Conversation
**Me:** "I'm looking for a noise-cancelling headset for travel. Budget is around $300."

**Agent:** *Thinking...*
1.  *Checks Memory:* "User prefers Sony over Bose."
2.  *Search Agent:* Finds the Sony WH-1000XM5 and Bose QC45.
3.  *Reddit Agent:* Finds a thread saying the Sony XM5s get hot on ears.
4.  *YouTube Agent:* Finds a flight test video.

**Agent:** "Based on your preference for Sony, the WH-1000XM5 is a strong contender. However, Reddit users mention they can get warm during long flights. Here's a video review comparing them to the Bose QC45..."

**Me:** "Email me the details."

**Agent:** *Sends email transcript.*

## 6. Challenges & Lessons Learned
This project taught me a lot about the nuances of AI agents:
-   **Herding Cats:** Getting multiple agents to talk to each other without getting confused was tricky. I had to refine the system prompts to ensure clear hand-offs.
-   **Link Rot:** AI models love to hallucinate links or break them. I had to add specific instructions (and a bit of code) to ensure YouTube links always opened correctly in new tabs.
-   **Speed vs. Accuracy:** Balancing the depth of research with response time is an art. I learned that sometimes a "good enough" answer fast is better than a perfect answer that takes 2 minutes.

## 7. What's Next?
I'm not done yet. In the future, I'd love to add:
-   **Price Alerts:** A background agent that watches for price drops.
-   **One-Click Buy:** Integration with shopping carts.
-   **Voice Mode:** So I can ask for advice while driving.

## 8. Conclusion
The Shopping Assistant Agent is my attempt to take the "work" out of homework. It demonstrates how AI can be more than just a chatbot—it can be a useful tool that interacts with the real world to save us time.
