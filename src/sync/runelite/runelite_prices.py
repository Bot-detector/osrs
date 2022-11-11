import requests

from src.sync.runelite.utils.endpoints import Endpoint
from src.sync.runelite.utils.timestep import timestep
from src.sync.runelite.utils.user_agent import userAgent
from src.utils.ratelimiter import RateLimiter


class runelitePrices:
    def __init__(
        self,
        user_agent: userAgent,
        n_calls: int = 60,
        interval: int = 60,
        endpoint: Endpoint = Endpoint.OSRS,
    ) -> None:
        self.rate_limiter = RateLimiter(n_calls, interval)
        self.user_agent = user_agent
        self.endpoint = endpoint
        pass

    def get_latest(
        self,
        id: int = None,
    ) -> dict:
        """
        Get the latest price for all available osrs
        """
        self.rate_limiter.call()

        url = f"{self.endpoint.value}/latest"
        params = dict(id=id) if id else {}

        response = requests.get(
            url=url,
            params=params,
            headers=self.user_agent.to_dict(),
        )
        response.raise_for_status()
        return response.json()

    def get_time_series(self, id: int, timestep: timestep = timestep.ONE_HOUR) -> dict:
        """Gives a list of the high and low prices of item with the given id at the given interval, up to 365 maximum."""
        self.rate_limiter.call()

        url = f"{self.endpoint.value}/timeseries"
        params = {
            "id": id,
            "timestep": timestep.value,
        }

        response = requests.get(
            url=url,
            params=params,
            headers=self.user_agent.to_dict(),
        )
        response.raise_for_status()
        return response.json()

    def get_avg_price(self, timestep: timestep, unix_time: int = None) -> dict:
        """Gives timestep average of item high and low prices as well as the number traded for the items that we have data on. Comes with a Unix timestamp indicating the timestep block the data is from"""
        self.rate_limiter.call()

        url = f"{self.endpoint.value}/{timestep.value}"
        params = {"timestamp": unix_time}
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(
            url=url,
            params=params,
            headers=self.user_agent.to_dict(),
        )
        response.raise_for_status()
        return response.json()
