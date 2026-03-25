import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from dotenv import load_dotenv

load_dotenv()

# A single agent — no tools, no memory, just the model
flight_agent = Agent(
    model="gemini-2.5-flash-lite",          
    name="FlightAgent",
    description="Finds transport options between cities",
    instruction="""
    You are a transport specialist for India and worldwide destinations.
    When asked about travel between two places, suggest:
    - Flight options with approximate prices in INR
    - Train options (especially Indian Railways for Indian routes)
    - Bus options if relevant
    - Total travel time for each option
    Always give budget options first. Be specific with prices and times.
    For Sikkim: always mention NJP railway station + shared jeep route.
    """
)

async def main():
    runner = InMemoryRunner(agent=flight_agent)
    print("\n--- FlightAgent Response ---\n")

    # run_debug returns the final text — good for quick testing
    response = await runner.run_debug(
        "How do I travel from Kolkata to Gangtok, Sikkim?",
        verbose=False
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())