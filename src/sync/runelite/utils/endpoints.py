from enum import Enum

class Endpoint(Enum):
    OSRS: str = "https://prices.runescape.wiki/api/v1/osrs"
    DEADMAN: str = "https://prices.runescape.wiki/api/v1/dmm"
    FRESH_START_WORLDS: str = "https://prices.runescape.wiki/api/v1/fsw"