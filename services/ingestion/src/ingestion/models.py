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