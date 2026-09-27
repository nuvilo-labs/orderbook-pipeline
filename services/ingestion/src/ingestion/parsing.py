from decimal import Decimal

from ingestion.errors import MalformedDepthMessage
from ingestion.models import DepthUpdate, PriceLevel


def parse_depth_update(message: dict) -> DepthUpdate:
    return DepthUpdate(
        symbol=message["s"],
        event_time=message["E"],
        first_update_id=message["U"],
        final_update_id=message["u"],
        bids=[PriceLevel(Decimal(p), Decimal(q)) for p, q in message["b"]],
        asks=[PriceLevel(Decimal(p), Decimal(q)) for p, q in message["a"]],
    )

def validate_depth_message(message: dict) -> None:
    required_fields = ["s", "E", "U", "u", "b", "a"]
    for field in required_fields:
        if field not in message:
            raise MalformedDepthMessage(f"missing field '{field}'")

    if message["e"] != "depthUpdate":
        raise MalformedDepthMessage(f"unexpected event type: {message['e']!r}")

    for side in ("b", "a"):
        levels = message[side]
        if not isinstance(levels, list):
            raise MalformedDepthMessage(f"field '{side}' must be a list")
        for level in levels:
            if not isinstance(level, list) or len(level) != 2:
                raise MalformedDepthMessage(
                    f"level in '{side}' must be a [price, qty] pair, got {level!r}"
                )

def parse_depth_message(message: dict) -> DepthUpdate:
    validate_depth_message(message)
    return parse_depth_update(message)