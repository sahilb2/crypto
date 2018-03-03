# Test different features of ccxt library.
import ccxt

if __name__ == "__main__":
  # print("ccxt list of exchanges...")
  # print(ccxt.exchanges)
  # binance = ccxt.binance()
  # binance.load_markets()
  # print("Loaded binance markets...")
  # print("Binance rate limit...")
  # print(binance.rateLimit)
  # symbols = binance.symbols
  # print("List of binance's symbols...")
  # print(symbols)
  # currencies = binance.currencies
  # print("List of binance's currencies...")
  # print(currencies)
  # print("The market for the first symbol...")
  # print(binance.markets[symbols[0]])
  # print("The market for BTC/USDT...")
  # print(binance.markets["BTC/USDT"])
  # print("Recent trades for symbol[0]...")
  # print(binance.fetch_trades(symbols[0]))
  # print("Recent trades for BTC/USD...")
  # print(binance.fetch_trades("BTC/USDT"))
  # print("Ticker for symbol...")
  # print(binance.fetch_ticker(symbols[0]))
  # print("Ticker for BTC/USDT...")
  # print(binance.fetch_ticker("BTC/USDT"))
  # print("order book for symbol...")
  # print(binance.fetch_order_book(symbols[0], 5))
  # print("order book for BTC/USDT...")
  # print(binance.fetch_order_book("BTC/USDT", 5))
  # print("Price spread of btc/USDT...")
  # first = ccxt.hitbtc()
  # first.load_markets()
  # o = first.fetch_order_book("BTC/USDT")
  # print(o["asks"][0][0] - o["bids"][0][0])
  # print("spread across exchanges...")
  # second = ccxt.exmo()
  # second.load_markets()
  # o1 = second.fetch_order_book("BTC/USDT")
  # maxBid = o["bids"][0][0] if o["bids"][0][0] > o1["bids"][0][0] \
  #    else o1["bids"][0][0]
  # minAsk = o["asks"][0][0] if o["asks"][0][0] < o1["asks"][0][0] \
  #    else o1["asks"][0][0]
  # print("maxBid - minAsk")
  # print(maxBid - minAsk)
  # print("maxBid - minAsk/midpoint")
  # print((maxBid - minAsk)*2/(maxBid + minAsk))
  print("Uncomment lines to see what ccxt can do..")
