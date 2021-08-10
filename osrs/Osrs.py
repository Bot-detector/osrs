import logging
import time

import requests

class osrsPrices:
    def __init__(self, header, respect_rate_limiter=True):
        self.header = header
        self.base_url = 'https://secure.runescape.com/m=itemdb_oldschool/api'
        self.last_call = None
        self.respect_rate_limiter = respect_rate_limiter
    
    def __webcall(self, url):
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

    def images(self, item_id):
        '''
            get the icon's for an item
        '''
        icon = self.__webcall(f'https://secure.runescape.com/m=itemdb_oldschool/obj_sprite.gif?id={item_id}')
        icon_large = self.__webcall(f'https://secure.runescape.com/m=itemdb_oldschool/obj_big.gif?id={item_id}')
        return icon, icon_large
        
    def category(self):
        url = f'{self.base_url}/catalogue/category.json?category=1'
        return self.__webcall(url).json()

    def items(self, letter, page=0):
        '''
            for each letter returns 12 items per page
        '''
        url = f'{self.base_url}/catalogue/items.json?category=1&alpha={letter}&page={page}'
        return self.__webcall(url).json()

    def itemDetail(self, item_id):
        url = f'{self.base_url}/catalogue/detail.json?item={item_id}'
        return self.__webcall(url).json()

    def timeseries(self, item_id):
        '''
            get timeseries of prices for an item
        '''
        url = f'{self.base_url}/graph/{item_id}.json'
        data = self.__webcall(url).json()

        # converting data in a more verbose way
        daily = [{'timestamp': key, 'price': value } for key, value in data['daily'].items()]
        average = [{'timestamp': key, 'price': value } for key, value in data['average'].items()]

        # recreate dictionary
        data = {}
        data['daily'] = daily
        data['average'] = average
        return data


if __name__ == "__main__":
    header = {'user-agent':'extreme4all#6456'}

    api = osrsPrices(header=header)
    # print(api.timeseries(2))
    # print(api.category())
    # print(api.items('a'))
    # print(api.itemDetail(4151))
    print(api.images(4151))
