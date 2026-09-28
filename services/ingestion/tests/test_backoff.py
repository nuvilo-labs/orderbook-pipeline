from ingestion.backoff import backoff_delay


def test_first_attempt_waits_base():
    assert backoff_delay(1) == 1.0


def test_delay_doubles_each_attempt():
    assert backoff_delay(2) == 2.0
    assert backoff_delay(3) == 4.0
    assert backoff_delay(4) == 8.0


def test_delay_is_capped():
    # 2^9 = 512, but the cap holds it at 60
    assert backoff_delay(10) == 60.0


def test_delay_never_exceeds_cap_for_large_attempts():
    assert backoff_delay(50) == 60.0