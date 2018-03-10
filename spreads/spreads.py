import ccxt

def get_spread(exchange0, exchange1, symbol, as_percent = False):
  """This function should get and return the difference between the max
  bid and min ask of two exchanges.
  @param exchange0 a ccxt exchange object
  @param exchange1 a ccxt exchange object
  @param as_percent a flag for deciding format of spread output.
  @return a tuple in the form of (spread, high bid, low ask)
  This will return a tuple of None if errors in the arguments.
  Example usage:

  spread, exchange , lowAsker = get_spread(someExchange, anotherOne, "BTC/USD")
  """

  order0, order1, maxBid, highBid = None, None, None, None
  minAsk, lowAsk = None, None

  try:
    exchange0.load_markets()
  except:
    print("exchange0 is not a ccxt exchange")
    return (None, None, None)
  try:
    exchange1.load_markets()
  except:
    print("exchange1 is not a ccxt exchange")
    return (None, None, None)
  try:
    # also could throw an exception if rate limit was reached but oh well
    order0 = exchange0.fetch_order_book(symbol)
  except:
    print(exchange0.name + " does not have a market for " + symbol)
    return (None, None, None)
  try:
    # also could throw an exception if rate limit was reached but oh well
    order1 = exchange1.fetch_order_book(symbol)
  except:
    print(exchange1.name + " does not have a market for " + symbol)
    return (None, None, None)

  if order0["bids"][0][0] > order1["bids"][0][0]:
    maxBid = order0["bids"][0][0]
    highBid = exchange0
  else:
    maxBid = order1["bids"][0][0]
    highBid = exchange1
  if order0["asks"][0][0] < order1["asks"][0][0]:
    minAsk = order0["asks"][0][0]
    lowAsk = exchange0
  else:
    minAsk = order1["asks"][0][0]
    lowAsk = exchange1
  if as_percent:
    return (2*(maxBid - minAsk)/(maxBid + minAsk), highBid, lowAsk)
  else:
    return (maxBid - minAsk, highBid, lowAsk)

def get_common_symbols(exchange0, exchange1):
  """This function can return a list of common markets that can be used to
  evaluate spreads.
  @param exchange0 a ccxt exchange object
  @param exchange1 a ccxt exchange object
  @return a list of common market symbols
  """

  try:
    exchange0.load_markets()
  except:
    print("exchange0 is not a ccxt exchange")
    return None
  try:
    exchange1.load_markets()
  except:
    print("exchange1 is not a ccxt exchange")
    return None

  return [s for s in exchange0.symbols if s in exchange1.symbols]

if __name__=="__main__":
  print("Can use this class to find spreads between exchanges")
# Uncomment the below to see an example
  # first = ccxt.exmo()
  # second = ccxt.hitbtc()
  # symbol = "BTC/USDT"
  # commonSymbols = get_common_symbols(first, second)
  # print(symbol in commonSymbols)
  # percentPlease = True
  # spread, bidder, asker = get_spread(first, second, symbol, percentPlease)
  # print(spread, bidder.name, asker.name)
