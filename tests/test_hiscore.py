import pytest
from aiohttp import ClientSession

from osrs.hiscore import HiScore


@pytest.mark.asyncio
async def test_get_ranking_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        hiscore_instance = HiScore(session=session)
        data = await hiscore_instance.get_ranking(table=0, category=0, size=10)
        assert isinstance(data, list)
        assert isinstance(data[0], dict)


@pytest.mark.asyncio
async def test_get_hiscore(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        hiscore_instance = HiScore(session=session)
        data = await hiscore_instance.get_hiscore(player="extreme4all")
        assert isinstance(data, dict)
