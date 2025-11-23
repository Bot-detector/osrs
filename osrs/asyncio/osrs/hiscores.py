import logging
import time
from enum import Enum

from aiohttp import ClientSession
from pydantic import BaseModel

from osrs.exceptions import PlayerDoesNotExist, Undefined, UnexpectedRedirection
from osrs.utils import RateLimiter

logger = logging.getLogger(__name__)


class Mode(str, Enum):
    OLDSCHOOL = "hiscore_oldschool"
    IRONMAN = "hiscore_oldschool_ironman"
    HARDCORE = "hiscore_oldschool_hardcore_ironman"
    ULTIMATE = "hiscore_oldschool_ultimate"
    DEADMAN = "hiscore_oldschool_deadman"
    SEASONAL = "hiscore_oldschool_seasonal"
    TOURNAMENT = "hiscore_oldschool_tournament"


class Skill(BaseModel):
    id: int
    name: str
    rank: int
    level: int
    xp: int


class Activity(BaseModel):
    id: int
    name: str
    rank: int
    score: int


class PlayerStats(BaseModel):
    skills: list[Skill]
    activities: list[Activity]


class HighscoreRank(BaseModel):
    name: str
    score: int
    rank: int


class Hiscore:
    BASE_URL = "https://secure.runescape.com"

    def __init__(
        self, proxy: str = "", rate_limiter: RateLimiter = RateLimiter()
    ) -> None:
        self.proxy = proxy
        self.rate_limiter = rate_limiter

    async def get(
        self,
        player: str,
        mode: Mode = Mode.OLDSCHOOL,
        session: ClientSession | None = None,
        return_latency: bool = False,
    ) -> PlayerStats | tuple[PlayerStats, float]:
        """
        Fetches player stats from the OSRS hiscores API.

        Args:
            mode (Mode): The hiscore mode.
            player (str): The player's username.
            session (ClientSession): The HTTP session.

        Returns:
            PlayerStats: Parsed player statistics.

        Raises:
            UnexpectedRedirection: If a redirection occurs.
            PlayerDoesNotExist: If the player is not found (404 error).
            ClientResponseError: For other HTTP errors.
            Undefined: For anything else that is not a 200
        """
        await self.rate_limiter.check()

        start_time = time.perf_counter()

        logger.debug(f"Performing hiscores lookup on {player}")
        url = f"{self.BASE_URL}/m={mode.value}/index_lite.json"
        params = {"player": player}

        _session = ClientSession() if session is None else session

        async with _session.get(url, proxy=self.proxy, params=params) as response:
            # when the HS are down it will redirect to the main page.
            # after redirction it will return a 200, so we must check for redirection first
            if response.history and any(r.status == 302 for r in response.history):
                error_msg = (
                    f"Redirection occured: {response.url} - {response.history[0].url}"
                )
                raise UnexpectedRedirection(error_msg)
            elif response.status == 404:
                raise PlayerDoesNotExist(f"player: {player} does not exist.")
            elif response.status != 200:
                # raises ClientResponseError
                response.raise_for_status()
                raise Undefined()
            data = await response.json()

        if session is None:
            await _session.close()

        if return_latency:
            total_time = time.perf_counter() - start_time
            return PlayerStats(**data), total_time

        return PlayerStats(**data)

    async def get_rank(
        self,
        mode: Mode,
        table: int,
        category: int,
        top_rank: int,
        size: int,
        session: ClientSession | None = None,
    ) -> list[HighscoreRank]:
        logger.debug("Performing hiscores lookup on ")
        url = f"{self.BASE_URL}/m={mode.value}/ranking.json"
        params = {
            "table": table,
            "category": category,
            "toprank": top_rank,
            "size": size,
        }

        _session = ClientSession() if session is None else session

        async with _session.get(url, proxy=self.proxy, params=params) as response:
            if response.history and any(r.status == 302 for r in response.history):
                error_msg = (
                    f"Redirection occured: {response.url} - {response.history[0].url}"
                )
                raise UnexpectedRedirection(error_msg)
            elif response.status != 200:
                response.raise_for_status()
                raise Undefined()
            data = await response.json()
        if session is None:
            await _session.close()
        return [
            HighscoreRank(
                name=d["name"],
                score=int(d["score"].replace(",", "")),
                rank=int(d["rank"].replace(",", "")),
            )
            for d in data
        ]
