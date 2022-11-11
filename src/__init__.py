# from bot_detector import xxx as xxx
# from osrs import xxx as xxx
# from runelite import xxx as xxx
from dataclasses import dataclass

from src.sync.runelite.runelite_prices import runelitePrices
from src.sync.runelite.utils import endpoints, timestep, user_agent
from src.utils.ratelimiter import RateLimiter


@dataclass
class runeliteSettings(object):
    userAgent = user_agent.userAgent
    timestep = timestep.timestep
    runeliteEndpoint = endpoints.Endpoint
