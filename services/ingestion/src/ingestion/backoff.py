

def backoff_delay(attempt: int):
    return min( 1 * 2**(attempt - 1), 60)
