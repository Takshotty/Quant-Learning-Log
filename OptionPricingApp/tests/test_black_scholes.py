# Test put-call parity for the black-scholes model that I created
import math
import sys, os
sys.path.append(os.path.abspath(".."))
from models.black_scholes import call_price
from models.black_scholes import put_price

# Put-Call parity states: underlying + long put = long call + risk-free bond

def test_put_call_parity(S, K, r, T, sigma):
    C = call_price(S, K, r, T, sigma)
    P = put_price(S, K, r, T, sigma)

    # Rearrange the formula to long call - long put = underlying - risk-free bond
    lhs = C - P
    rhs = S - K * math.exp(-r*T)

    # Check for AssertionErrors
    assert abs(lhs - rhs) < 1e-6

# Should get no AssertionErrors no matter what the parameters are
test_put_call_parity(100, 100, 0.05, 1, 0.2)
test_put_call_parity(50, 200, 0.03, 4, 0)