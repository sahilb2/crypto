# some tests for simTrade
from simTrade import Exchange

def testExchangeConstructor():
  binance = Exchange("binance")
  assert (binance is not None), "Binance was not constructed"
  assert (binance.wallet["USD"] == 0), "Binance should have wallet['USD'] == 0"
  assert (binance.name == "binance"), "Binance.name should equal 'binance'"

def testExchangeDeposit():
  binance = Exchange("binance")
  binance.deposit("USD", 10)
  assert (binance.wallet["USD"] == 10), "Deposit of 10 should raise value to 10"
  binance.deposit("BTC", 5)
  assert (binance.wallet["BTC"] == 5), "Deposit of new currency should work."
  binance.deposit("USD", 1)
  assert (binance.wallet["USD"] == 11), "Multiple deposits should work."

def testExchangeTrade():
  binance = Exchange("binance")
  binance.deposit("USD", 10)
  assert (binance.trade("USD", "USD", 1, 1)), "This is a valid trade."
  assert (binance.wallet["USD"] == 10), "Trade shouldn't have changed value"
  assert (binance.trade("USD", "USD", 11, 11) == False), "Amount too large."
  assert (binance.trade("USD", "BTC", 5, 1)), "Should be able to trade to new."
  assert (binance.wallet["USD"] == 5), "Trades should reduce fromCurrency."
  assert (binance.wallet["BTC"] == 1), "Trades should increase toCurrency."
  assert (binance.trade("BTC", "USD", 1, 1)), "Should be able to trade back."
  assert (binance.wallet["BTC"] == 0), "Should go to zero."

def testExchange(verbose = True):
  if verbose: print("Testing Exchange class...")
  testExchangeConstructor()
  if verbose: print("Passed Constructor Tests")
  testExchangeDeposit()
  if verbose: print("Passed Deposit Tests")
  testExchangeTrade()
  if verbose: print("Passed Trade Tests")
  if verbose: print("Passed all tests :)")

if __name__ == "__main__":
  testExchange()
