# The project
The goal is to make a wrapper around the varius runescape related api's.
i am thinking of
Runelite prices api: https://prices.runescape.wiki/api/v1/osrs/
osrs api: https://secure.runescape.com/m=itemdb_oldschool/api
wiki api: 

# Runelite
## prices
Runelite prices api: https://prices.runescape.wiki/api/v1/osrs/
you must set a header, preferably with a discord tag or email
```
from osrs import Runelite
header = {'user-agent':'extreme4all#6456'}

api = Runelite.runelitePrices(header=header)
```
to get a mapping of item names, id, low & high alch values etc
```
print(api.items())
```
to get latest prices averaging over an interval or from a specific timestamp
```
intervals = [
    '5m',
    '10m',
    '30m',
    '1h',
    '6h',
    '24h'
]
print(api.prices(interval='24h'))
print(api.prices(interval='24h', timestamp=1628380800))
```
to get a timeseries of the 300 values averaged over interval by item id or item name
```
print(api.timeseries(interval='5m', id=2))
print(api.timeseries(interval='5m', name='Cannonball'))
```

to get the latest prices of items
```
print(api.latest())
```
# OSRS
The osrs endpoints, these endpoints are heavily rate limited
## osrsPrices
```
from osrs import OSRS

header = {'user-agent':'extreme4all#6456 - testing python package "osrs"'}
api = OSRS.osrsPrices(header=header)
```
OSRS has only one category, with all the items, here you get each alpha or letter and howmany items are in it
```
print(api.category())
```
The items endpoint is paginated and will return 12 items for each page
```
print(api.items(letter='a', page=0))
```
You can get the itemDetails for a specific item, based on item_id
```
print(api.itemDetail(item_id=4151))
```
You can get the item price as a timeseries based on item_id
```
print(api.timeseries(item_id=4151))
```
## hiscores
return the hiscore for a player
```
from osrs import OSRS

header = {'user-agent':'extreme4all#6456 - testing python package "osrs"'}
api = OSRS.hiscores(header=header)
modes = [
    'hiscore_oldschool', 'hiscore_oldschool_ironman', 'hiscore_oldschool_hardcore_ironman',
    'hiscore_oldschool_ultimate','hiscore_oldschool_deadman','hiscore_oldschool_seasonal',
    'hiscore_oldschool_tournament'
]
    
print(api.player(player_name='extreme4all', mode='hiscore_oldschool'))
```
# development
## setup
```
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## for admin purposes saving & upgrading

```
venv\Scripts\activate
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '==', '>=' } | Set-Content requirements.txt"
call pip install -r requirements.txt --upgrade
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '>=', '==' } | Set-Content requirements.txt"
```
## build & publish
building package and deploying to pypi
```
python -m build
python -m twine upload osrs dist/*
```
