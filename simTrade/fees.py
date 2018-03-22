""" This is used by simulation to store, calculate, and charge fees."""
# from exchange import Exchange

class Fee:
    """This class can be used to calculate and respond to different fees.
    """
    total_fees = 0
    buy_rates = {
        "default": .0025,
        }
    sell_rates = {
        "default": .0025,
        }
    def __init__(self, exchange, amount, fee_type):
        """ This is a fee object. """
        self.exchange = exchange
        self.fee = amount
        self.fee_type = fee_type
        Fee.total_fees += amount

    @staticmethod
    def make_buy_fee(exchange, price_traded, amount_traded):
        """Return a transaction fee associated with a particular trade."""
        if exchange.name in Fee.buy_rates:
            rate = Fee.buy_rates[exchange.name]
        else:
            rate = Fee.buy_rates["default"]
        return Fee(exchange, rate * price_traded * amount_traded, "buy")

    @staticmethod
    def make_sell_fee(exchange, price_traded, amount_traded):
        """Return a transaction fee associated with a particular trade."""
        if exchange.name in Fee.sell_rates:
            rate = Fee.sell_rates[exchange.name]
        else:
            rate = Fee.sell_rates["default"]
        return Fee(exchange, rate * price_traded * amount_traded, "sell")

    @staticmethod
    def make_transaction_fees(order):
        """Given an order from simulation create fees and act on them."""
        sell = Fee.make_sell_fee(order["sell"]["exchange"],\
                order["sell"]["price"], order["sell"]["amount"])
        buy = Fee.make_buy_fee(order["buy"]["exchange"],\
                order["buy"]["price"], order["buy"]["amount"])
        return (buy, sell)
