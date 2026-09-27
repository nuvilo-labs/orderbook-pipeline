# 2. Partition key is the trading symbol

Date: 2026-09-27
Status: accepted

## Context

Each message produced to Kafka carries a key, and the key determines which
partition the message lands in. Kafka only guarantees ordering *within* a
partition, not across partitions.

Depth updates from Binance are incremental: the order book for a symbol is
rebuilt by applying a sequence of deltas in the exact order they arrived.
If updates for one symbol were spread across partitions, they could be
consumed out of order and corrupt the reconstructed book.

## Decision

Use the trading symbol (e.g. `BTCUSDT`) as the partition key.

- `partition_key(update)` returns `update.symbol` as a `str`.
- All updates for one symbol therefore share a key, land in the same
  partition, and are consumed in order.
- Updates for different symbols get different keys and may land in
  different partitions, which allows them to be processed in parallel.

The function returns `str`, not `bytes`. Encoding to bytes is Kafka's
concern and lives in the producer (the infrastructure layer), not in the
domain. `partition_key` does not know Kafka exists.

## Consequences

- Per-symbol ordering is preserved, which is what order book
  reconstruction requires.
- Two different symbols may hash to the same partition; this is harmless.
  Consumers separate messages by key, and per-symbol order still holds.
- Partition count is chosen for parallelism (max N consumers in parallel),
  not to isolate symbols — collisions between symbols do not affect
  correctness.
- Tests assert the key equals the symbol and is deterministic, not which
  numbered partition it maps to (that is Kafka's `hash(key) % n` and would
  make the test brittle).