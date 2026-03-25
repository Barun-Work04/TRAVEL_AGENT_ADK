import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

# Same agent as File 1, but now with google_search
# One line difference — tools=[google_search]
flight_agent_with_search = Agent(
    model="gemini-2.5-flash-lite",
    name="FlightAgentWithSearch",
    description="Finds real-time transport options using web search",
    instruction="""
    You are a transport specialist for India and worldwide destinations.
    ALWAYS use the google_search tool before answering.
    Search for current information about:
    - Flight prices and schedules
    - Train routes (check Indian Railways for Indian destinations)
    - Approximate travel times and costs
    Give prices in INR for Indian routes. Mention budget-friendly options first.
    For Sikkim: always search for NJP railway + shared jeep route.
    """,
    tools=[google_search]   # ← This one line gives the agent live web access
)

async def main():
    runner = InMemoryRunner(agent=flight_agent_with_search)

    print("\n--- File 1 guessed. This agent SEARCHES the web. ---\n")

    response = await runner.run_debug(
        "What are the current cheapest ways to travel from Kolkata to Gangtok in 2025?",
        verbose=False
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())