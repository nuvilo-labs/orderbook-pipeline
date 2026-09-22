# 01 – Topics and partitions

## What I did
Created `orderbook.raw` with 6 partitions. Produced messages with and
without a key using `rpk topic produce`, consumed them with `-f '%p key=%k value=%v\n'`
to see which partition each landed in.

## What I observed
- With a key (e.g. BTCUSDT), all messages with the same key land in the
  same partition. Verified: two BTCUSDT messages → same partition.
- Partition is chosen by `hash(key) % num_partitions` — deterministic,
  not random.
- Without a key, messages are spread across partitions with no ordering
  guarantee.

## Why it matters for this project
- Key = trading symbol → all updates for one symbol stay in one partition,
  in order. Needed to rebuild each order book correctly.
- Two different keys can share a partition (hash collision); that's fine —
  the consumer separates them by key, and per-key order is still preserved.
- Partition count is about parallelism (max N consumers in parallel),
  not about isolating keys.