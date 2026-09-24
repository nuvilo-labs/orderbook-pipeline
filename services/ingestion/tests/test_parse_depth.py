from decimal import Decimal

from ingestion.parse_depth import parse_depth_update


def test_parse_message_depth():
    message = {
        "e": "depthUpdate",
        "E": 1699999999999,
        "s": "BTCUSDT",
        "U": 157,
        "u": 160,
        "b": [
            ["50000.00", "1.5"],
            ["49990.00", "0.0"],
        ],
        "a": [
            ["50010.00", "2.1"],
        ],
    }

    depth_update = parse_depth_update(message)

    assert depth_update.symbol == "BTCUSDT"
    assert depth_update.bids[0].price == Decimal("50000.00")
    assert depth_update.bids[0].qty == Decimal("1.5")
    assert depth_update.bids[1].qty == Decimal("0.0")
    assert depth_update.asks[0].price == Decimal("50010.00")