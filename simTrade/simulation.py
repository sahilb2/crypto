import ccxt
from exchange import Exchange
import time
import json

class Arb_Simulation:
  """This class can be used to create simulations for arbitrage crypto trading.
  TODO: example usage
  """
  def __init__(self, exchange0, exchange1, symbol, duration = 1):
    self.exchange0 = exchange0
    self.exchange1 = exchange1
    self.symbol = symbol
    self.duration = duration
    self.paper_exchange0 = Exchange(exchange0.name)
    self.paper_exchange1 = Exchange(exchange1.name)
    self.base_currency = symbol.split("/")[0]
    self.quote_currency = symbol.split("/")[1]
    # Set initial balances in each market
    default_deposit_amount = 100000
    self.paper_exchange0.deposit(self.base_currency, default_deposit_amount)
    self.paper_exchange1.deposit(self.base_currency, default_deposit_amount)
    self.paper_exchange0.deposit(self.quote_currency, default_deposit_amount)
    self.paper_exchange1.deposit(self.quote_currency, default_deposit_amount)
    self.rate_limit = max(exchange0.rateLimit, exchange1.rateLimit)
    self.profit = 0

  def get_to_buy(self):
    orders0 = self.exchange0.fetch_order_book(self.symbol)
    orders1 = self.exchange1.fetch_order_book(self.symbol)
    buy0 = orders0["asks"][0]
    buy1 = orders1["asks"][0]
    if buy0[0] == min(buy0[0], buy0[0]):
      lowBuy = buy0
      exchange = self.exchange0
    else:
      lowBuy = sell1
      exchange = self.exchange1
    return {"price": lowBuy[0], "amount": lowBuy[1], "exchange": exchange}

  def get_to_sell(self):
    orders0 = self.exchange0.fetch_order_book(self.symbol)
    orders1 = self.exchange1.fetch_order_book(self.symbol)
    sell0 = orders0["bids"][0]
    sell1 = orders1["bids"][0]
    if sell0[0] == max(sell0[0], sell1[0]):
      highSell = sell0
      exchange = self.exchange0
    else:
      highSell = sell1
      exchange = self.exchange1
    return {"price": highSell[0], "amount": highSell[1], "exchange": exchange}

  def get_order(self):
    buy_info = self.get_to_buy()
    sell_info = self.get_to_sell()
    amount = min(buy_info["amount"], sell_info["amount"])
    buy_info["amount"] = amount
    sell_info["amount"] = amount
    return {"buy": buy_info, "sell": sell_info}

  def place_paper_order(self):
    order = self.get_order()
    self.profit += (order["sell"]["price"]\
        - order["buy"]["price"]) * order["buy"]["amount"]
    if order["sell"]["price"] - order["buy"]["price"] <= 0:
      # not a profitable order
      print("Sell at " + str(order["sell"]["price"]) + " Buy at "\
          + str(order["buy"]["price"]))
      print("Skipping...")
      return True
    # Not entirely sure how trading money works? My best guess.
    # But even if it's wrong the simulation will look like it's working.
    if (order["sell"]["exchange"] == self.exchange0):
      sell_succeeded = self.paper_exchange0.trade(self.base_currency,\
          self.quote_currency, order["sell"]["amount"],\
          order["sell"]["amount"] * order["sell"]["price"])
    else:
      sell_succeeded = self.paper_exchange1.trade(self.base_currency,\
          self.quote_currency, order["sell"]["amount"],\
          order["sell"]["amount"] * order["sell"]["price"])
    if not sell_succeeded:
      return False
    if (order["buy"]["exchange"] == self.exchange0):
      buy_succeeded = self.paper_exchange0.trade(self.quote_currency,\
         self.base_currency, order["buy"]["amount"] * order["buy"]["price"],\
         order["buy"]["amount"])
    else:
      buy_succeeded = self.paper_exchange1.trade(self.quote_currency,\
         self.base_currency, order["buy"]["amount"] * order["buy"]["price"],\
         order["buy"]["amount"])

    return buy_succeeded

  def start_simulation(self):
    start_time = time.time()
    starting_balances = [
        self.paper_exchange0.wallet.copy(),
        self.paper_exchange1.wallet.copy(),
        ]
    self.exchange0.load_markets()
    self.exchange1.load_markets()
    fail_count = 0
    while(fail_count < 5 and (time.time() - start_time) < self.duration * 60):
      if not self.place_paper_order():
        # paper order did not work so maybe stop trading
        print("Order failed")
        fail_count += 1
    else:
      print("Duration complete.")
    self.print_output(starting_balances, True, True)

  def print_output(self, starting_balances, change = False, totals = False):
    print("After running arbitrage for " + str(self.duration) + " on the "\
        + self.exchange0.name + " and " + self.exchange1.name + " exchanges "\
        + "in the market for " + self.symbol + " the results were as follows:")
    print("Simple profit: " + str(self.profit))
    dBase0 = self.paper_exchange0.wallet[self.base_currency]\
        - starting_balances[0][self.base_currency]
    dQuote0 = self.paper_exchange0.wallet[self.quote_currency]\
        - starting_balances[0][self.quote_currency]
    dBase1 = self.paper_exchange1.wallet[self.base_currency]\
        - starting_balances[1][self.base_currency]
    dQuote1 = self.paper_exchange1.wallet[self.quote_currency]\
        - starting_balances[1][self.quote_currency]
    dBase = dBase0 + dBase1
    dQuote = dQuote0 + dQuote1
    if change:
      print(" Change in amount of currencies:")
      print("   " + self.base_currency)
      print("     " + self.exchange0.name + ":" + str(dBase0))
      print("     " + self.exchange1.name + ":" + str(dBase1))
      print("     Total:" + str(dBase))
      print("   " + self.quote_currency)
      print("     " + self.exchange0.name + ":" + str(dQuote0))
      print("     " + self.exchange1.name + ":" + str(dQuote1))
      print("     Total:" + str(dQuote))
      print()
    if totals:
      print("Starting Totals:")
      print(self.exchange0.name + " " + json.dumps(starting_balances[0]))
      print(self.exchange1.name + " " + json.dumps(starting_balances[1]))
      print("Ending Totals:")
      print(self.exchange0.name + " " + json.dumps(self.paper_exchange0.wallet))
      print(self.exchange1.name + " " + json.dumps(self.paper_exchange1.wallet))

if __name__=="__main__":
  e = ccxt.exmo()
  h = ccxt.hitbtc()
  sim = Arb_Simulation(e, h, "BTC/USDT", 1)
  sim.start_simulation()
  sim = Arb_Simulation(e, h, "BTC/USDT", 3)
  sim.start_simulation()
  sim = Arb_Simulation(e, h, "BTC/USDT", 5)
  sim.start_simulation()
  sim = Arb_Simulation(e, h, "BTC/USDT", 30)
  sim.start_simulation()
