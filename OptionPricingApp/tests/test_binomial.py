import sys, os
sys.path.append(os.path.abspath(".."))

# Import functions from the models I created
from models.black_scholes import call_price
from models.black_scholes import put_price
from models.binomial import binomial_price

# Test Binomial convergence to Black Scholes (both call and put options)
def test_binomial_euro_call_converges_to_bs():
    S, K, r, T, sigma = 100, 100, 0.01, 1.0, 0.2
    bs = call_price(S, K, r, T, sigma)
    bino = binomial_price(S, K, r, T, sigma, steps = 1000, type = "call", american = False)
    return abs(bino - bs) < 0.01

def test_binomial_euro_put_converges_to_bs():
    S, K, r, T, sigma = 100, 100, 0.01, 1.0, 0.2
    bs = put_price(S, K, r, T, sigma)
    bino = binomial_price(S, K, r, T, sigma, steps = 1000, type = "put", american = False)
    return abs(bino - bs) < 0.01

# Test to Make Sure American Call Code Works
def test_american_call_equals_euro_when_no_dividends():
    # American call on a non-dividend-paying stock should NOT be exercised early.
    S, K, r, T, sigma = 100, 100, 0.01, 1.0, 0.2
    euro = binomial_price(S, K, r, T, sigma, steps = 600, type = "call", american = False, div_yield = 0.0)
    amer = binomial_price(S, K, r, T, sigma, steps = 600, type = "call", american = True,  div_yield = 0.0)
    return abs(amer - euro) < 1e-6

def test_american_put_is_at_least_european_put():
    # American puts can have early-exercise value; price should be >= European.
    S, K, r, T, sigma = 100, 100, 0.05, 1.0, 0.2
    euro = binomial_price(S, K, r, T, sigma, steps = 600, type = "put", american = False)
    amer = binomial_price(S, K, r, T, sigma, steps = 600, type = "put", american = True)
    return amer - euro >= 0

print(test_binomial_euro_call_converges_to_bs())
print(test_binomial_euro_put_converges_to_bs())
print(test_american_call_equals_euro_when_no_dividends())
print(test_american_put_is_at_least_european_put())

