import ccxt
import time

global profits
profits = 0

def make_trade(revenue, cost):
  global profits
  profits += (revenue - cost)
  # print("making trade...")

def get_buy_price(exchange0, exchange1, symbol):
  buy0 = exchange0.fetch_order_book(symbol)["asks"][0][0]
  buy1 = exchange1.fetch_order_book(symbol)["asks"][0][0]
  lowBuy = min(buy0, buy1)
  return lowBuy

def get_sell_price(exchange0, exchange1, symbol):
  sell0 = exchange0.fetch_order_book(symbol)["bids"][0][0]
  sell1 = exchange1.fetch_order_book(symbol)["bids"][0][0]
  highSell = max(sell0, sell1)
  return highSell

def simple_simulate(exchange0 = ccxt.exmo(), exchange1 = ccxt.hitbtc(),\
    symbol = "BTC/USDT", duration = 5):
  start_time = time.time()
  rate_limit = max(exchange0.rateLimit, exchange1.rateLimit)
  current_period = time.time()
  exchange0.load_markets()
  exchange1.load_markets()
  while((time.time() - start_time) < duration * 60):
    cost = get_buy_price(exchange0, exchange1, symbol)
    revenue = get_sell_price(exchange0, exchange1, symbol)
    make_trade(revenue, cost)
    time.sleep(rate_limit/1000.0)
  print("Total profits made trading on " + exchange0.name + " and "\
      + exchange1.name + " in the market of " + symbol + " over "\
      + str(duration) + " minutes were:")
  global profit
  print(profits)
  return profits

if __name__ == "__main__":
  simple_simulate(duration = .25)
  profits = 0
  simple_simulate(duration = 2)
  profits = 0
  # simple_simulate(duration = 5)
  # profits = 0
