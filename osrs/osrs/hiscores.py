# support modes: hiscore_oldschool_hardcore_ironman, hiscore_oldschool_ultimate, hiscore_oldschool_deadman, hiscore_oldschool_seasonal, hiscore_oldschool_tournament, hiscore_oldschool_fresh_start
# support lite: https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=X
# support json: https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player=X
from enum import Enum, auto


class Mode(Enum):
    hiscore_oldschool_hardcore_ironman = auto()
    hiscore_oldschool_ultimate = auto()
    hiscore_oldschool_deadman = auto()
    hiscore_oldschool_seasonal = auto()
    hiscore_oldschool_tournament = auto()
    hiscore_oldschool_fresh_start = auto()


class HiScore:
    def __init__(self) -> None:
        self.BASE_URL = "https://secure.runescape.com"

    def get_ranking(self, mode:Mode, table:int=0, category:int=0, size:int=10):
        url = f"{self.BASE_URL}/m={mode.name}/ranking.json"
        params = {
            "table": table,
            "category": category,
            "size": size
        }
        print(url, params)

    def get_score_json(self, mode:Mode, player:str):
        url = f"{self.BASE_URL}/m={mode.name}/index_lite.json"
        param = {"player":player}
    
    def get_score_ws(self, mode:Mode, player:str):
        url = f"{self.BASE_URL}/m={mode.name}/index_lite.ws"
        param = {"player":player}
    