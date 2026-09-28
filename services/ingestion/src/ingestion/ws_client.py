import asyncio
import json
import time

import websockets
from aiokafka import AIOKafkaProducer

from ingestion.metrics import compute_rates
from ingestion.parsing import validate_depth_message
from ingestion.errors import MalformedDepthMessage
from ingestion.backoff import backoff_delay


REPORT_INTERVAL = 10  # seconds
SYMBOLS = ["btcusdt", "ethusdt", "bnbusdt", "solusdt", "xrpusdt"]
KAFKA_BOOTSTRAP = "localhost:9092"
RAW_TOPIC = "orderbook.raw"


def build_stream_url(symbols: list[str]) -> str:
    streams = "/".join(f"{s}@depth" for s in symbols)
    return f"wss://stream.binance.com:9443/stream?streams={streams}"

async def stream_depth() -> None:
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    await producer.start()
    url = build_stream_url(SYMBOLS)
    attempt = 0

    message_count = 0
    byte_count = 0
    last_report = time.monotonic()
    
    try:
        while True:
            try:
                async with websockets.connect(url) as ws:
                    attempt = 0  # connected OK, reset backoff
                    async for raw in ws:
                        envelope = json.loads(raw)
                        data = envelope["data"]
                        try:
                            validate_depth_message(data)
                        except MalformedDepthMessage as exc:
                            print(f"skipping malformed message: {exc}")
                            continue
                        key = data["s"].encode()
                        value = raw.encode() if isinstance(raw, str) else raw
                        await producer.send_and_wait(RAW_TOPIC, key=key, value=value)

                        # --- metrics ----
                        message_count += 1
                        byte_count += len(value)
                        now = time.monotonic()
                        elapsed = now - last_report
                        if elapsed >= REPORT_INTERVAL:
                            rates = compute_rates(message_count, byte_count, elapsed)
                            print(
                                f"{rates.messages_per_second:.1f} msg/s | "
                                f"{rates.bytes_per_second/1024:.1f} KB/s | "
                                f"{rates.bytes_per_day/1_000_000_000:.2f} GB/day"
                            )
                            message_count = 0
                            byte_count = 0
                            last_report = now
            except (websockets.ConnectionClosed, OSError) as exc:
                attempt += 1
                delay = backoff_delay(attempt)
                print(f"connection lost ({exc}); reconnecting in {delay}s")
                await asyncio.sleep(delay)
    finally:
        await producer.stop()


if __name__ == "__main__":
    try:
        asyncio.run(stream_depth())
    except KeyboardInterrupt:
        print("\nstopped")