# osrs
The goal is to make a wrapper around the varius runescape related api's

# usage
you must set a header, preferably with a discord tag or email
```
from osrs import Runelite
header = {'user-agent':'extreme4all#6456'}

api = Runelite.runelitePrices(header=header)
```
Runelite prices api: https://prices.runescape.wiki/api/v1/osrs/
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
