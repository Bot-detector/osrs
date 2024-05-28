import time

import pytest
from aiohttp import ClientSession

from osrs.wiki import Endpoint, Interval, WikiPrices


@pytest.mark.asyncio
async def test_get_mapping_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        client = WikiPrices(
            session=session,
            user_agent="pypi:osrs, test client, discord: 242987611226898433",
        )
        data = await client.mapping()
        assert isinstance(data, list)
        assert isinstance(data[0], dict)


@pytest.mark.asyncio
async def test_get_latest_id_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        client = WikiPrices(
            session=session,
            user_agent="pypi:osrs, test client, discord: 242987611226898433",
        )
        data = await client.latest(endpoint=Endpoint.v1_osrs, id=2)
        assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_get_latest_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        client = WikiPrices(
            session=session,
            user_agent="pypi:osrs, test client, discord: 242987611226898433",
        )
        data = await client.latest(endpoint=Endpoint.v1_osrs)
        assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_get_prices_nots_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        client = WikiPrices(
            session=session,
            user_agent="pypi:osrs, test client, discord: 242987611226898433",
        )
        data = await client.prices(
            endpoint=Endpoint.v1_osrs,
            interval=Interval.FIVE_MINUTES,
        )
        assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_get_prices_ts_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        client = WikiPrices(
            session=session,
            user_agent="pypi:osrs, test client, discord: 242987611226898433",
        )
        for interval in Interval:
            data = await client.prices(
                endpoint=Endpoint.v1_osrs,
                interval=interval,
                timestamp=int(time.time() - 60 * 60 * 7),
            )
            assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_get_timeseries_success(aiohttp_session: ClientSession):
    async for session in aiohttp_session:
        client = WikiPrices(
            session=session,
            user_agent="pypi:osrs, test client, discord: 242987611226898433",
        )
        data = await client.timeseries(
            endpoint=Endpoint.v1_osrs,
            interval=Interval.FIVE_MINUTES,
            id=2,
        )
        assert isinstance(data, dict)
