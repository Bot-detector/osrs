import pytest
from aiohttp import ClientSession

from osrs.async_api.wiki.prices import (
    AveragePrices,
    Interval,
    ItemMapping,
    LatestPrices,
    TimeSeries,
    WikiPrices,
)


@pytest.mark.asyncio
async def test_get_mapping_valid():
    """Test fetching item mappings successfully."""
    wiki_prices_instance = WikiPrices(
        user_agent="tests - https://github.com/Bot-detector/osrs"
    )
    async with ClientSession() as session:
        mappings = await wiki_prices_instance.get_mapping(session=session)

        assert isinstance(mappings, list), "Mappings should be a list"
        assert len(mappings) > 0, "Mappings list should not be empty"
        assert isinstance(
            mappings[0], ItemMapping
        ), "First mapping should be of type ItemMapping"


@pytest.mark.asyncio
async def test_get_latest_prices_valid():
    """Test fetching the latest prices successfully."""
    wiki_prices_instance = WikiPrices(
        user_agent="tests - https://github.com/Bot-detector/osrs"
    )
    async with ClientSession() as session:
        latest_prices = await wiki_prices_instance.get_latest_prices(session=session)

        assert isinstance(
            latest_prices, LatestPrices
        ), "The returned object is not of type LatestPrices"
        assert latest_prices.data, "Latest prices data should not be empty"


@pytest.mark.asyncio
async def test_get_average_prices_valid():
    """Test fetching average prices with valid parameters."""
    wiki_prices_instance = WikiPrices(
        user_agent="tests - https://github.com/Bot-detector/osrs"
    )
    async with ClientSession() as session:
        average_prices = await wiki_prices_instance.get_average_prices(
            session=session, interval=Interval.FIVE_MIN
        )

        assert isinstance(
            average_prices, AveragePrices
        ), "The returned object is not of type AveragePrices"
        assert average_prices.data, "Average prices data should not be empty"


@pytest.mark.asyncio
async def test_get_average_prices_invalid():
    """Test fetching average prices with an invalid interval."""
    wiki_prices_instance = WikiPrices(
        user_agent="tests - https://github.com/Bot-detector/osrs"
    )
    async with ClientSession() as session:
        with pytest.raises(Exception):
            await wiki_prices_instance.get_average_prices(
                session=session,
                interval="invalid_interval",
            )


@pytest.mark.asyncio
async def test_get_time_series_valid():
    """Test fetching time series data for a valid item ID and timestep."""
    wiki_prices_instance = WikiPrices(
        user_agent="tests - https://github.com/Bot-detector/osrs"
    )
    async with ClientSession() as session:
        item_id = 4151
        time_series = await wiki_prices_instance.get_time_series(
            session=session, item_id=item_id, timestep=Interval.ONE_HOUR
        )

        assert isinstance(
            time_series, TimeSeries
        ), "The returned object is not of type TimeSeries"
        assert len(time_series.data) > 0, "Time series data should not be empty"


@pytest.mark.asyncio
async def test_get_time_series_invalid():
    """Test fetching time series data for an invalid item ID."""
    wiki_prices_instance = WikiPrices(
        user_agent="tests - https://github.com/Bot-detector/osrs"
    )
    async with ClientSession() as session:
        invalid_item_id = 9999999

        time_series = await wiki_prices_instance.get_time_series(
            session=session, item_id=invalid_item_id, timestep=Interval.ONE_HOUR
        )
        assert isinstance(
            time_series, TimeSeries
        ), "The returned object is not of type TimeSeries"
        assert len(time_series.data) == 0, "Time series data should be empty"
