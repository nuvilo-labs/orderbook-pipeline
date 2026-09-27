from decimal import Decimal

from ingestion.models import DepthUpdate, PriceLevel
from ingestion.partitioning import partition_key


def make_update(symbol: str) -> DepthUpdate:
    return DepthUpdate(
        symbol=symbol,
        event_time=1699999999999,
        first_update_id=1,
        final_update_id=2,
        bids=[PriceLevel(price=Decimal("50000.00"), qty=Decimal("1.0"))],
        asks=[],
    )


def test_key_is_the_symbol():
    update = make_update("BTCUSDT")

    assert partition_key(update) == "BTCUSDT"


def test_same_symbol_gives_same_key():
    key_a = partition_key(make_update("ETHUSDT"))
    key_b = partition_key(make_update("ETHUSDT"))

    assert key_a == key_b


def test_different_symbols_give_different_keys():
    btc = partition_key(make_update("BTCUSDT"))
    eth = partition_key(make_update("ETHUSDT"))

    assert btc != eth