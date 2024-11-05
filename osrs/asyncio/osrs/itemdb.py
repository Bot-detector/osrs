import json
import logging
from datetime import datetime
from enum import Enum
from typing import Union

from aiohttp import ClientSession
from pydantic import BaseModel, HttpUrl

from osrs.utils import RateLimiter

logger = logging.getLogger(__name__)


class Mode(str, Enum):
    OLDSCHOOL = "itemdb_oldschool"
    RS3 = "itemdb_rs"


class CurrentPrice(BaseModel):
    trend: str
    price: int | str  # Price can be an int or a formatted string (e.g., "15.5k")


class TodayPrice(BaseModel):
    trend: str
    price: int | str  # Price can also be an int or string (e.g., "+2")


class Item(BaseModel):
    icon: HttpUrl
    icon_large: HttpUrl
    id: int
    type: str
    typeIcon: HttpUrl
    name: str
    description: str
    current: CurrentPrice
    today: TodayPrice
    members: str | bool


class Items(BaseModel):
    total: int
    items: list[Item]


class PriceDetail(BaseModel):
    trend: str
    price: Union[int, str]  # Price can be int or formatted string (e.g., "+9")


class ChangeDetail(BaseModel):
    trend: str
    change: str  # Change is a percentage string (e.g., "+8.0%")


class ItemDetail(BaseModel):
    icon: HttpUrl
    icon_large: HttpUrl
    id: int
    type: str
    typeIcon: HttpUrl
    name: str
    description: str
    current: PriceDetail
    today: PriceDetail
    members: str  # Boolean-like strings ("true"/"false")
    day30: ChangeDetail
    day90: ChangeDetail
    day180: ChangeDetail


class Detail(BaseModel):
    item: ItemDetail


class TradeHistory(BaseModel):
    daily: dict[datetime, int]
    average: dict[datetime, int]


class Catalogue:
    BASE_URL = "https://secure.runescape.com"

    def __init__(
        self, proxy: str = "", rate_limiter: RateLimiter = RateLimiter()
    ) -> None:
        """Initialize the Catalogue with an optional proxy and rate limiter.

        Args:
            proxy (str): Proxy URL to use for API requests. Defaults to "".
            rate_limiter (RateLimiter): Rate limiter to manage request throttling.
                                        Defaults to a new RateLimiter instance.
        """
        self.proxy = proxy
        self.rate_limiter = rate_limiter

    async def get_items(
        self,
        alpha: str,
        page: int | None = 1,
        mode: Mode = Mode.OLDSCHOOL,
        session: ClientSession | None = None,
        category: int = 1,
    ) -> Items:
        """Fetch items from the RuneScape item catalog based on alphabetical filter.

        Args:
            session (ClientSession): An active aiohttp session for making requests.
            alpha (str): Alphabetical character to filter item names.
            page (int, optional): Page number to retrieve. Defaults to 1.
            mode (Mode, optional): Game mode (RS3 or OLDSCHOOL). Defaults to Mode.OLDSCHOOL.
            category (int, optional): Category identifier for items. Defaults to 1.

        Returns:
            Items: List of items matching the filter.
        """
        await self.rate_limiter.check()

        url = f"{self.BASE_URL}/m={mode.value}/api/catalogue/items.json"
        params = {"category": category, "alpha": alpha, "page": page}
        params = {k: v for k, v in params.items()}

        logger.debug(f"[GET]: {url=}, {params=}")

        _session = ClientSession() if session is None else session

        async with _session.get(url, proxy=self.proxy, params=params) as response:
            response.raise_for_status()
            data = await response.text()

        if session is None:
            await _session.close()

        return Items(**json.loads(data))

    async def get_detail(
        self,
        item_id: int,
        mode: Mode = Mode.OLDSCHOOL,
        session: ClientSession | None = None,
    ) -> Detail:
        """Fetch detailed information about a specific item.

        Args:
            session (ClientSession): An active aiohttp session for making requests.
            item_id (int): Unique identifier for the item.
            mode (Mode, optional): Game mode (RS3 or OLDSCHOOL). Defaults to Mode.OLDSCHOOL.

        Returns:
            Detail: Detailed information about the item.
        """
        await self.rate_limiter.check()

        url = f"{self.BASE_URL}/m={mode.value}/api/catalogue/detail.json"
        params = {"item": item_id}

        logger.debug(f"[GET]: {url=}, {params=}")

        _session = ClientSession() if session is None else session

        async with _session.get(url, proxy=self.proxy, params=params) as response:
            response.raise_for_status()
            data = await response.text()

        if session is None:
            await _session.close()
        return Detail(**json.loads(data))


class Graph:
    BASE_URL = "https://secure.runescape.com"

    def __init__(
        self,
        proxy: str = "",
        rate_limiter: RateLimiter = RateLimiter(),
    ) -> None:
        """Initialize the Catalogue with an optional proxy and rate limiter.

        Args:
            proxy (str): Proxy URL to use for API requests. Defaults to "".
            rate_limiter (RateLimiter): Rate limiter to manage request throttling.
                                        Defaults to a new RateLimiter instance.
        """
        self.proxy = proxy
        self.rate_limiter = rate_limiter

    async def get_graph(
        self,
        item_id: int,
        mode: Mode = Mode.OLDSCHOOL,
        session: ClientSession | None = None,
    ) -> TradeHistory:
        """Fetch trade history graph data for a specific item.

        Args:
            session (ClientSession): An active aiohttp session for making requests.
            item_id (int): Unique identifier for the item.
            mode (Mode, optional): Game mode (RS3 or OLDSCHOOL). Defaults to Mode.OLDSCHOOL.

        Returns:
            TradeHistory: Historical trading data for the item.
        """
        await self.rate_limiter.check()

        url = f"{self.BASE_URL}/m={mode.value}/api/graph/{item_id}.json"

        logger.debug(f"[GET]: {url=}")

        _session = ClientSession() if session is None else session

        async with _session.get(url, proxy=self.proxy) as response:
            response.raise_for_status()
            data = await response.text()

        if session is None:
            await _session.close()

        return TradeHistory(**json.loads(data))
