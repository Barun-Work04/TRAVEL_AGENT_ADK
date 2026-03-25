import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from dotenv import load_dotenv

load_dotenv()

# Constants — these identify the app, user, and session
APP_NAME = "travel_memory_demo"
USER_ID  = "user1"
SESSION_ID = "session1"

travel_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="TravelMemoryAgent",
    description="A travel agent that remembers the full conversation",
    instruction="""
    You are a helpful travel assistant for India and worldwide destinations.
    Remember everything the user has said in this conversation.
    Refer back to earlier details (destination, duration, preferences)
    when answering follow-up questions. Never ask for info the user already gave.
    """
)

async def chat(runner, session_id, message):
    """Send one message and print the agent's reply."""
    print(f"\nYou: {message}")
    user_message = Content(role="user", parts=[Part(text=message)])

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Agent: {event.content.parts[0].text}")

async def main():
    # Session service stores the conversation history in memory
    session_service = InMemorySessionService()

    runner = Runner(
        agent=travel_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Create the session before sending messages
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    print("=== Memory Demo: Watch the agent remember across turns ===")

    # Turn 1 — gives the destination and duration
    await chat(runner, SESSION_ID, "I want to plan a trip to Sikkim for 3 days.")

    # Turn 2 — agent must recall Sikkim without being told again
    await chat(runner, SESSION_ID, "What documents do I need to enter?")

    # Turn 3 — agent must recall 3 days + Sikkim together
    await chat(runner, SESSION_ID, "Give me a day-wise plan based on what I told you.")

if __name__ == "__main__":
    asyncio.run(main())