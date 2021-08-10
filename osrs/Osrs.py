import logging
import time

import requests

hiscore_dict = {
    "Overall": {"rank": 0, "level": 0, "exp": 0},
    "Attack": {"rank": 0, "level": 0, "exp": 0},
    "Defence": {"rank": 0, "level": 0, "exp": 0},
    "Strength": {"rank": 0, "level": 0, "exp": 0},
    "Hitpoints": {"rank": 0, "level": 0, "exp": 0},
    "Ranged": {"rank": 0, "level": 0, "exp": 0},
    "Prayer": {"rank": 0, "level": 0, "exp": 0},
    "Magic": {"rank": 0, "level": 0, "exp": 0},
    "Cooking": {"rank": 0, "level": 0, "exp": 0},
    "Woodcutting": {"rank": 0, "level": 0, "exp": 0},
    "Fletching": {"rank": 0, "level": 0, "exp": 0},
    "Fishing": {"rank": 0, "level": 0, "exp": 0},
    "Firemaking": {"rank": 0, "level": 0, "exp": 0},
    "Crafting": {"rank": 0, "level": 0, "exp": 0},
    "Smithing": {"rank": 0, "level": 0, "exp": 0},
    "Mining": {"rank": 0, "level": 0, "exp": 0},
    "Herblore": {"rank": 0, "level": 0, "exp": 0},
    "Agility": {"rank": 0, "level": 0, "exp": 0},
    "Thieving": {"rank": 0, "level": 0, "exp": 0},
    "Slayer": {"rank": 0, "level": 0, "exp": 0},
    "Farming": {"rank": 0, "level": 0, "exp": 0},
    "Runecrafting": {"rank": 0, "level": 0, "exp": 0},
    "Hunter": {"rank": 0, "level": 0, "exp": 0},
    "Construction": {"rank": 0, "level": 0, "exp": 0},
    "League Points": {"rank": 0, "score": 0},
    "Bounty Hunter - Hunter": {"rank": 0, "score": 0},
    "Bounty Hunter - Rogue": {"rank": 0, "score": 0},
    "Clue Scrolls (all)": {"rank": 0, "score": 0},
    "Clue Scrolls (beginner)": {"rank": 0, "score": 0},
    "Clue Scrolls (easy)": {"rank": 0, "score": 0},
    "Clue Scrolls (medium)": {"rank": 0, "score": 0},
    "Clue Scrolls (hard)": {"rank": 0, "score": 0},
    "Clue Scrolls (elite)": {"rank": 0, "score": 0},
    "Clue Scrolls (master)": {"rank": 0, "score": 0},
    "LMS - Rank": {"rank": 0, "score": 0},
    "Soul Wars Zeal": {"rank": 0, "score": 0},
    "Abyssal Sire": {"rank": 0, "score": 0},
    "Alchemical Hydra": {"rank": 0, "score": 0},
    "Barrows Chests": {"rank": 0, "score": 0},
    "Bryophyta": {"rank": 0, "score": 0},
    "Callisto": {"rank": 0, "score": 0},
    "Cerberus": {"rank": 0, "score": 0},
    "Chambers of Xeric": {"rank": 0, "score": 0},
    "Chambers of Xeric: Challenge Mode": {"rank": 0, "score": 0},
    "Chaos Elemental": {"rank": 0, "score": 0},
    "Chaos Fanatic": {"rank": 0, "score": 0},
    "Commander Zilyana": {"rank": 0, "score": 0},
    "Corporeal Beast": {"rank": 0, "score": 0},
    "Crazy Archaeologist": {"rank": 0, "score": 0},
    "Dagannoth Prime": {"rank": 0, "score": 0},
    "Dagannoth Rex": {"rank": 0, "score": 0},
    "Dagannoth Supreme": {"rank": 0, "score": 0},
    "Deranged Archaeologist": {"rank": 0, "score": 0},
    "General Graardor": {"rank": 0, "score": 0},
    "Giant Mole": {"rank": 0, "score": 0},
    "Grotesque Guardians": {"rank": 0, "score": 0},
    "Hespori": {"rank": 0, "score": 0},
    "Kalphite Queen": {"rank": 0, "score": 0},
    "King Black Dragon": {"rank": 0, "score": 0},
    "Kraken": {"rank": 0, "score": 0},
    "Kree'Arra": {"rank": 0, "score": 0},
    "K'ril Tsutsaroth": {"rank": 0, "score": 0},
    "Mimic": {"rank": 0, "score": 0},
    "Nightmare": {"rank": 0, "score": 0},
    "Phosani's Nightmare": {"rank": 0, "score": 0},
    "Obor": {"rank": 0, "score": 0},
    "Sarachnis": {"rank": 0, "score": 0},
    "Scorpia": {"rank": 0, "score": 0},
    "Skotizo": {"rank": 0, "score": 0},
    "Tempoross": {"rank": 0, "score": 0},
    "The Gauntlet": {"rank": 0, "score": 0},
    "The Corrupted Gauntlet": {"rank": 0, "score": 0},
    "Theatre of Blood": {"rank": 0, "score": 0},
    "Theatre of Blood: Hard Mode": {"rank": 0, "score": 0},
    "Thermonuclear Smoke Devil": {"rank": 0, "score": 0},
    "TzKal-Zuk": {"rank": 0, "score": 0},
    "TzTok-Jad": {"rank": 0, "score": 0},
    "Venenatis": {"rank": 0, "score": 0},
    "Vet'ion": {"rank": 0, "score": 0},
    "Vorkath": {"rank": 0, "score": 0},
    "Wintertodt": {"rank": 0, "score": 0},
    "Zalcano": {"rank": 0, "score": 0},
    "Zulrah": {"rank": 0, "score": 0}
}


