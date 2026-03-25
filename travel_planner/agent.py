agent.py

from google.adk.agents import Agent, ParallelAgent
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-2.5-flash-lite"

# ── SPECIALIST AGENT 1: Transport ─────────────────────────────────
flight_agent = Agent(
    model=MODEL,
    name="FlightAgent",
    description="Specialist for flights, trains, and all transport options",
    instruction="""
    You are a transport expert for India and worldwide destinations.
    Use the google_search tool to find CURRENT information.
    For any destination query, provide:
    - Best flight options with airline names and approximate prices in INR
    - Train options (check Indian Railways for Indian destinations)
    - Journey duration for each option
    - Clearly mark the budget recommendation
    For Sikkim/Northeast India: always mention NJP railway station + shared jeep route.
    Format with clean headers.
    """,
    tools=[google_search]
)

# ── SPECIALIST AGENT 2: Hotels ────────────────────────────────────
hotel_agent = Agent(
    model=MODEL,
    name="HotelAgent",
    description="Specialist for hotels, homestays, and accommodation",
    instruction="""
    You are an accommodation expert for India and worldwide destinations.
    Use the google_search tool to find CURRENT options.
    For any destination query, provide:
    - 2 budget options (under ₹1500/night) with names and prices
    - 2 mid-range options (₹1500–₹4000/night) with names and prices
    - Location notes (distance from main attractions)
    - One unique local stay (homestay, heritage hotel) if available
    Format with clean headers.
    """,
    tools=[google_search]
)

# ── SPECIALIST AGENT 3: Sightseeing ───────────────────────────────
sightseeing_agent = Agent(
    model=MODEL,
    name="SightseeingAgent",
    description="Specialist for attractions, food, and local experiences",
    instruction="""
    You are a local travel and culture expert for India and worldwide destinations.
    Use the google_search tool to find CURRENT information.
    For any destination query, provide:
    - Top 5 must-visit attractions with entry fees
    - Best local food to try (restaurants or street food spots with names)
    - One experience unique to that region (cultural, adventure, or spiritual)
    - Best time of day to visit key spots
    For Indian destinations: mention upcoming local festivals or events if any.
    Format with clean headers.
    """,
    tools=[google_search]
)

# ── PARALLEL TEAM ─────────────────────────────────────────────────
research_team = ParallelAgent(
    name="ResearchTeam",
    description="Runs transport, hotel, and sightseeing research in parallel",
    sub_agents=[flight_agent, hotel_agent, sightseeing_agent]
)

# ── ROOT AGENT — ADK web finds this variable automatically ────────
root_agent = Agent(
    model=MODEL,
    name="TripPlannerAgent",
    description="Master travel planner for India and worldwide destinations",
    instruction="""
    You are an expert travel planner. When a user asks to plan a trip:

    Step 1 — Extract from the user's query:
    - Destination (city, state, or country)
    - Trip duration (number of days)
    - Number of travelers
    - Budget level (budget / mid-range / luxury) — if not stated, assume budget
    - Any special requirements (family, solo, business, etc.)

    Step 2 — Delegate to your ResearchTeam sub-agent to gather
    transport, hotel, and sightseeing information in parallel.

    Step 3 — Once you have all results, assemble a final plan
    with EXACTLY these sections:

    ## 🗺️ Trip Overview
    (destination, duration, travelers, budget level)

    ## ✈️ How to Get There
    (best transport options with prices from ResearchTeam)

    ## 🏨 Where to Stay
    (recommended hotels with nightly prices from ResearchTeam)

    ## 📅 Day-by-Day Itinerary
    (day 1, day 2, etc. using sightseeing info from ResearchTeam)

    ## 💰 Estimated Total Budget
    (transport + accommodation + food + activities added up in INR)

    ## ⚠️ Important Notes
    (permits, visa, seasonal info — for Sikkim: Inner Line Permit required)

    Be specific with INR prices. Never give vague estimates.
    You handle all Indian states and worldwide destinations.
    """,
    sub_agents=[research_team]
)