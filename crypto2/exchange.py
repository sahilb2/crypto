"""This script could be used to simulate trades within exchanges."""
class Exchange:
    """This class can be used to paper trade on a single exchange."""
    def __init__(self, newName):
        """This should represent a new exchange and keep track of
        the amount of currency held in each individual exchange."""
        self.name = newName
        self.wallet = {"USD": 0}
    def trade(self, from_currency, to_currency, amount_given, amount_recieved):
        """This function simulates a trade of one currency for another by a
        given amount. Example call that trades one bitcoin for $100 dollars:
        binance = Exchange("binance")
        if binance.trade("BTC", "USD", 1, 100):
          print("Successfully traded 1 BTC for 100 USD")
        """
        if from_currency not in self.wallet.keys():
            print("From currency not in wallet.")
            return False
        if to_currency not in self.wallet:
            self.wallet[to_currency] = 0
        if self.wallet[from_currency] >= amount_given:
            self.wallet[from_currency] -= amount_given
            self.wallet[to_currency] += amount_recieved
            return True
        print("Insuffecient funds for trade:")
        print("Attempted: " + str(amount_given) + " Available: "\
            + str(self.wallet[from_currency]))
        return False
    def deposit(self, currency, amount):
        """This function allow for deposits into the wallet such that money can
        be added to the exchange arbitrarily without mere trades."""
        if currency not in self.wallet:
            self.wallet[currency] = 0
        self.wallet[currency] += amount
