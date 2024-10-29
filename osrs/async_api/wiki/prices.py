import logging
from enum import Enum

from aiohttp import ClientSession
from pydantic import BaseModel

from osrs.exceptions import Undefined
from osrs.utils import RateLimiter

logger = logging.getLogger(__name__)


class Interval(str, Enum):
    FIVE_MIN = "5m"
    ONE_HOUR = "1h"
    SIX_HOUR = "6h"
    DAY = "24h"


class ItemMapping(BaseModel):
    examine: str
    id: int
    members: bool
    lowalch: int | None = None
    limit: int | None = None
    value: int
    highalch: int | None = None
    icon: str
    name: str


class PriceData(BaseModel):
    high: int | None
    highTime: int | None
    low: int | None
    lowTime: int | None


class LatestPrices(BaseModel):
    data: dict[str, PriceData]


class AveragePriceData(BaseModel):
    avgHighPrice: int | None
    highPriceVolume: int | None
    avgLowPrice: int | None
    lowPriceVolume: int | None


class AveragePrices(BaseModel):
    data: dict[str, AveragePriceData]


class TimeSeriesData(BaseModel):
    timestamp: int
    avgHighPrice: int | None
    avgLowPrice: int | None
    highPriceVolume: int | None
    lowPriceVolume: int | None


class TimeSeries(BaseModel):
    data: list[TimeSeriesData]


class WikiPrices:
    BASE_URL = "https://prices.runescape.wiki/api/v1"

    def __init__(
        self,
        user_agent: str = None,
        proxy: str = "",
        rate_limiter: RateLimiter = RateLimiter(),
    ) -> None:
        """
        Initializes the WikiPrices client for accessing OSRS price data.

        Args:
            user_agent (str): User-Agent like 'price_tracker - @username on Discord'
            proxy (str): Optional proxy URL for requests.
            rate_limiter (RateLimiter): Rate limiter to control request frequency.
        """
        self.proxy = proxy
        self.rate_limiter = rate_limiter

        if user_agent:
            self.user_agent = user_agent
        else:
            inp = input("""
                User-Agent like 'price_tracker - @username on Discord'\n
                user_agent: 
            """)
            if not inp:
                raise Exception("invalid input")
            self.user_agent = inp

    async def fetch_data(self, session: ClientSession, url: str, params: dict = {}):
        """
        Utility method to fetch data from a specific endpoint, with ratelimiter,
        and basic error handling

        Args:
            session (ClientSession): The HTTP session for making the request.
            url (str): The URL endpoint to fetch data from.
            params (Optional[dict]): Query parameters for the request.

        Returns:
            dict: JSON-parsed data from the API response.
        """
        await self.rate_limiter.check()

        async with session.get(url, proxy=self.proxy, params=params) as response:
            if response.status == 400:
                error = await response.json()
                raise Exception(error)
            elif response.status != 200:
                response.raise_for_status()
                raise Undefined("Unexpected error.")
            return await response.json()

    async def get_mapping(self, session: ClientSession):
        """
        Fetches item mappings containing metadata.

        Args:
            session (ClientSession): The HTTP session for making the request.

        Returns:
            List[ItemMapping]: List of ItemMapping objects with metadata for each item.

        Example:
            >>> session = ClientSession()
            >>> wiki_prices = WikiPrices()
            >>> mappings = await wiki_prices.get_mapping(session)
            >>> print(mappings[0].name)  # e.g., '3rd age amulet'
        """
        url = f"{self.BASE_URL}/osrs/mapping"
        data = await self.fetch_data(session=session, url=url)
        return [ItemMapping(**item) for item in data]

    async def get_latest_prices(self, session: ClientSession) -> LatestPrices:
        """
        Fetches the latest prices for all items.

        Args:
            session (ClientSession): The HTTP session for making the request.

        Returns:
            LatestPrices: A dictionary of item IDs to PriceData.

        Example:
            >>> session = ClientSession()
            >>> wiki_prices = WikiPrices()
            >>> latest_prices = await wiki_prices.get_latest_prices(session)
            >>> print(latest_prices.data["2"].high)  # e.g., 240
        """
        url = f"{self.BASE_URL}/osrs/latest"
        data = await self.fetch_data(session=session, url=url)
        return LatestPrices(**data)

    async def get_average_prices(
        self,
        session: ClientSession,
        interval: Interval,
        timestamp: int | None = None,
    ) -> AveragePrices:
        """
        Fetches average prices at a specified interval (5-minute, 1-hour, etc.).

        Args:
            session (ClientSession): The HTTP session for the request.
            interval (Interval): The time interval ('5m', '1h', etc.) for averaging.
            timestamp (Optional[int]): Optional Unix timestamp to retrieve prices for a specific time.

        Returns:
            AveragePrices: A dictionary of item IDs to AveragePriceData.

        Example:
            >>> session = ClientSession()
            >>> wiki_prices = WikiPrices()
            >>> avg_prices = await wiki_prices.get_average_prices(session, Interval.ONE_HOUR)
            >>> print(avg_prices.data["2"].avgHighPrice)  # e.g., 235
        """
        url = f"{self.BASE_URL}/osrs/{interval.value}"
        params = {"timestamp": timestamp} if timestamp else {}
        data = await self.fetch_data(session=session, url=url, params=params)
        return AveragePrices(**data)

    async def get_time_series(
        self, session: ClientSession, item_id: int, timestep: Interval
    ) -> TimeSeries:
        """
        Fetches time-series data for a specific item and timestep.

        Args:
            session (ClientSession): The HTTP session for the request.
            item_id (int): The item ID.
            timestep (Interval): The timestep (e.g., '5m', '1h').

        Returns:
            TimeSeries: A list of TimeSeriesData entries for the specified item and timestep.

        Example:
            >>> session = ClientSession()
            >>> wiki_prices = WikiPrices()
            >>> time_series = await wiki_prices.get_time_series(session, 2, Interval.ONE_HOUR)
            >>> print(time_series.data[0].avgHighPrice)  # e.g., 1310000
        """
        url = f"{self.BASE_URL}/osrs/timeseries"
        params = {"id": item_id, "timestep": timestep.value}
        data = await self.fetch_data(session=session, url=url, params=params)
        return TimeSeries(**data)
