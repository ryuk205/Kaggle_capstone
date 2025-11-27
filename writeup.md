# Shopping Assistant Agent - Kaggle Agents Intensive Capstone

## 1. Problem Statement
Shopping for products often involves tedious research across multiple platforms: checking specs on Google, reading user reviews on Reddit, watching video reviews on YouTube, and comparing prices. This process is time-consuming and disjointed. 

The **Shopping Assistant Agent** solves this by acting as a unified concierge that autonomously researches products across these sources, synthesizes the information, and even emails a transcript to the user, saving hours of manual work.

## 2. Solution Overview
The Shopping Assistant is a multi-agent system designed to act as a personal shopping concierge. It leverages the power of Google's Gemini models to understand user requests, decompose them into research tasks, and synthesize findings from diverse sources into a coherent recommendation.

### Key Features
-   **Multi-Source Research:** Aggregates data from Google Search (specs/prices), Reddit (community sentiment), and YouTube (video reviews).
-   **Personalized Memory:** Remembers user preferences (budget, brands) across sessions to tailor recommendations.
-   **Actionable Output:** Provides a consolidated summary and can email the full transcript to the user.
-   **Location Awareness:** Automatically detects the user's country to provide relevant search results and currency.

## 3. System Architecture
The system follows a **Hub-and-Spoke Orchestrator Pattern**:

-   **Chat Agent (Orchestrator):** The central brain that analyzes user requests, plans tasks, and delegates to specialized sub-agents.
-   **Specialized Agents:**
    -   **Search Agent:** Uses Google Search for real-time product specs and pricing.
    -   **Reddit Agent:** Scrapes Reddit for authentic user discussions and sentiment.
    -   **YouTube Agent:** Finds video reviews for visual confirmation.
    -   **Memory Agent:** Persists user preferences (budget, favorite brands) across sessions.
-   **Tools:**
    -   **Session Manager:** Handles batched initialization and location caching for efficiency.
    -   **Email Tool:** Delivers research summaries to the user via SMTP.

### Technical Implementation
-   **Framework:** Built using the Google Agent Development Kit (ADK).
-   **Model:** Powered by `gemini-2.5-flash` for fast and reasoning-capable performance.
-   **Optimization:** Implemented batching for initialization tasks (memory + location) to reduce API calls by ~50%.
-   **Privacy:** Location data is cached in-memory only and not persisted to disk.

## 4. Demo Flow
1.  **Initialization:** Agent greets user, detects location (cached), and retrieves past preferences.
2.  **Request:** User asks "Recommend a gaming laptop under $1500".
3.  **Research:** Agent searches Google for options, then checks Reddit and YouTube for the top pick.
4.  **Synthesis:** Agent presents a consolidated recommendation with pros/cons and sources.
5.  **Action:** Agent offers to email the research.
6.  **Completion:** Transcript sent to user's email.

## 5. Challenges & Learnings
-   **Tool Output Formatting:** Ensuring the LLM preserved HTML links (e.g., for YouTube) required explicit instruction tuning in the system prompt.
-   **Latency:** Orchestrating multiple agents can be slow. We addressed this by batching initialization tasks and using the faster `gemini-2.5-flash` model.
-   **Context Management:** Managing the context window across multiple agent turns required careful summarization of tool outputs.

## 6. Future Improvements
-   **Price Tracking:** Implement a background job to monitor price changes for saved items.
-   **Direct Purchasing:** Integrate with affiliate APIs to allow "Add to Cart" functionality.
-   **Voice Interface:** Add speech-to-text and text-to-speech for a hands-free experience.

## 7. Conclusion
The Shopping Assistant Agent demonstrates the power of agentic workflows to transform a fragmented user task into a seamless, conversational experience. By combining the reasoning of Gemini with specialized tools, we've built a helpful assistant that saves users time and effort.
