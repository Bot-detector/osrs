# https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices#Routes
# https://prices.runescape.wiki/api/v1/osrs/latest
import logging
from enum import Enum

from aiohttp import ClientSession, TCPConnector

from osrs.ratelimiter import Ratelimiter

logger = logging.getLogger()


class Endpoint(Enum):
    v1_osrs = "v1/osrs"
    v1_dmm = "v1/dmm"
    v1_fsw = "v1/fsw"


class Interval(Enum):
    FIVE_MINUTES = "5m"
    ONE_HOUR = "1h"
    SIX_HOURS = "6h"
    ONE_DAY = "24h"


class WikiPrices:
    def __init__(
        self,
        user_agent: str,
        proxy: str = "",
        session: ClientSession = None,
        ratelimiter: Ratelimiter = Ratelimiter(60),
    ) -> None:
        """
        Initialize the HiScore class.

        Parameters:
            proxy (str): The proxy to be used for HTTP requests.
            session (ClientSession): The aiohttp ClientSession to be used for making HTTP requests.
        """
        self.headers = {"User-Agent": user_agent}
        """
        USER AGENT
        BLOCKED BY THE WIKI TEAM
            python-requests
            Python-urllib
            Apache-HttpClient
            RestSharp
            Java/{version}

        An awesome example:
            "volume_tracker - @ThisIsMyUsername on Discord". 
        """
        self.BASE_URL = "https://prices.runescape.wiki/api"
        self.proxy = proxy
        self.session = session
        self.ratelimiter = ratelimiter

    async def _init(self) -> ClientSession:
        if self.session is None:
            connector = TCPConnector(limit=0)
            self.session = ClientSession(connector=connector)
        assert isinstance(self.session, ClientSession)

    def docs(self):
        docs = "https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices#Routes"
        print(docs)
        return docs

    def _round_time_to_interval(self, interval: Interval, timestamp: int):
        interval_seconds = {
            Interval.FIVE_MINUTES: 300,
            Interval.ONE_HOUR: 3600,
            Interval.SIX_HOURS: 21600,
            Interval.ONE_DAY: 86400,
        }[interval]
        rounded_time = timestamp - (timestamp % interval_seconds)
        return rounded_time

    async def mapping(self):
        await self._init()
        url = f"{self.BASE_URL}/v1/osrs/mapping"

        await self.ratelimiter.call()

        async with self.session.get(
            url,
            proxy=self.proxy,
            headers=self.headers,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

    async def latest(self, endpoint: Endpoint, id: int = None):
        await self._init()
        url = f"{self.BASE_URL}/{endpoint.value}/latest"
        params = {"id": id}
        params = {k: v for k, v in params.items() if v}

        async with self.session.get(
            url, proxy=self.proxy, headers=self.headers, params=params
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

    async def prices(
        self,
        interval: Interval,
        endpoint: Endpoint,
        timestamp: int = None,
    ):
        await self._init()
        url = f"{self.BASE_URL}/{endpoint.value}/{interval.value}"
        params = {
            "timestamp": self._round_time_to_interval(
                interval=interval,
                timestamp=timestamp,
            )
            if timestamp
            else None
        }
        params = {k: v for k, v in params.items() if v}

        async with self.session.get(
            url, proxy=self.proxy, headers=self.headers, params=params
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

    async def timeseries(self, interval: Interval, endpoint: Endpoint, id: int):
        await self._init()
        url = f"{self.BASE_URL}/{endpoint.value}/timeseries"
        params = {"id": id, "timestep": interval.value}
        params = {k: v for k, v in params.items() if v}

        async with self.session.get(
            url, proxy=self.proxy, headers=self.headers, params=params
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data
