from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from customer_support_chat.app.services.tools import (
    search_trip_recommendations,
    book_excursion,
    update_excursion,
    cancel_excursion,
)
from customer_support_chat.app.agents import load_agent_config, resolve_tools
from customer_support_chat.app.services.assistants.assistant_base import Assistant, CompleteOrEscalate, llm

excursion_agent_config = load_agent_config("excursion")

# Excursion assistant prompt
excursion_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", excursion_agent_config.system_prompt),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

excursion_tool_registry = {
    "search_trip_recommendations": search_trip_recommendations,
    "book_excursion": book_excursion,
    "update_excursion": update_excursion,
    "cancel_excursion": cancel_excursion,
}

book_excursion_safe_tools = resolve_tools(
    excursion_agent_config,
    excursion_tool_registry,
    ("safe_tools",),
)
book_excursion_sensitive_tools = resolve_tools(
    excursion_agent_config,
    excursion_tool_registry,
    ("sensitive_tools",),
)
book_excursion_tools = book_excursion_safe_tools + book_excursion_sensitive_tools

# Create the excursion assistant runnable
book_excursion_runnable = excursion_prompt | llm.bind_tools(
    book_excursion_tools + [CompleteOrEscalate]
)

# Instantiate the excursion assistant
excursion_assistant = Assistant(book_excursion_runnable)
