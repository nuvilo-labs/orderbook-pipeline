import asyncio

import websockets

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth"


async def stream_depth() -> None:
    async with websockets.connect(BINANCE_WS_URL) as ws:
        async for message in ws:
            print(message)


if __name__ == "__main__":
    asyncio.run(stream_depth())