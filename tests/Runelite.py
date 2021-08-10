from osrs import runelite

api = runelite.RunelitePrices(identification='extreme4all#6456')

intervals = [
    '5m',
    '10m',
    '30m',
    '1h',
    '6h',
    '24h'
]

assert isinstance(api.items(), list)

for interval in intervals:
    assert isinstance(api.prices(interval), dict)
    assert isinstance(api.timeseries(interval=interval, id=2), dict)
    assert isinstance(api.timeseries(interval=interval, name='Cannonball'), dict)

# timestamp must be specific devicable based on interval
assert isinstance(api.prices(interval='24h', timestamp=1628380800), dict)
assert isinstance(api.latest(), dict)