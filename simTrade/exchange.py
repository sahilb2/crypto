# This script could be used to simulate trades within exchanges.
class Exchange:
  def __init__(self, newName):
    """This should represent a new exchange and keep track of
    the amount of currency held in each individual exchange."""
    self.name = newName
    self.wallet = {"USD": 0}
  def trade(self,fromCurrency, toCurrency, amountGiven, amountRecieved):
    """This function simulates a trade of one currency for another by a given
    amount. Example call that trades one bitcoin for $100 dollars:
    binance = Exchange("binance")
    if binance.trade("BTC", "USD", 1, 100):
      print("Successfully traded 1 BTC for 100 USD")
    """
    if fromCurrency not in self.wallet.keys():
      print("From currency not in wallet.")
      return False
    if toCurrency not in self.wallet:
      self.wallet[toCurrency] = 0
    if self.wallet[fromCurrency] >= amountGiven:
      self.wallet[fromCurrency] -= amountGiven
      self.wallet[toCurrency] += amountRecieved
      return True
    else:
      print("Insuffecient funds for trade:")
      print("Attempted: " + str(amountGiven) + " Available: "\
          + str(self.wallet[fromCurrency]))
      return False
  def deposit(self, currency, amount):
    """This function allow for deposits into the wallet such that money can
    be added to the exchange arbitrarily without mere trades."""
    if currency not in self.wallet:
      self.wallet[currency] = 0
    self.wallet[currency] += amount
