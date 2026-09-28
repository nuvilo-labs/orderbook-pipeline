from ingestion.metrics import compute_rates


def test_messages_per_second():
    rates = compute_rates(messages=100, total_bytes=50_000, seconds=10)
    assert rates.messages_per_second == 10.0


def test_bytes_per_day_extrapolated():
    # 50_000 bytes in 10s -> 5_000 bytes/s -> 432_000_000 bytes/day
    rates = compute_rates(messages=100, total_bytes=50_000, seconds=10)
    assert rates.bytes_per_day == 432_000_000.0


def test_zero_seconds_is_safe():
    # avoid division by zero
    rates = compute_rates(messages=0, total_bytes=0, seconds=0)
    assert rates.messages_per_second == 0.0