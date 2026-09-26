from decimal import Decimal

from ingestion.parsing import parse_depth_message
import pytest


from ingestion.errors import MalformedDepthMessage


def valid_message():
    return {
        "e": "depthUpdate",
        "E": 1699999999999,
        "s": "BTCUSDT",
        "U": 157,
        "u": 160,
        "b": [["50000.00", "1.5"]],
        "a": [["50010.00", "2.1"]],
    }


def test_parse_depth_message_returns_parsed_object_for_valid_input():
    result = parse_depth_message(valid_message())

    assert result.symbol == "BTCUSDT"
    assert result.bids[0].price == Decimal("50000.00")


def test_parse_depth_message_rejects_invalid_input():
    message = valid_message()
    del message["s"]

    with pytest.raises(MalformedDepthMessage):
        parse_depth_message(message)