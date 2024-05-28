import asyncio
import logging
import time
from collections import deque

logger = logging.getLogger(__name__)


class Ratelimiter:
    def __init__(self, calls_per_minute: int) -> None:
        self.history = deque(maxlen=calls_per_minute)

    async def call(self):
        """
        Rate limits the scraper to 60 calls a minute.
        """
        self.history.append(int(time.time()))
        maxlen = self.history.maxlen
        MINUTE = 60

        if not len(self.history) == maxlen:
            return

        head = self.history[0]  # first
        tail = self.history[-1]  # last
        span = tail - head

        if span > MINUTE:
            return

        sleep = MINUTE - span
        logger.warning(f"Rate limit reached, sleeping {sleep} seconds")
        await asyncio.sleep(sleep)
