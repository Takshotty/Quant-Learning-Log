import numpy as np

""" 
Note: For the Black Scholes model, I created two separate functions (one for call options and one for put options) to reduce the number
of parameters. For the Binomial model, however, given that there are already additional parameters, I will be creating just one function
that also incorporates an additional argument and checks if the option type is a call or a put.

Accepts 9 parameters, with the first five being the same as the Black Scholes Model:
S -> Underlying price (spot price)
K -> Strike price
r -> Risk-free interest rate
T -> Time to expiration in years
sigma -> Volatility (standard deviation)
steps -> Number of time steps in the binomial tree
type -> Either "call" or "put" (self-explanatory)
american -> If True, then early exercise (prior to maturity/expiration date) is allowed at any point; if False, 
it is a European option and must be exercised at expiration
div_yield -> continuous dividend yield (usually denoted as q)

This was one of the most challenging parts of the project to code so I added lots of comments to help you all (and myself) follow along
"""
def binomial_price(
    S, K, r, T, sigma, steps,
    type = "Call",
    american = False,
    div_yield = 0.0
):
    # Check if the call option is expired (if so, the call is worth the larger value of S - K and 0)
    if T <= 0:
        if type == "Call":
            price = max(S - K, 0)
            return price
        else:
            price = max(K - S, 0)
            return price

    # Ensure that there is at least 1 time step! 
    if steps < 1:
        raise ValueError("steps must be >= 1")

    # If the volatility is zero, then the stock price is deterministic (no randomness) and the option payoff is simply discounted back
    if sigma <= 0:
        # Calculate the guaranteed value of the stock at maturity by accounting for the risk-free interest rate & time
        ST = S * np.exp((r - div_yield) * T)
        # Calculate the discount rate (we will discount the expected payoff at maturity back to present value!)
        disc = np.exp(-r * T)
        if type == "Call":
            return disc * max(ST - K, 0.0)
        else:
            return disc * max(K - ST, 0.0)

    # Parameters :)
    # Store time per each step in the variable dt (discrete time step)
    dt = T / steps
    # Store the "up factor" (how much the stock price goes up by each step) in the variable u
    u = np.exp(sigma * np.sqrt(dt))
    # Store the "down factor" (how much the stock price goes down by each step) in the variable d
    d = 1.0 / u
    # Store the discount rate PER step in the variable disc
    disc = np.exp(-r * dt)
    # Calculate the probability (risk-free probability) of an "up" move
    p = (np.exp((r - div_yield) * dt) - d) / (u - d)

    # Ensure that the probability is from 0 to 1 (tree breaks if not)
    if not (0.0 < p < 1.0):
        raise ValueError(f"Invalid probability p = {p:.6f}")

    # Calculate the option's terminal value (value at maturity before we work backwards)
    # Create an array of possible number of "up" moves (from 0 to the total number of steps)
    j = np.arange(steps + 1)
    # Compute the stock price at maturity for all possible paths; recall j represents # of up moves, and steps - j represents # of down moves
    ST = S * (u ** j) * (d ** (steps - j))
    # Store all the possible options payoffs in the variable values
    if type == "Call":
        values = np.maximum(ST - K, 0)
    else:
        values = np.maximum(K - ST, 0)

    # Backwards Induction. Probably the most confusing part of the entire project (took me several times to wrap my head around this)!
    # Loop through each step BACKWARDS in time, starting at the second-to-last time stamp
    for i in range(steps - 1, -1, -1):
        # Recall that values currently holds the options payoffs at time step i+1 (before starting the loop)
        # For each time step, we want to discount each possible expected value
        values = disc * (p * values[1:] + (1 - p) * values[:-1])
        # Find the optimal time to exercise the option if the option is American
        if american:
            # Create a vector that contains the stock prices for every single time stamp (in this case for time i)
            Sj = S * (u ** np.arange(i + 1)) * (d ** (i - np.arange(i + 1)))
            # Immediate exercise payoffs for each time stamp (considering the type of option of course)
            if type == "Call":
                exercise = np.maximum(Sj - K, 0.0)
            else:
                exercise = np.maximum(K - Sj, 0.0)
            values = np.maximum(values, exercise)
    # Once the backwards loop, values has been collapsed down to just one value: the option's fair price
    price = float(values[0])
    return price