import asyncio
import json

import websockets
from aiokafka import AIOKafkaProducer

from ingestion.parsing import validate_depth_message
from ingestion.errors import MalformedDepthMessage

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth"
KAFKA_BOOTSTRAP = "localhost:9092"
RAW_TOPIC = "orderbook.raw"

async def stream_depth() -> None:
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    await producer.start()
    try:
        async with websockets.connect(BINANCE_WS_URL) as ws:
            async for message in ws:
                try:
                    data = json.loads(message)
                    validate_depth_message(data)
                except MalformedDepthMessage as exc:
                    print(f"skipping malformed message: {exc}")
                    continue

                key = data["s"].encode()
                value = message.encode()
                await producer.send_and_wait(RAW_TOPIC, key=key, value=value)
                print(f"produced {data['s']} update to {RAW_TOPIC}")
    finally:
        await producer.stop()


if __name__ == "__main__":
    try:
        asyncio.run(stream_depth())
    except KeyboardInterrupt:
        print("\nstopped")