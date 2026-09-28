from dataclasses import dataclass

SECONDS_PER_DAY = 86_400


@dataclass(frozen=True)
class Rates:
    messages_per_second: float
    bytes_per_second: float
    bytes_per_day: float


def compute_rates(messages: int, total_bytes: int, seconds: float) -> Rates:
    if seconds <= 0:
        return Rates(0.0, 0.0, 0.0)

    msg_per_sec = messages / seconds
    bytes_per_sec = total_bytes / seconds
    return Rates(
        messages_per_second=msg_per_sec,
        bytes_per_second=bytes_per_sec,
        bytes_per_day=bytes_per_sec * SECONDS_PER_DAY,
    )