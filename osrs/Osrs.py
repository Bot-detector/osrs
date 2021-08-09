import requests
import time
import logging


class osrsPrices:
    def __init__(self, header):
        self.header = header
        self.base_url = 'https://secure.runescape.com/m=itemdb_oldschool/api'
        self.last_call = None
    
    def category(self):
        url = f'{self.base_url}/catalogue/category.json?category=1'
        data = requests.get(url, headers=self.header)
        
        if len(data.text) == 0:
            raise ValueError('rate limiter applied by jagex')
        return data.json()

    def items(self, letter, page=0):
        '''
            for each letter returns 12 items per page
        '''
        url = f'{self.base_url}/catalogue/items.json?category=1&alpha={letter}&page={page}'
        data = requests.get(url, headers=self.header)

        if len(data.text) == 0:
            raise ValueError('rate limiter applied by jagex')
        
        return data.json()

    def itemDetail(self, item_id):
        url = f'{self.base_url}/catalogue/detail.json?item={item_id}'
        data = requests.get(url, headers=self.header)

        if len(data.text) == 0:
            raise ValueError('rate limiter applied by jagex')
        
        return data.json()

    def timeseries(self, item_id):
        '''
            get timeseries of prices for an item
        '''
        now = time.time()
        if self.last_call and now - self.last_call < 2:
            logging.warning('rate limiter may apply')

        url = f'{self.base_url}/graph/{item_id}.json'
        data = requests.get(url, headers=self.header)
        self.last_call = now
        
        if len(data.text) == 0:
            raise ValueError('rate limiter applied by jagex')

        data = data.json()

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
    print(api.itemDetail(4151))