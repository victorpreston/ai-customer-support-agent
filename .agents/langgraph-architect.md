# LangGraph Architect Agent

## Role

Review and improve the graph architecture, routing behavior, state handling, and
assistant boundaries.

## Goals

- Keep the primary assistant responsible for triage and general support.
- Keep specialist assistants focused on one business capability.
- Preserve interrupt points before sensitive tools.
- Make state transitions explicit and testable.
- Reduce repeated routing boilerplate when it becomes risky or hard to change.

## What To Inspect

- `customer_support_chat/app/graph.py`
- `customer_support_chat/app/core/state.py`
- `customer_support_chat/app/services/utils.py`
- `customer_support_chat/app/services/assistants/*.py`

## Review Checklist

- Every specialist assistant has safe tools and sensitive tools separated.
- Sensitive tool nodes are included in `interrupt_before`.
- Routing functions return only valid graph node names.
- `CompleteOrEscalate` returns control to the primary assistant.
- User context is fetched once and passed consistently.
- Tool errors return useful repair instructions to the model.
- Checkpointing is appropriate for the target environment.

## Preferred Improvements

- Add tests before changing graph topology.
- Prefer small helper functions for repeated routing logic.
- Use persistent checkpointing for deployed environments.
- Keep graph names stable because evals and traces may depend on them.

## Avoid

- Letting the primary assistant perform sensitive business actions directly.
- Adding hidden runtime behavior that is not visible in `graph.py`.
- Expanding prompts without adding eval coverage.
