import logging
from src import runelitePrices, runeliteSettings as rlSettings
from dataclasses import dataclass

logger = logging.getLogger("__name__")

user_agent = rlSettings.userAgent(
    discord="testDiscord", purpose="Testing: https://github.com/Bot-detector/osrs"
)
api = runelitePrices(
    user_agent=user_agent,
    endpoint=rlSettings.runeliteEndpoint.OSRS
)

@dataclass
class testLatest():
    id: int

@dataclass
class testTimeSeries():
    id: int
    timestep: rlSettings.timestep

@dataclass
class testAvgPrice():
    timestep: rlSettings.timestep = rlSettings.timestep.FIVE_MINUTES
    unix_time: int = None

def test_get_latest():
    """
    Tests the get_latest() function.
    """
    config = [testLatest(id=2)]
    logger.info("Test get_latest() function")
    for item in config:
        data = api.get_latest(item.id)

        logger.info(data)
        error = f"Expected dict, but received {type(data)} instead"
        assert isinstance(data, dict), error


def test_time_series():
    """
    Tests the get_time_series() function.
    """
    timestep = rlSettings.timestep.ONE_HOUR
    config = [testTimeSeries(id=2, timestep=timestep.ONE_HOUR)]
    for item in config:
        data = api.get_time_series(id=item.id, timestep=item.timestep)

        logger.info(data)
        error = f"Expected dict, but received {type(data)} instead"
        assert isinstance(data, dict), error

def test_time_avg_price():
    """
    Tests the get_avg_price() function.
    """
    config = [testAvgPrice(timestep=rlSettings.timestep.FIVE_MINUTES)]
    for item in config:
        data = api.get_avg_price(unix_time=item.unix_time, timestep=item.timestep)

        logger.info(data)
        error = f"Expected dict, but received {type(data)} instead"
        assert isinstance(data, dict), error