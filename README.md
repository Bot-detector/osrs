# The project
The goal is to make a wrapper around the varius runescape related api's.

# Runelite
## prices
Runelite prices api: https://prices.runescape.wiki/api/v1/osrs/
you must provide some identification to tell who you are, preferably with a discord tag or email
```
from osrs import runelite

api = runelite.RunelitePrices(identification='extreme4all#6455')
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
from osrs import osrs

api = osrs.OsrsPrices(identification='extreme4all#6456')
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
from osrs import osrs

api = osrs.Hiscores(identification='extreme4all#6456')
modes = [
    'hiscore_oldschool', 'hiscore_oldschool_ironman', 'hiscore_oldschool_hardcore_ironman',
    'hiscore_oldschool_ultimate','hiscore_oldschool_deadman','hiscore_oldschool_seasonal',
    'hiscore_oldschool_tournament'
]
    
print(api.player(player_name='extreme4all', mode='hiscore_oldschool'))
```

