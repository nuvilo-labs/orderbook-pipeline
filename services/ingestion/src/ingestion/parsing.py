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

    if not isinstance(message["b"], list):
        raise MalformedDepthMessage("field 'b' must be a list")
    if not isinstance(message["a"], list):
            raise MalformedDepthMessage("field 'a' must be a list")