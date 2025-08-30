import numpy as np

# Import normal distribution methods through scipy (like cumulative distribution functions)
from scipy.stats import norm

# Define the method for determining call option price given the 5 main arguments 
def call_price(S, K, r, T, sigma):
    """
    Parameters:
    S: current stock price (in USD)
    K: strike price (in USD)
    r: risk-free rate (as a decimal, not a percentage)
    T: time to expiration (in years)
    sigma: volatility (as a decimal)
    """

    # Check if the call option is expired (if so, the call is worth the larger value of S - K and 0
    if T <= 0: 
        price = max(S - K, 0)
        return price
    
    # Deterministic case (if no volatility, then same as if the call was expired except must discount strike)
    if sigma == 0:
        price = max(S - K * np.exp(-r*T), 0)
        return price
    
    # Black Scholes Formula, using mathematical methods from numpy and scipy libraries
    d1 = (np.log(S / K) + (r + 0.5 * (sigma ** 2)) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# Define the method for determining put option price given the 5 main arguments 
def put_price(S, K, r, T, sigma):
    """
    (Same as above but displayed here again)
    Parameters:
    S: current stock price (in USD)
    K: strike price (in USD)
    r: risk-free rate (as a decimal, not a percentage)
    T: time to expiration (in years)
    sigma: volatility (as a decimal)
    """

    # Check if the put option is expired (if so, the put is worth the larger value of K - S and 0)
    if T <= 0:
        price = max(K - S, 0)
        return price
    
    # Deterministic case (if no volatility, then same as if the put was expired except must discount strike)
    if sigma == 0:
        price = max(K * np.exp(-r*T) - S, 0)
        return price
    
    # Black Scholes Formula, exact same as for the call except flip the signs!
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# Define a method that returns the Greeks (in a dictionary)
def greeks(S, K, r, T, sigma):

    # If the option is expired, then all the Greeks = 0
    if T <= 0:
        return {"delta": 0, "gamma": 0, "vega": 0, "theta": 0, "rho": 0}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    pdf_d1 = norm.pdf(d1)

    """ 
    Making sense of the Greeks (I recommend referring to Investopedia if you want more clarity)
    Delta: Represents the price sensitivity of the option relative to the underlying.
    Gamma: Represents the rate of change between an options's delta and the underlying asset's price. 
    Vega: Represents the rate of change between an option's value and the underlying's implied volatility.
    Theta: Represents the time sensitivity of the option (sometimes known as time decay)
    Rho: Represents the rate of change between an option's value and a 1% change in the interest rate
    """
    delta = norm.cdf(d1)
    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T)
    theta = -(S * pdf_d1 * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d2)
    rho = K * T * np.exp(-r * T) * norm.cdf(d2)

    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}
