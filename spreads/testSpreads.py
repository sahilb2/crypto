from spreads import *
import ccxt

def test_get_spread():
  print("Testing get_spread()...")
  a = ccxt.exmo()
  b = ccxt.hitbtc()
  c = ccxt.kraken()
  d = ccxt.binance()
  e = ccxt.huobi()
  f = "myMadeUpExchangeName"
  g = "binance"
  s0 = "BTC/USDT"
  s1 = "LTC/BTC"
  s3 = "Not real"
  assert get_spread(a, b, s0)[0] is not None, "Example of valid comparison"
  assert get_spread(a, b, s1)[0] is not None, "Example of valid comparison"
  assert get_spread(d, c, s0)[0] is None, "Example of market without sym"
  assert get_spread(a, f, s0)[0] is None, "Example of invalid exchange"
  assert get_spread(a, b, s3)[0] is None, "Example of invalid symbol"
  assert get_spread(a, b, s0, True)[0] <= 1, "Percent should be less than 1"
  assert get_spread(a, b, s0, True)[0] >= 0, "Spread cannot be less than 1"
  assert get_spread(a, b, s0)[0] >= 0, "Spread cannot be less than 1"
  assert len(get_spread(a, b, s0)) == 3, "Tuple length should be 3."
  assert len(get_spread(a, f, s0)) == 3, "Tuple length should be 3."
  assert len(get_spread(a, b, s3)) == 3, "Tuple length should be 3."
  print("Passed get_spreads() test...")

def test_get_common_symbols():
  print("Testing get_common_symbols()...")
  a = ccxt.exmo()
  b = ccxt.hitbtc()
  c = ccxt.kraken()
  d = ccxt.binance()
  e = ccxt.huobi()
  f = "myMadeUpExchangeName"
  g = "binance"
  s0 = "BTC/USDT"
  s1 = "LTC/BTC"
  s3 = "Not real"
  assert get_common_symbols(a, b) is not None, "Should have some in common"
  assert s0 in get_common_symbols(a, b), s0 + " is in both of these."
  assert get_common_symbols(a, f) is None, "Made up exchange"
  assert len(get_common_symbols(a, b)) == 14, "Should have consistent length."
  print("Passed get_common_symbols() test...")

def testAll():
  print("Begining tests...")
  test_get_spread()
  test_get_common_symbols()
  print("Passed all tests.")

if __name__=="__main__":
  testAll()
