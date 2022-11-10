import time
from collections import deque
import logging

logger = logging.getLogger("__name__")

class RateLimiter():
    def __init__(self, n_calls: int = 60, interval: int = 60):
        self.n_calls = n_calls
        self.interval = interval
        self.history = deque(maxlen=n_calls)

    def call(self) -> None:
        """The rate limiter function will wait if the number of calls per interval (in seconds) is exceeded"""
        self.history.append(int(time.time()))
        maxlen = self.history.maxlen
        if len(self.history) == maxlen:
            head = self.history[0]
            tail = self.history[-1]
            span = tail - head
            if span < self.interval:
                sleep = self.interval - span
                logger.debug(f"Rate limit reached, sleeping {sleep} seconds")
                time.sleep(sleep)
        return

    def reset(self):
        self.history = deque(maxlen=self.n_calls)