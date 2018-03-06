""" This is a module for simulating arbitrage on crypto currencies.
"""
import time
import sys
import json
import ccxt
from exchange import Exchange

class ArbitrageSimulation: # pylint: disable=too-many-instance-attributes
    """This class can be used to create simulations for arbitrage crypto trading.
    TODO: example usage
    """
    def __init__(self, exchange0, exchange1, symbol):
        """ This initializes a simulation with given arguments."""
        self.exchange0 = exchange0
        self.exchange1 = exchange1
        self.symbol = symbol
        self.paper_exchange0 = Exchange(exchange0.name)
        self.paper_exchange1 = Exchange(exchange1.name)
        self.base_currency = symbol.split("/")[0]
        self.quote_currency = symbol.split("/")[1]
        self.profit = 0
        # Set initial balances in each market
        default_deposit_amount = 5
        default_quote_multiplier = 1e5
        self.paper_exchange0.deposit(self.base_currency,\
            default_deposit_amount)
        self.paper_exchange1.deposit(self.base_currency,\
            default_deposit_amount)
        self.paper_exchange0.deposit(self.quote_currency,\
            default_deposit_amount * default_quote_multiplier)
        self.paper_exchange1.deposit(self.quote_currency,\
            default_deposit_amount * default_quote_multiplier)

    def get_to_buy(self):
        """This method querries the exchanges to find the lowest asking price
        and returns it along with needed trade information."""
        orders0 = self.exchange0.fetch_order_book(self.symbol)
        orders1 = self.exchange1.fetch_order_book(self.symbol)
        buy0 = orders0["asks"][0] if orders0["asks"] else [0, 0]
        buy1 = orders1["asks"][0] if orders1["asks"] else [0, 0]
        if buy0[0] == min(buy0[0], buy1[0]):
            low_buy = buy0
            exchange = self.exchange0
        else:
            low_buy = buy1
            exchange = self.exchange1
        return {
            "price": low_buy[0],
            "amount": low_buy[1],
            "exchange": exchange,
            }

    def get_to_sell(self):
        """This method querries the exchanges to find the highest bid price
        and returns it along with needed trade information."""
        orders0 = self.exchange0.fetch_order_book(self.symbol)
        orders1 = self.exchange1.fetch_order_book(self.symbol)
        sell0 = orders0["bids"][0] if orders0["bids"] else [0, 0]
        sell1 = orders1["bids"][0] if orders0["bids"] else [0, 0]
        if sell0[0] == max(sell0[0], sell1[0]):
            high_sell = sell0
            exchange = self.exchange0
        else:
            high_sell = sell1
            exchange = self.exchange1
        return {
            "price": high_sell[0],
            "amount": high_sell[1],
            "exchange": exchange
            }

    def get_order(self):
        """This method combines buy and sell orders into a useful arbitrage
        order."""
        buy_info = self.get_to_buy()
        sell_info = self.get_to_sell()
        amount = min(buy_info["amount"], sell_info["amount"])
        buy_info["amount"] = amount
        sell_info["amount"] = amount
        return {"buy": buy_info, "sell": sell_info}

    def place_paper_order(self):
        """This method uses combined order information to make paper trades."""
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
        if order["sell"]["exchange"] == self.exchange0:
            sell_succeeded = self.paper_exchange0.trade(self.base_currency,\
                self.quote_currency, order["sell"]["amount"],\
                order["sell"]["amount"] * order["sell"]["price"])
        else:
            sell_succeeded = self.paper_exchange1.trade(self.base_currency,\
                self.quote_currency, order["sell"]["amount"],\
                order["sell"]["amount"] * order["sell"]["price"])
        if not sell_succeeded:
            return False
        if order["buy"]["exchange"] == self.exchange0:
            buy_succeeded = self.paper_exchange0.trade(self.quote_currency,\
              self.base_currency,\
              order["buy"]["amount"] * order["buy"]["price"],\
              order["buy"]["amount"])
        else:
            buy_succeeded = self.paper_exchange1.trade(self.quote_currency,\
                self.base_currency,\
                order["buy"]["amount"] * order["buy"]["price"],\
                order["buy"]["amount"])

        return buy_succeeded

    def start_simulation(self, duration=2):
        """This method simulates arbitrage trading printing the output."""
        start_time = time.time()
        starting_balances = [
            self.paper_exchange0.wallet.copy(),
            self.paper_exchange1.wallet.copy(),
            ]
        self.exchange0.load_markets()
        self.exchange1.load_markets()
        fail_count = 0
        while (time.time() - start_time) < duration * 60:
            if not self.place_paper_order():
                # paper order did not work so maybe stop trading
                print("Order failed")
                fail_count += 1
            if fail_count > 5:
                break
            time.sleep(.5)
        else:
            print("Duration complete.")
        self.print_output(starting_balances, duration, True, True)
        self.reset_balances(starting_balances)

    def reset_balances(self, starting_balances):
        """This method reset starting balances so simulation can be reran."""
        self.paper_exchange0.deposit(self.base_currency,\
            starting_balances[0][self.base_currency])
        self.paper_exchange0.deposit(self.quote_currency,\
            starting_balances[0][self.quote_currency])
        self.paper_exchange1.deposit(self.base_currency,\
            starting_balances[1][self.base_currency])
        self.paper_exchange1.deposit(self.quote_currency,\
            starting_balances[1][self.quote_currency])

    def print_output(self, starting_balances, duration, change=False,\
        totals=False):
        """This method prints out the results of the simulation."""
        print("After running arbitrage for " + str(duration) + " on the "\
            + self.exchange0.name + " and " + self.exchange1.name\
            + " exchanges in the market for " + self.symbol\
            + " the results were as follows:")
        print("Simple profit: " + str(self.profit))
        d_base0 = self.paper_exchange0.wallet[self.base_currency]\
            - starting_balances[0][self.base_currency]
        d_quote0 = self.paper_exchange0.wallet[self.quote_currency]\
            - starting_balances[0][self.quote_currency]
        d_base1 = self.paper_exchange1.wallet[self.base_currency]\
            - starting_balances[1][self.base_currency]
        d_quote1 = self.paper_exchange1.wallet[self.quote_currency]\
            - starting_balances[1][self.quote_currency]
        d_base = d_base0 + d_base1
        d_quote = d_quote0 + d_quote1
        if change:
            print(" Change in amount of currencies:")
            print("   " + self.base_currency)
            print("     " + self.exchange0.name + ":" + str(d_base0))
            print("     " + self.exchange1.name + ":" + str(d_base1))
            print("     Total:" + str(d_base))
            print("   " + self.quote_currency)
            print("     " + self.exchange0.name + ":" + str(d_quote0))
            print("     " + self.exchange1.name + ":" + str(d_quote1))
            print("     Total:" + str(d_quote))
            print()
        if totals:
            print("Starting Totals:")
            print(self.exchange0.name + " " + json.dumps(starting_balances[0]))
            print(self.exchange1.name + " " + json.dumps(starting_balances[1]))
            print("Ending Totals:")
            print(self.exchange0.name + " "\
                + json.dumps(self.paper_exchange0.wallet))
            print(self.exchange1.name + " "\
                + json.dumps(self.paper_exchange1.wallet))

if __name__ == "__main__":
    E = ccxt.exmo()
    G = ccxt.gdax()
    HIT = ccxt.hitbtc()
    BIT = ccxt.bittrex()
    CHOICES = [
        ArbitrageSimulation(BIT, HIT, "BTC/USDT"),
        ArbitrageSimulation(E, G, "BTC/USD"),
        ]
    CHOICE = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    SIM = CHOICES[CHOICE]
    if len(sys.argv) == 3:
        SIM.start_simulation(int(sys.argv[2]))
    elif len(sys.argv) > 3:
        for arg in sys.argv[2:]:
            SIM.start_simulation(int(arg))
    else:
        SIM.start_simulation(1)
        SIM.start_simulation(2)
        SIM.start_simulation(3)
        SIM.start_simulation(5)
