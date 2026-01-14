from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from customer_support_chat.app.services.tools import (
    search_flights,
    update_ticket_to_new_flight,
    cancel_ticket,
)
from customer_support_chat.app.agents import load_agent_config, resolve_tools
from customer_support_chat.app.services.assistants.assistant_base import Assistant, CompleteOrEscalate, llm

flight_agent_config = load_agent_config("flight_booking")

# Flight booking assistant prompt
flight_booking_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", flight_agent_config.system_prompt),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

flight_tool_registry = {
    "search_flights": search_flights,
    "update_ticket_to_new_flight": update_ticket_to_new_flight,
    "cancel_ticket": cancel_ticket,
}

update_flight_safe_tools = resolve_tools(
    flight_agent_config,
    flight_tool_registry,
    ("safe_tools",),
)
update_flight_sensitive_tools = resolve_tools(
    flight_agent_config,
    flight_tool_registry,
    ("sensitive_tools",),
)
update_flight_tools = update_flight_safe_tools + update_flight_sensitive_tools

# Create the flight booking assistant runnable
update_flight_runnable = flight_booking_prompt | llm.bind_tools(
    update_flight_tools + [CompleteOrEscalate]
)

# Instantiate the flight booking assistant
flight_booking_assistant = Assistant(update_flight_runnable)
