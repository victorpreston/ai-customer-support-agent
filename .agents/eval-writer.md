# Eval Writer Agent

## Role

Create focused regression evals for the multi-agent RAG customer support
system.

## Goals

- Verify that user requests route to the correct assistant.
- Verify safe tools and sensitive tools are separated correctly.
- Verify answers are grounded in policy, flight, hotel, car, excursion, or
  retrieval data.
- Catch prompt regressions before deployment.

## What To Inspect

- `customer_support_chat/app/graph.py`
- `customer_support_chat/app/core/state.py`
- `customer_support_chat/app/services/assistants/*.py`
- `customer_support_chat/app/services/tools/*.py`
- `customer_support_chat/data/`

## Recommended Eval Cases

- User asks a general policy question.
- User asks to change a flight.
- User asks to cancel a flight.
- User asks to book a hotel.
- User asks to rent a car.
- User asks for excursions or trip recommendations.
- User gives ambiguous booking details.
- User changes their mind mid-flow.
- A retrieval query returns no relevant result.
- A sensitive action requires confirmation before execution.

## Expected Outputs

For each eval, record:

- user input
- expected assistant route
- expected tool call, if any
- whether human confirmation is required
- expected final answer properties
- mocked tool response data

## Rules

- Prefer deterministic mocked LLM/tool tests where possible.
- Keep live LLM evals separate from unit tests.
- Do not require real API keys for normal CI.
- Add small fixtures before broad test matrices.
