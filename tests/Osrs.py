from osrs.OSRS import OsrsPrices
from osrs import osrs

header = {'user-agent':'extreme4all#6456 - testing python package "osrs"'}
api = osrs.OsrsPrices(identification='extreme4all#6456')

assert isinstance(api.items('a'), dict)
assert isinstance(api.category(), dict)
assert isinstance(api.timeseries(4151), dict)
assert isinstance(api.itemDetail(4151), dict)
# assert isinstance(api.images(4151), list)