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
```py
import asyncio
from aiohttp import ClientSession
from osrs.catalogue import Catalogue, Mode  # Assuming this is the file/module name for your code

async def main():
    # Initialize the Catalogue with optional proxy and rate limiter
    catalogue = Catalogue(proxy="")

    async with ClientSession() as session:
        # Example 1: Fetching items by alphabetical filter
        alpha = "A"  # Items starting with "A"
        page = 1     # First page of results
        category = 1 # Category identifier, for OSRS there is only 1 category
        items = await catalogue.get_items(session, alpha=alpha, page=page, mode=Mode.OLDSCHOOL, category=category)
        print("Fetched Items:", items)

        # Example 2: Fetching detailed information for a specific item
        item_id = 4151  # Example item ID (Abyssal whip in OSRS)
        item_detail = await catalogue.get_detail(session, item_id=item_id, mode=Mode.OLDSCHOOL)
        print("Item Detail:", item_detail)

        # Example 3: Fetching historical trade data (price graph) for a specific item
        trade_history = await catalogue.get_graph(session, item_id=item_id, mode=Mode.OLDSCHOOL)
        print("Trade History:", trade_history)

# Run the asynchronous main function
asyncio.run(main())
``` 