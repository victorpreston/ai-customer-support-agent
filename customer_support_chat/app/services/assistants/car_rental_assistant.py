from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from customer_support_chat.app.services.tools import (
    search_car_rentals,
    book_car_rental,
    update_car_rental,
    cancel_car_rental,
)
from customer_support_chat.app.agents import load_agent_config, resolve_tools
from customer_support_chat.app.services.assistants.assistant_base import Assistant, CompleteOrEscalate, llm

car_rental_agent_config = load_agent_config("car_rental")

# Car rental assistant prompt
car_rental_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", car_rental_agent_config.system_prompt),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

car_rental_tool_registry = {
    "search_car_rentals": search_car_rentals,
    "book_car_rental": book_car_rental,
    "update_car_rental": update_car_rental,
    "cancel_car_rental": cancel_car_rental,
}

book_car_rental_safe_tools = resolve_tools(
    car_rental_agent_config,
    car_rental_tool_registry,
    ("safe_tools",),
)
book_car_rental_sensitive_tools = resolve_tools(
    car_rental_agent_config,
    car_rental_tool_registry,
    ("sensitive_tools",),
)
book_car_rental_tools = book_car_rental_safe_tools + book_car_rental_sensitive_tools

# Create the car rental assistant runnable
book_car_rental_runnable = car_rental_prompt | llm.bind_tools(
    book_car_rental_tools + [CompleteOrEscalate]
)

# Instantiate the car rental assistant
car_rental_assistant = Assistant(book_car_rental_runnable)
