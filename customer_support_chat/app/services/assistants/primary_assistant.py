from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from customer_support_chat.app.services.tools import (
    search_flights,
    lookup_policy,
)
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults
from customer_support_chat.app.agents import load_agent_config, resolve_tools
from customer_support_chat.app.services.assistants.assistant_base import Assistant, llm
from customer_support_chat.app.core.state import State
from pydantic import BaseModel, Field

# Define task delegation tools
class ToFlightBookingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle flight updates and cancellations."""
    request: str = Field(description="Any necessary follow-up questions the update flight assistant should clarify before proceeding.")

class ToBookCarRental(BaseModel):
    """Transfers work to a specialized assistant to handle car rental bookings."""
    location: str = Field(description="The location where the user wants to rent a car.")
    start_date: str = Field(description="The start date of the car rental.")
    end_date: str = Field(description="The end date of the car rental.")
    request: str = Field(description="Any additional information or requests from the user regarding the car rental.")

class ToHotelBookingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle hotel bookings."""
    location: str = Field(description="The location where the user wants to book a hotel.")
    checkin_date: str = Field(description="The check-in date for the hotel.")
    checkout_date: str = Field(description="The check-out date for the hotel.")
    request: str = Field(description="Any additional information or requests from the user regarding the hotel booking.")

class ToBookExcursion(BaseModel):
    """Transfers work to a specialized assistant to handle trip recommendation and other excursion bookings."""
    location: str = Field(description="The location where the user wants to book a recommended trip.")
    request: str = Field(description="Any additional information or requests from the user regarding the trip recommendation.")

primary_agent_config = load_agent_config("primary")

# Primary assistant prompt
primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", primary_agent_config.system_prompt),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

primary_tool_registry = {
    "DuckDuckGoSearchResults": DuckDuckGoSearchResults(max_results=10),
    "search_flights": search_flights,
    "lookup_policy": lookup_policy,
    "ToFlightBookingAssistant": ToFlightBookingAssistant,
    "ToBookCarRental": ToBookCarRental,
    "ToHotelBookingAssistant": ToHotelBookingAssistant,
    "ToBookExcursion": ToBookExcursion,
}

primary_assistant_tools = resolve_tools(
    primary_agent_config,
    primary_tool_registry,
    ("safe_tools", "delegation_tools"),
)

# Create the primary assistant runnable
primary_assistant_runnable = primary_assistant_prompt | llm.bind_tools(primary_assistant_tools)

# Instantiate the primary assistant
primary_assistant = Assistant(primary_assistant_runnable)
