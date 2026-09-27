# 1. Depth message validation and parsing

Date: 2026-09-27
Status: accepted

## Context

The ingestor receives depth-update messages from Binance over WebSocket.
These are external, untrusted input: fields may be missing, types may be
wrong, and numeric values may be malformed or out of range. The rest of
the pipeline (order book state, imbalance) depends on this data being
well-formed, so bad messages must be rejected at the boundary rather than
crashing a consumer three layers deep.

Two separate concerns exist: checking a message is well-formed
(validation) and turning it into an internal model (parsing). A design
question is where the numeric-content checks (a price is a valid number,
quantity is not negative) should live, since checking that a string
converts to Decimal means attempting the conversion — which parsing
already does.

## Decision

- Keep `validate_depth_message` and `parse_depth_update` as separate
  functions, exposed through a facade `parse_depth_message` that validates
  then parses. The facade is the only entry point callers use, so it is
  impossible to parse without validating.
- Split the checks to avoid duplicated work (option 2):
  - `validate_depth_message` checks structure: required fields present,
    `e == "depthUpdate"`, `b`/`a` are lists, each level is a `[price, qty]`
    pair of exactly two elements.
  - `parse_depth_update` does the numeric conversion once, and rejects
    non-numeric values, `price <= 0`, and `qty < 0` by raising
    `MalformedDepthMessage`.
- Business rules: price strictly > 0, quantity >= 0 (zero quantity is
  valid — it means "remove this level").
- Decimal, never float, for all prices and quantities.
- Field-type checks on `E`/`U`/`u` (must be ints) are deferred; not needed
  yet.

## Consequences

- No value is converted twice; the same numeric conversion is not repeated
  between validation and parsing.
- Validation is split across two functions rather than all in one. This is
  accepted because the facade guarantees the invariant: callers get either
  a valid `DepthUpdate` or a `MalformedDepthMessage`, never a raw
  `InvalidOperation` or `KeyError`.
- Malformed messages fail with a clear reason, which sets up the dead
  letter queue in the failure-handling phase.