from decimal import Decimal

from ingestion.parsing import parse_depth_update




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

def test_parse_depth_with_empty_ask_side():
    message = {
        "e": "depthUpdate",
        "E": 1699999999999,
        "s": "BTCUSDT",
        "U": 157,
        "u": 160,
        "b": [["50000.00", "1.5"]],
        "a": [],
    }

    result = parse_depth_update(message)

    assert result.bids[0].price == Decimal("50000.00")
    assert result.asks == []

def test_parse_depth_keeps_zero_quantity_levels():
    message = {
        "e": "depthUpdate",
        "E": 1699999999999,
        "s": "ETHUSDT",
        "U": 200,
        "u": 205,
        "b": [["2500.00", "0.00000000"]],
        "a": [["2501.00", "3.0"]],
    }
    result = parse_depth_update(message)

    assert result.bids[0].qty == Decimal("0")