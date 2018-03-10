"""Simple simulation script."""
import time
import ccxt


def make_trade(revenue, cost):
    """Record profit if trade were to be made."""
    return revenue - cost
    # print("making trade...")

def get_buy_price(exchange0, exchange1, symbol):
    """Find lowest price to buy from."""
    buy0 = exchange0.fetch_order_book(symbol)["asks"][0][0]
    buy1 = exchange1.fetch_order_book(symbol)["asks"][0][0]
    low_buy = min(buy0, buy1)
    return low_buy

def get_sell_price(exchange0, exchange1, symbol):
    """Find highest price to sell for."""
    sell0 = exchange0.fetch_order_book(symbol)["bids"][0][0]
    sell1 = exchange1.fetch_order_book(symbol)["bids"][0][0]
    high_sell = max(sell0, sell1)
    return high_sell

def simple_simulate(exchange0=ccxt.exmo(), exchange1=ccxt.hitbtc(),\
    symbol="BTC/USDT", duration=5):
    """Run the simple simulation."""
    start_time = time.time()
    rate_limit = max(exchange0.rateLimit, exchange1.rateLimit)
    exchange0.load_markets()
    exchange1.load_markets()
    profits = 0
    while (time.time() - start_time) < duration * 60:
        cost = get_buy_price(exchange0, exchange1, symbol)
        revenue = get_sell_price(exchange0, exchange1, symbol)
        profits += make_trade(revenue, cost)
        time.sleep(rate_limit/1000.0)
    print("Total profits made trading on " + exchange0.name + " and "\
        + exchange1.name + " in the market of " + symbol + " over "\
        + str(duration) + " minutes were:")
    print(profits)
    return profits

if __name__ == "__main__":
    simple_simulate(duration=.25)
    simple_simulate(duration=2)
    # simple_simulate(duration = 5)
