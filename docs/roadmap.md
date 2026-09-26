# orderbook-pipeline — roadmap

Branch-by-branch plan. Local dev uses **Apache Kafka (KRaft)** on the Mac + `rpk`
(no Redpanda locally). Redpanda is the target for the 24/7 box in Phase 5.
Decisions live in `docs/decisions/` (ADRs). Tasks tracked in TickTick.

Branch naming: `feat/` feature · `chore/` maintenance · `docs/` writing · `fix/` fixes.
Rule: one branch = one closeable thing. Split if it grows mid-way.

---

## Phase 0 — Foundations ✅

- `ci/github-actions` — CI running pytest on every PR ✅
- Kafka setup + `orderbook.raw` topic via `rpk`, documented in `docs/local-setup.md` ✅

---

## Phase 1 — Ingestion service

- `feat/parse-depth` — parse a `depth` message into `DepthUpdate` (models, errors, validation) ✅
- `chore/cleanup-and-facade` — `.gitignore`, stop tracking `__pycache__`, `parse_depth_message` facade ✅
- `feat/harden-parser` — reject non-numeric price/qty, negative qty, malformed level,
  wrong type on `E`/`U`/`u`, `e == depthUpdate`. Closes A0.
- `feat/partition-key` — (TDD) decide + test the partition key (symbol → always same partition). Includes an ADR.
- `feat/ws-client` — asyncio WebSocket client for 1 symbol, printing to screen (no Kafka yet).
- `feat/ws-to-kafka` — WebSocket → producer → `orderbook.raw`; see messages with `rpk`.
- `feat/ws-reconnect` — automatic reconnect with backoff, scale to 5-10 symbols.
- `feat/ingestion-metrics` — measure + note messages/sec and bytes/day (to size the VPS with real data).
- `docs/blog-why` — post: "why this project exists".

---

## Phase 2 — Calculation service

- `feat/orderbook-state` — (TDD) maintain book state by applying deltas. **Core function — write by hand.**
- `feat/imbalance-calc` — (TDD) compute imbalance over the first N levels. **Core function — write by hand.**
- `feat/calc-consumer` — consume `orderbook.raw` → compute → produce to `orderbook.imbalance`.
- `feat/offset-commit-strategy` — commit before/after processing; document (ADR) + test.
- `feat/consumer-group-rebalance` — run 2 instances, observe rebalance with `rpk`.
- `docs/blog-partitions` — post: "partitions, consumer groups, and what happened with two instances".

---

## Phase 3 — Persistence & API

- `feat/api-service` — API service with its own database; consumer that persists imbalances.
- `feat/history-endpoint` — (TDD) FastAPI endpoint: history by symbol + time window.
- `feat/message-contracts` — versioned schema in `contracts/` (JSON Schema first; evaluate Pydantic v2 here).
- `feat/schema-evolution` — change message format without breaking the old consumer, and write it up.
- `feat/clickhouse-history` — (optional) ClickHouse for the history service, if still wanted.

---

## Phase 4 — Failure & operations (the real experience)

- `feat/broker-failure` — kill the broker while ingesting; what's lost, what isn't; fix it.
- `feat/consumer-idempotency` — kill the consumer mid-way; duplicates? make processing idempotent.
- `feat/dlq` — malformed messages → dead letter queue (where `MalformedDepthMessage` pays off).
- `feat/backpressure` — deliberately slow consumer; observe lag and decide what to do.
- `feat/retention-metrics` — time-based retention on topics; basic metrics (structured log or Prometheus).
- `docs/blog-failures` — post: "the failures I caused and what I changed".

---

## Phase 5 — Production

- `feat/vps-deploy` — Hetzner VPS + Redpanda (target for 24/7); deploy the three services.
- `feat/telegram-alerts` — alert channel when imbalance crosses a threshold; first real users.
- `docs/blog-architecture` — final post: full architecture, real numbers, incidents.

---
