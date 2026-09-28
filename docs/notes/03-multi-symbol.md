# 03 – Multi-symbol ingestion with reconnect

Combined WebSocket for N symbols (btcusdt, ethusdt, bnbusdt, solusdt, xrpusdt).
Auto-reconnect with exponential backoff (backoff_delay, capped at 60s, reset on connect).

## Important
- Messages in `orderbook.raw` are stored WITH the multi-stream envelope:
  `{"stream": "...@depth", "data": {...}}`. The consumer must unwrap `data`
  before parsing.
- Different symbols land in different partitions (key = symbol). Verified:
  BTC→p2, ETH→p5, BNB→p3.