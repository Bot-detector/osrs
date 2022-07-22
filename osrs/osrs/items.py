import asyncio
import logging
import time
from collections import deque

import aiohttp
from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class itemScraper:
    base_url = "https://secure.runescape.com/m=itemdb_oldschool"  # /api'

    def __init__(
        self,
        proxy: str = "",
        calls_per_minute: int = 60,
        session: ClientSession = ClientSession(),
    ) -> None:
        self.proxy = proxy
        self.history = deque(maxlen=calls_per_minute)
        self.session = session

    async def __rate_limit(self):
        """
        Rate limits the scraper to 60 calls a minute.
        """
        self.history.append(int(time.time()))
        maxlen = self.history.maxlen
        if len(self.history) == maxlen:
            head = self.history[0]
            tail = self.history[-1]
            span = tail - head
            if span < 60:
                sleep = 60 - span
                logger.debug(f"Rate limit reached, sleeping {sleep} seconds")
                await asyncio.sleep(sleep)
        return

    async def __webrequest(self, url) -> dict:
        await self.__rate_limit()
        async with self.session.get(url) as response:
            if response.ok:
                data = await response.json(content_type=None)
            else:
                try:
                    body = await response.text()
                except:
                    body = ""
                error = {
                    "url": url,
                    "status_code": response.status,
                    "headers": response.headers,
                    "body": body,
                }
                logger.error(error)
        return data

    async def images(self, item_id: int) -> list:
        icon = self.base_url + f"/obj_sprite.gif?id={item_id}"
        icon_large = self.base_url + f"/obj_big.gif?id={item_id}"
        return icon, icon_large

    async def category(self, category: int = 1) -> dict:
        url = self.base_url + "/api" + f"/catalogue/category.json?category={category}"
        return await self.__webrequest(url)

    async def items(self, letter: str, page: int = 0) -> dict:
        url = (
            self.base_url
            + "/api"
            + f"/catalogue/items.json?category=1&alpha={letter}&page={page}"
        )
        return await self.__webrequest(url)

    async def itemDetail(self, item_id: int) -> dict:
        url = self.base_url + "/api" + f"/catalogue/detail.json?item={item_id}"
        return await self.__webrequest(url)

    async def timeseries(self, item_id: int) -> dict:
        url = self.base_url + "/api" + f"/graph/{item_id}.json"
        data = await self.__webrequest(url)

        # converting data in a more verbose way
        daily = [
            {"timestamp": key, "price": value} for key, value in data["daily"].items()
        ]
        average = [
            {"timestamp": key, "price": value} for key, value in data["average"].items()
        ]

        # recreate dictionary
        data = {}
        data["daily"] = daily
        data["average"] = average
        return data
