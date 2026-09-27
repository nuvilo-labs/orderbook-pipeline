# Orderbook Pipeline

Real-time crypto order book imbalance detection built on Kafka.
Ingests Binance depth streams, computes order imbalance in the first N
levels, and exposes it via a FastAPI history endpoint.


**Status:** active development (see Roadmap below)


## Why this project
Order book imbalance — when bid and ask pressure diverges in the first
price levels — is one of the strongest short-term signals in crypto
markets. Capturing it means ingesting thousands of depth updates per
second, computing state reliably, and keeping the history queryable.

This system ingests depth updates from Binance over WebSocket, streams
them through Kafka, computes imbalance in real time, and serves a
queryable history via FastAPI.

**Why Kafka here:** the volume is continuous and bursty (thousands of
depth updates/sec), ingestion and computation evolve at different speeds,
and every message may need to be replayed — exactly the properties Kafka
is for. A queue or a plain database would have worked for a demo; this
wouldn't survive requirements changing mid-project.


## Architecture
            ┌─────────────┐
            │   Binance   │
            │  WS (depth) │
            └──────┬──────┘
                   │ WebSocket
                   ▼
        ┌──────────────────────┐
        │     ingestor         │
        │  parse · validate    │
        │  produce             │
        └──────────┬───────────┘
                   │ orderbook.raw
                   ▼
             ┌───────────┐      ┌──────────────┐
             │   Kafka   │◄─────│   DLQ        │
             └─────┬─────┘      │ (malformed)  │
                   │            └──────────────┘
                   ▼
        ┌──────────────────────┐
        │     calculator       │
        │  order book state    │
        │  imbalance (N levels)│
        └──────────┬───────────┘
                   │ orderbook.imbalance
                   ▼
        ┌──────────────────────┐
        │     history-api      │
        │  persist · query     │
        │  FastAPI             │
        └──────────┬───────────┘
                   ▼
          ┌────────────────┐
          │  PostgreSQL /  │
          │  ClickHouse    │
          └────────────────┘

| Component    | What it does                                        | Stack                     |
|--------------|-----------------------------------------------------|---------------------------|
| ingestor     | Connects to Binance WS, parses and validates depth  | Python, asyncio, aiokafka |
|              | updates, produces to `orderbook.raw`                |                           |
| calculator   | Maintains order book state, computes imbalance      | Python, aiokafka          |
| history-api  | Persists imbalances, exposes history endpoints      | FastAPI, PostgreSQL       |


## Quickstart (local)

```bash
git clone https://github.com/nuvilo-labs/orderbook-pipeline
cd orderbook-pipeline

# Install (uv)
uv sync        

# Run the test suite
uv run pytest

# Kafka local setup (topics, etc.): see docs/local-setup.md
```

## Roadmap

- [x] CI with pytest on every PR
- [x] Depth message parsing with validation
- [x] Partitioning strategy (symbol as partition key)
- [ ] WebSocket ingestion from Binance
- [ ] Order book state from deltas
- [ ] Imbalance calculation (first N levels)
- [ ] History API (FastAPI, queryable by symbol and time window)
- [ ] Versioned message contracts
- [ ] Failure drills: broker down, consumer crash, DLQ, backpressure
- [ ] 24/7 deployment on VPS with alerts

