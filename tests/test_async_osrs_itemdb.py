import pytest
from aiohttp import ClientSession

from osrs.async_api.osrs.itemdb import (
    Catalogue,
    Detail,
    Graph,
    Items,
    Mode,
    TradeHistory,
)


@pytest.mark.asyncio
async def test_get_items_valid():
    """Test fetching items with valid parameters"""
    catalogue_instance = Catalogue()
    async with ClientSession() as session:
        items = await catalogue_instance.get_items(
            session=session,
            alpha="a",  # Assume items starting with "A" exist
            page=1,
            mode=Mode.OLDSCHOOL,
            category=1,
        )

        # Assertions to confirm the response is correct
        assert isinstance(items, Items), "The returned object is not of type Items"
        assert items.items, "Items list should not be empty"
        assert items.total > 0, "Total count should be greater than zero"


@pytest.mark.asyncio
async def test_get_items_invalid_page():
    """Test fetching items with an invalid page number"""
    catalogue_instance = Catalogue()
    async with ClientSession() as session:
        items = await catalogue_instance.get_items(
            session=session,
            alpha="A",
            page=9999,  # Assume this page does not exist
            mode=Mode.OLDSCHOOL,
            category=1,
        )

        # Assertions for an empty result or similar handling
        assert isinstance(items, Items), "The returned object is not of type Items"
        assert not items.items, "Items list should be empty for a non-existing page"


@pytest.mark.asyncio
async def test_get_detail_valid():
    """Test fetching details for a valid item ID"""
    catalogue_instance = Catalogue()
    async with ClientSession() as session:
        item_id = 4151  # Assume this is a valid item ID
        item_detail = await catalogue_instance.get_detail(
            session=session, item_id=item_id, mode=Mode.OLDSCHOOL
        )

        # Assertions to confirm the response is correct
        assert isinstance(
            item_detail, Detail
        ), "The returned object is not of type Detail"
        assert item_detail.item.name == "Abyssal whip", "Unexpected item name returned"


@pytest.mark.asyncio
async def test_get_detail_invalid():
    """Test fetching details for an invalid item ID"""
    catalogue_instance = Catalogue()
    async with ClientSession() as session:
        invalid_item_id = 9999999  # Assume this item ID does not exist
        with pytest.raises(
            Exception
        ):  # Replace Exception with a specific exception if defined
            await catalogue_instance.get_detail(
                session=session, item_id=invalid_item_id, mode=Mode.OLDSCHOOL
            )


@pytest.mark.asyncio
async def test_get_graph_valid():
    """Test fetching trade history for a valid item ID"""
    catalogue_instance = Graph()
    async with ClientSession() as session:
        item_id = 4151  # Assume this is a valid item ID
        trade_history = await catalogue_instance.get_graph(
            session=session, item_id=item_id, mode=Mode.OLDSCHOOL
        )

        # Assertions to confirm the response is correct
        assert isinstance(
            trade_history, TradeHistory
        ), "The returned object is not of type TradeHistory"
        assert trade_history.daily, "Daily trade history should not be empty"
        assert trade_history.average, "Average trade history should not be empty"


@pytest.mark.asyncio
async def test_get_graph_invalid():
    """Test fetching trade history for an invalid item ID"""
    catalogue_instance = Graph()
    async with ClientSession() as session:
        invalid_item_id = 9999999  # Assume this item ID does not exist
        with pytest.raises(
            Exception
        ):  # Replace Exception with a specific exception if defined
            await catalogue_instance.get_graph(
                session=session, item_id=invalid_item_id, mode=Mode.OLDSCHOOL
            )
