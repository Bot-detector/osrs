import asyncio
from enum import Enum, auto

import aiohttp
from aiohttp import ClientSession, TCPConnector


class Mode(Enum):
    hiscore_oldschool = auto()
    hiscore_oldschool_hardcore_ironman = auto()
    hiscore_oldschool_ultimate = auto()
    hiscore_oldschool_deadman = auto()
    hiscore_oldschool_seasonal = auto()
    hiscore_oldschool_tournament = auto()
    hiscore_oldschool_fresh_start = auto()


class HiScore:
    def __init__(
        self,
        proxy: str = "",
    ) -> None:
        """
        Initialize the HiScore class.

        Parameters:
            proxy (str): The proxy to be used for HTTP requests.
            session (ClientSession): The aiohttp ClientSession to be used for making HTTP requests.
        """
        self.BASE_URL = "https://secure.runescape.com"
        self.proxy = proxy
        self.session = None

    async def init(self) -> ClientSession:
        connector = TCPConnector(limit=0)
        self.session = ClientSession(connector=connector)

    async def get_ranking(
        self,
        mode: Mode,
        table: int = 0,
        category: int = 0,
        size: int = 10,
    ) -> list[dict]:
        """
        Get the ranking for a specific game mode.

        Parameters:
            mode (Mode): The game mode for which the ranking is requested.
            table (int): The table index.
            category (int): The category index.
            size (int): The size of the ranking list.

        Returns:
            list[dict]: The ranking data in JSON format.

        Raises:
            aiohttp.ClientResponseError: If the HTTP request fails or returns a non-200 status code.
            aiohttp.ClientConnectionError: If a connection error occurs.
        """
        url = f"{self.BASE_URL}/m={mode.name}/ranking.json"
        params = {"table": table, "category": category, "size": size}

        if not self.session:
            await self.init()

        async with self.session.get(url, params=params, proxy=self.proxy) as response:
            response.raise_for_status()
            data = await response.json()
            return data

    async def get_hiscore(
        self,
        mode: Mode,
        player: str,
        json: bool = True,
    ) -> dict:
        """
        Get the hiscore data for a specific player and game mode.

        Parameters:
            mode (Mode): The game mode for which the hiscore data is requested.
            player (str): The player's username.
            json (bool): Whether to request the data in JSON format (default True).

        Returns:
            dict or str: The hiscore data in JSON format if json=True, otherwise as a string.

        Raises:
            aiohttp.ClientResponseError: If the HTTP request fails or returns a non-200 status code.
            aiohttp.ClientConnectionError: If a connection error occurs.
        """
        endpoint = "index_lite.json" if json else "index_lite.ws"
        url = f"{self.BASE_URL}/m={mode.name}/{endpoint}"
        params = {"player": player}

        if not self.session:
            await self.init()

        async with self.session.get(url, params=params, proxy=self.proxy) as response:
            response.raise_for_status()
            if json:
                data = await response.json()
            else:
                data = await response.text()
            return data


async def main():
    hiscore = HiScore()
    # existing player
    player_stats = await hiscore.get_hiscore(
        mode=Mode.hiscore_oldschool, player="extreme4all"
    )
    assert isinstance(player_stats, dict)

    # not existing player
    try:
        player_stats = await hiscore.get_hiscore(
            mode=Mode.hiscore_oldschool, player="aaa-bbb-ccc-ddd-eee-fff"
        )
    except aiohttp.ClientResponseError as e:
        assert e.status == 404
        assert e.message == "Not found"


if __name__ == "__main__":
    asyncio.run(main())
