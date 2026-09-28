# 02 – WebSocket to Kafka

Ingestor connects to Binance depth stream, validates each message,
and produces the raw original to `orderbook.raw`, keyed by symbol.

## Run
1. Start Kafka: `kafka-server-start /opt/homebrew/etc/kafka/server.properties`
2. Run ingestor: `uv run python src/ingestion/ws_client.py`
3. Verify: `rpk topic consume orderbook.raw -X brokers=localhost:9092`

## Observed
- ~1 message/sec per symbol; each message is large (tens of levels/side)
- Most quantities are 0.00000000 → "remove level" signals
- BTCUSDT consistently lands in the same partition (key = symbol)