class OsrsPrices:
    base_url = 'https://secure.runescape.com/m=itemdb_oldschool/api'
    last_call = None

    def __init__(self, identification: str, respect_rate_limiter: bool = True):
        self.header = {'user-agent': identification}
        self.respect_rate_limiter = respect_rate_limiter

    def __webcall(self, url: str):
        now = time.time()
        second_per_call = 2

        if self.last_call:
            wait = now - self.last_call
            if wait < second_per_call:
                if self.respect_rate_limiter:
                    sleep = second_per_call - wait
                    logging.debug(f'Respecting rate limiter sleeping: {sleep}')
                    time.sleep(sleep)
                else:
                    logging.warning('rate limiter may apply')

        data = requests.get(url, headers=self.header)
        self.last_call = now

        if len(data.text) == 0:
            raise ValueError('rate limiter applied by jagex')

        return data

    def images(self, item_id: int) -> list:
        '''
            get the icon's for an item
        '''
        icon = self.__webcall(
            f'https://secure.runescape.com/m=itemdb_oldschool/obj_sprite.gif?id={item_id}')
        icon_large = self.__webcall(
            f'https://secure.runescape.com/m=itemdb_oldschool/obj_big.gif?id={item_id}')
        return icon, icon_large

    def category(self) -> dict:
        url = f'{self.base_url}/catalogue/category.json?category=1'
        return self.__webcall(url).json()

    def items(self, letter: str, page: int = 0) -> dict:
        '''
            for each letter returns 12 items per page
        '''
        url = f'{self.base_url}/catalogue/items.json?category=1&alpha={letter}&page={page}'
        return self.__webcall(url).json()

    def itemDetail(self, item_id: int) -> dict:
        url = f'{self.base_url}/catalogue/detail.json?item={item_id}'
        return self.__webcall(url).json()

    def timeseries(self, item_id: int) -> dict:
        '''
            get timeseries of prices for an item
        '''
        url = f'{self.base_url}/graph/{item_id}.json'
        data = self.__webcall(url).json()

        # converting data in a more verbose way
        daily = [{'timestamp': key, 'price': value}
                 for key, value in data['daily'].items()]
        average = [{'timestamp': key, 'price': value}
                   for key, value in data['average'].items()]

        # recreate dictionary
        data = {}
        data['daily'] = daily
        data['average'] = average
        return data


class Hiscores:
    base_url = 'https://secure.runescape.com/m=itemdb_oldschool/api'
    last_call = None
    modes = ['hiscore_oldschool', 'hiscore_oldschool_ironman', 'hiscore_oldschool_hardcore_ironman',
             'hiscore_oldschool_ultimate', 'hiscore_oldschool_deadman', 'hiscore_oldschool_seasonal', 'hiscore_oldschool_tournament']

    def __init__(self, identification: str, respect_rate_limiter: bool = True):
        self.header = {'user-agent': identification}
        self.respect_rate_limiter = respect_rate_limiter

    def __webcall(self, url: str):
        now = time.time()
        second_per_call = 2

        if self.last_call:
            wait = now - self.last_call
            if wait < second_per_call:
                if self.respect_rate_limiter:
                    sleep = second_per_call - wait
                    logging.debug(f'Respecting rate limiter sleeping: {sleep}')
                    time.sleep(sleep)
                else:
                    logging.warning('rate limiter may apply')

        data = requests.get(url, headers=self.header)
        self.last_call = now

        if len(data.text) == 0:
            raise ValueError('rate limiter applied by jagex')

        return data

    def player(self, player_name: str, mode: str = 'hiscore_oldschool') -> dict:
        if not (mode in self.modes):
            raise ValueError(f'mode must be in: {self.modes}')

        url = f'{self.base_url}{mode}/index_lite.ws?player={player_name}'
        data = self.__webcall(url)
        rows = data.text.split()
        data = hiscore_dict.copy()

        if 'Incapsula' in rows:
            raise ValueError('blocked by jagex, incapsula')

        if not(len(rows) == len(data)):
            print(len(rows), len(data))
            raise ValueError(
                'Data is not the same size, hiscores have probably been updated')

        # parse data
        for row, key in zip(rows, data):
            row = [int(v) for v in row.split(',')]
            for i in range(len(row)):
                keys = [k[0] for k in data[key].items()]
                data[key][keys[i]] = row[i]

        return data


if __name__ == "__main__":
    api = OsrsPrices(identification='extreme4all#6456')
    print(api.category())
    api = Hiscores(identification='extreme4all#6456')
    d = api.player(player_name='extreme4all', mode='hiscore_oldschool')
    print(d)
