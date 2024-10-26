# The project
The goal is to make a wrapper around the various oldschool runescape api's.

# osrs hiscores
```py
import asyncio

from aiohttp import ClientSession

from osrs.async_api.osrs.hiscores import Mode, PlayerStats, Hiscore, RateLimiter
from osrs.exceptions import PlayerDoesNotExist


async def main():
    # 100 calls per minute
    limiter = RateLimiter(calls_per_interval=100, interval=60)
    hiscore_instance = Hiscore(proxy="", rate_limiter=limiter)
    
    async with ClientSession() as session:
        player_stats = await hiscore_instance.get(
            mode=Mode.OLDSCHOOL,
            player="extreme4all",
            session=session,
        )
        print(player_stats)


loop = asyncio.get_running_loop()
await loop.create_task(main())
```