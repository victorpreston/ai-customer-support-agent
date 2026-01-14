from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from customer_support_chat.app.services.tools import (
    search_hotels,
    book_hotel,
    update_hotel,
    cancel_hotel,
)
from customer_support_chat.app.agents import load_agent_config, resolve_tools
from customer_support_chat.app.services.assistants.assistant_base import Assistant, CompleteOrEscalate, llm

hotel_agent_config = load_agent_config("hotel_booking")

# Hotel booking assistant prompt
hotel_booking_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", hotel_agent_config.system_prompt),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

hotel_tool_registry = {
    "search_hotels": search_hotels,
    "book_hotel": book_hotel,
    "update_hotel": update_hotel,
    "cancel_hotel": cancel_hotel,
}

book_hotel_safe_tools = resolve_tools(
    hotel_agent_config,
    hotel_tool_registry,
    ("safe_tools",),
)
book_hotel_sensitive_tools = resolve_tools(
    hotel_agent_config,
    hotel_tool_registry,
    ("sensitive_tools",),
)
book_hotel_tools = book_hotel_safe_tools + book_hotel_sensitive_tools

# Create the hotel booking assistant runnable
book_hotel_runnable = hotel_booking_prompt | llm.bind_tools(
    book_hotel_tools + [CompleteOrEscalate]
)

# Instantiate the hotel booking assistant
hotel_booking_assistant = Assistant(book_hotel_runnable)
