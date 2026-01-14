# Runtime Agent Definitions

This directory contains runtime configuration for the application's LangGraph
assistants.

The graph topology remains in Python under `customer_support_chat/app/graph.py`,
but assistant prompts, tool lists, and sensitive interrupt node declarations are
loaded from these YAML files.

## Files

- `primary.yaml`: triage, policy lookup, flight search, and delegation.
- `flight_booking.yaml`: flight search, updates, and cancellation.
- `hotel_booking.yaml`: hotel search, booking, updates, and cancellation.
- `car_rental.yaml`: car rental search, booking, updates, and cancellation.
- `excursion.yaml`: trip recommendation search, booking, updates, and
  cancellation.

## Runtime Boundaries

- Tool names must exist in the importing assistant module's tool registry.
- Sensitive tools must also appear in `requires_confirmation`.
- Sensitive graph nodes must be listed in `interrupt_before`.
- Changes to prompts or tool lists should be covered by routing and tool-use
  evals.
