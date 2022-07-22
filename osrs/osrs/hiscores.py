import asyncio
import logging
import time
from collections import deque
from typing import Optional

import aiohttp

from osrs.utils.inputs import Inputs
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)

#TODO: use the modes
class modes(Enum):
    OLDSCHOOL: str = "hiscore_oldschool"
    IRONMAN: str = "hiscore_oldschool_ironman"
    HARDCORE: str = "hiscore_oldschool_hardcore_ironman"
    ULTIMATE: str = "hiscore_oldschool_ultimate"
    DEADMAN: str = "hiscore_oldschool_deadman"
    SEASONAL: str = "hiscore_oldschool_seasonal"
    TOURNAMENT: str = "hiscore_oldschool_tournament"

#TODO: complete the optional values
@dataclass
class player():
    id:Optional[int]
    name:str


class hiscoreScraper:
    def __init__(
        self, calls_per_minute: int = 60, proxy: str = ""
    ) -> None:
        self.proxy = proxy
        self.history = deque(maxlen=calls_per_minute)

    async def rate_limit(self):
        """
        Rate limits the scraper to defined (default=60) calls a minute.
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

    async def lookup_hiscores(
        self, player: dict, session: aiohttp.ClientSession
    ) -> dict:
        """
        Performs a hiscores lookup on the given player.

        :param player: a dictionary containing the player's name and id
        :return: a dictionary containing the player's hiscores.  if the player does not exist on hiscores, returns a dictionary of the player
        """
        await self.rate_limit()
        logger.debug(f"performing hiscores lookup on {player.get('name')}")
        url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={player.get('name')}"
        try:
            async with session.get(
                url, proxy=self.proxy
            ) as response:
                if response.status == 200:
                    hiscore = await response.text()
                    hiscore = await self.__parse_hiscores(hiscore)
                    hiscore["Player_id"] = player.get('id')
                    # logger.debug(f"{player.get('name')}, {hiscore}")
                    return hiscore
                elif response.status == 403:
                    logger.warning(f"403 bot challenge received proxy: {self.proxy}")
                    # If we hit the bot challenge page just give up for now..
                    await asyncio.sleep(1)
                elif response.status == 404:
                    logger.debug(f"{player.get('name')} does not exist on hiscores.")
                    return {"error": player}
                elif response.status == 502:
                    logger.warning("502 proxy error")
                    await asyncio.sleep(1)
                elif response.status in [500, 504, 520, 524]:
                    logger.warning(f"{response.status} returned from hiscore_oldschool")
                    await asyncio.sleep(1)
                else:
                    body = await response.text()
                    logger.error(
                        f"unhandled status code {response.status} from hiscore_oldschool.  header: {response.headers}  body: {body}"
                    )
                    await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"{e}, player: {player}")
            await asyncio.sleep(10)
            return None

    async def __parse_hiscores(self, hiscore: str) -> dict:
        """
        Parses the hiscores response into a dictionary.

        :param hiscore: the hiscores response
        :return: a dictionary containing the hiscores
        """
        # each row is seperated by a new line.
        # each value is seperated by a comma.
        # we only want the last value; the xp/kills
        hiscore = [row.split(",")[-1] for row in hiscore.split("\n")]

        # filter empty line (last line is empty)
        hiscore = list(filter(None, hiscore))

        # failsafe incase they update the hiscores
        expected_rows = len(Inputs.skills + Inputs.minigames + Inputs.bosses)
        if len(hiscore) != expected_rows:
            raise Exception(
                f"Unexpected hiscore size. Received: {len(hiscore)}, Expected: {expected_rows}"
            )

        hiscore: dict = dict(
            zip(Inputs.skills + Inputs.minigames + Inputs.bosses, hiscore)
        )
        # calculate the skills total as it might not be ranked
        hiscore["total"] = sum(
            [
                int(hiscore[skill])
                for skill in Inputs.skills[1:]
                if int(hiscore[skill]) != -1
            ]
        )

        # cast every value to integer
        hiscore = {k: int(v) for k, v in hiscore.items()}
        return hiscore

