import pytest
from aiohttp import ClientSession


@pytest.fixture
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()
