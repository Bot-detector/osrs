import logging
from enum import Enum

from aiohttp import ClientSession
from pydantic import BaseModel

from osrs.exceptions import PlayerDoesNotExist, Undefined, UnexpectedRedirection
from osrs.utils import RateLimiter

logger = logging.getLogger(__name__)


class Mode(str, Enum):
    OLDSCHOOL: str = "hiscore_oldschool"
    IRONMAN: str = "hiscore_oldschool_ironman"
    HARDCORE: str = "hiscore_oldschool_hardcore_ironman"
    ULTIMATE: str = "hiscore_oldschool_ultimate"
    DEADMAN: str = "hiscore_oldschool_deadman"
    SEASONAL: str = "hiscore_oldschool_seasonal"
    TOURNAMENT: str = "hiscore_oldschool_tournament"


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


class Hiscore:
    BASE_URL = "https://secure.runescape.com"

    def __init__(
        self, proxy: str = "", rate_limiter: RateLimiter = RateLimiter()
    ) -> None:
        self.proxy = proxy
        self.rate_limiter = rate_limiter

    async def get(self, mode: Mode, player: str, session: ClientSession) -> PlayerStats:
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

        logger.info(f"Performing hiscores lookup on {player}")
        url = f"{self.BASE_URL}/m={mode.value}/index_lite.json"
        params = {"player": player}

        async with session.get(url, proxy=self.proxy, params=params) as response:
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
            return PlayerStats(**data)
