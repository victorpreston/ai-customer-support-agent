# Repository Agents

These files describe development-time agents for maintaining this LangGraph
customer support system. They are not loaded by the application at runtime.

Use them as focused instructions for future reviews, Codex sessions, or
automation around this repository.

## Agents

- `langgraph-architect.md`: reviews graph structure, routing, state, and
  assistant boundaries.
- `eval-writer.md`: creates regression evals for routing, tool use, and RAG
  groundedness.
- `tool-safety-reviewer.md`: reviews sensitive tools, confirmation flows, and
  idempotency.
- `readme-reviewer.md`: validates README accuracy against the current repo.

## Runtime Agent Configs

The production assistants currently live in:

- `customer_support_chat/app/services/assistants/primary_assistant.py`
- `customer_support_chat/app/services/assistants/flight_booking_assistant.py`
- `customer_support_chat/app/services/assistants/car_rental_assistant.py`
- `customer_support_chat/app/services/assistants/hotel_booking_assistant.py`
- `customer_support_chat/app/services/assistants/excursion_assistant.py`

If the project later needs declarative runtime agent definitions, prefer adding
versioned config files under `customer_support_chat/app/agents/` and loading
them from the Python graph code.
