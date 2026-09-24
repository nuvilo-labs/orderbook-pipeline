from dataclasses import dataclass
from decimal import Decimal
from typing import NamedTuple

class PriceLevel(NamedTuple):
    price: Decimal
    qty: Decimal

@dataclass(frozen=True)
class DepthUpdate:
    symbol: str
    event_time: int
    first_update_id: int
    final_update_id: int
    bids: list[PriceLevel]
    asks: list[PriceLevel]

def parse_depth_update(message: dict) -> DepthUpdate:
    return DepthUpdate(
        symbol=message["s"],
        event_time=message["E"],
        first_update_id=message["U"],
        final_update_id=message["u"],
        bids=[PriceLevel(Decimal(p), Decimal(q)) for p, q in message["b"]],
        asks=[PriceLevel(Decimal(p), Decimal(q)) for p, q in message["a"]],
    )