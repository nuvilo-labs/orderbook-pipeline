from ingestion.errors import MalformedDepthMessage
from ingestion.parsing import validate_depth_message
import pytest 
from decimal import Decimal


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

def test_valid_message_passes():
    # No exception means it's valid
    validate_depth_message(valid_message())

def test_missing_symbol_is_rejected():
    message = valid_message()
    del message["s"]

    with pytest.raises(MalformedDepthMessage):
        validate_depth_message(message)

def test_missing_bids_is_rejected():
    message = valid_message()
    del message["b"]

    with pytest.raises(MalformedDepthMessage):
        validate_depth_message(message)


def test_bids_must_be_a_list():
    message = valid_message()
    message["b"] = "not a list"

    with pytest.raises(MalformedDepthMessage):
        validate_depth_message(message)