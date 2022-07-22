# api = osrs.OsrsPrices(identification='extreme4all#6456')

# assert isinstance(api.items('a'), dict)
# assert isinstance(api.category(), dict)
# assert isinstance(api.timeseries(4151), dict)
# assert isinstance(api.itemDetail(4151), dict)
# # assert isinstance(api.images(4151), list)

from osrs import hiscoreScraper
import aiohttp
import pytest

@pytest.mark.asyncio
async def test_scraper():
    session = aiohttp.ClientSession()
    scraper = hiscoreScraper()
    result = await scraper.lookup_hiscores({"name": "extreme4all"}, session)
    assert isinstance(result, dict)