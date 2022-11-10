from src import RateLimiter
import time
import logging

logger = logging.getLogger(__name__)

def test_rate_limiter():
    """The test will run for 10 seconds and see how many requests were made."""
    N_CALLS = 5
    INTERVAL = 10 # in seconds
    # Create a rate limiter
    rate_limiter = RateLimiter(N_CALLS, INTERVAL)

    # Start the test
    start_time = time.time()
    count = 0
    while (time.time() - start_time) < INTERVAL:
        rate_limiter.call()
        count += 1
        logger.info(f"{count=}, time={time.time() - start_time}")
        print(f"{count=}, time={time.time() - start_time}")
    assert count <= N_CALLS, f"expected call count to be <= {N_CALLS}, but was {count}."
