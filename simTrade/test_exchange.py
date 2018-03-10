"""Some tests for exchange class."""
from exchange import Exchange

def test_exchange_constructor():
    """Test the exchange class constructor with simple cases."""
    binance = Exchange("binance")
    assert (binance is not None), "Binance was not constructed"
    assert (binance.wallet["USD"] == 0),\
        "Binance should have wallet['USD'] == 0"
    assert (binance.name == "binance"), "Binance.name should equal 'binance'"

def test_exchange_deposit():
    """Test the exchange class deposit funciton with simple cases."""
    binance = Exchange("binance")
    binance.deposit("USD", 10)
    assert (binance.wallet["USD"] == 10),\
        "Deposit of 10 should raise value to 10"
    binance.deposit("BTC", 5)
    assert (binance.wallet["BTC"] == 5), "Deposit of new currency should work."
    binance.deposit("USD", 1)
    assert (binance.wallet["USD"] == 11), "Multiple deposits should work."

def test_exchange_trade():
    """Test the exchange class trade funciton with simple cases."""
    binance = Exchange("binance")
    binance.deposit("USD", 10)
    assert (binance.trade("USD", "USD", 1, 1)), "This is a valid trade."
    assert (binance.wallet["USD"] == 10), "Trade shouldn't have changed value"
    assert (not binance.trade("USD", "USD", 11, 11)), "Amount too large."
    assert (binance.trade("USD", "BTC", 5, 1)),\
        "Should be able to trade to new."
    assert (binance.wallet["USD"] == 5), "Trades should reduce fromCurrency."
    assert (binance.wallet["BTC"] == 1), "Trades should increase toCurrency."
    assert (binance.trade("BTC", "USD", 1, 1)), "Should be able to trade back."
    assert (binance.wallet["BTC"] == 0), "Should go to zero."

def test_exchange(verbose=True):
    """Test the exchange class with all created cases."""
    if verbose:
        print("Testing Exchange class...")
    test_exchange_constructor()
    if verbose:
        print("Passed Constructor Tests")
    test_exchange_deposit()
    if verbose:
        print("Passed Deposit Tests")
    test_exchange_trade()
    if verbose:
        print("Passed Trade Tests")
    if verbose:
        print("Passed all tests :)")

if __name__ == "__main__":
    test_exchange()
