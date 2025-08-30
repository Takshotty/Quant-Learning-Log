# Enable Python to find modules from the parent directory (OptionPricingApp)
import sys, os
sys.path.append(os.path.abspath(".."))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Importing pricing models (will do convergence plot again towards the bottom)
from models.binomial import binomial_price
from models.black_scholes import call_price, put_price



st.title("Binomial Pricing Model")
st.write("""
This page demonstrates the Binomial option pricing model.
Feel free to play around with the parameters on the left! (You'll notice that there are a few more to choose from compared to the Black-Scholes Model) Explore
the effects of the parameters on the option price and the diagrams
below! Have fun :)
"""
)

# PARAMETER SLIDERS (except prices so the user can type in a number)!!! 
st.sidebar.header("Binomial Parameters")
S = st.sidebar.number_input("Current Asset Price (S)", min_value = 0.01, value = 100.00)
K = st.sidebar.number_input("Strike Price (K)", min_value = 0.01, value = 100.00)
r = st.sidebar.slider("Risk-free Interest Rate (r)", 0.0, 0.1, 0.01, step = 0.005)
T = st.sidebar.slider("Time to Expiration (T in years)", 0.0, 5.0, 1.0, step = 0.1)
sigma = st.sidebar.slider("Volatility (σ)", 0.0, 1.0, 0.2, step = 0.01)
steps = st.sidebar.slider("Number of Steps", 1, 1024, 250, step = 1)
# The option type and whether it's American or European are binary so I used a drop down menu (selectbox instead of radio)
type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
american = st.sidebar.selectbox("American Option?", [True, False])


# Calculate & Display Binomial Price
# Round to nearest Hundredth (since we want it in cents)
bin_price = round(binomial_price(S, K, r, T, sigma, steps, type, american), 2)
# Displaying in bold (using **)
st.subheader(f"**{type} Option Price:** :$blue[{bin_price}]")



# PAYOFF DIAGRAM (Yes I'm reusing the entire code from Black Scholes)
st.subheader("Payoff Diagram")

# Choose the option position (I used st.selectbox for a drop-down menu but st.radio would have also sufficed)
position = st.selectbox("Position", ["Long", "Short"])

# Range of possible stock prices at expiration for the graph (going from -50% to +50% for simplicity)
S_range = np.linspace(0.5 * K, 1.5 * K, 200)

# Compute payoff at expiration based off of option type & position
if type == "Call":
    payoff = np.maximum(S_range - K, 0)
else:
    payoff = np.maximum(K - S_range, 0)
if position == "Short":
    payoff = -payoff

# Plot payoffs (once again using the figures and axes for creating the plot)
fig, ax = plt.subplots()
ax.plot(S_range, payoff, label = f"{position} {type}")
ax.axhline(0, color = "black", linewidth = 1)
ax.axvline(K, color = "gray", linestyle = "--", label = "Strike Price")
ax.set_title("Option Payoff at Expiration")
ax.set_xlabel("Stock Price at Expiration ($)")
ax.set_ylabel("Profit / Loss ($)")
ax.legend()
st.pyplot(fig)







# CONVERGENCE PLOT (using Matplotlib)!!!
st.subheader("Binomial vs Black–Scholes Convergence")
st.write(
    "This visualization shows how the Binomial option price converges "
    "to the Black–Scholes price as the number of steps in the binomial tree increases."
)
steps_list = [2, 4, 8, 16, 32, 64, 128, 256, 512]
# Here, I calculate the binomial price based on the number of steps and store it in a list
bino_prices = [
    # To avoid the positional argument follows keyword argument error
    binomial_price(S = S, K = K, r = r, T = T, sigma = sigma, steps = s, type = type, american = False)
    for s in steps_list
]

# Compute Black-Scholes price (European call only for comparison) 
# NOTE: These are the ONLY DIFFERENT LINES OF CODE compared to the Convergence Plot with Black Scholes
if type == "Call":
    bs_price = call_price(S, K, r, T, sigma)
else:
    bs_price = put_price(S, K, r, T, sigma)   # 

# Instead of using plt for everything I ran the line of code below bc otherwise Streamlit would be confused
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(steps_list, bino_prices, marker = "o", label = "Binomial Prices (European)")
ax.axhline(bs_price, linestyle = "--", label = "Black Scholes Price")
ax.set_xscale("log", base = 2) # Reminder that options distribution is Logarithmic!
ax.set_xlabel("Binomial Steps") 
ax.set_ylabel(f"{type} Price ($)")
ax.set_title("Convergence of Binomial Price to Black–Scholes")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.info(
    "As the number of steps in the binomial tree increases, "
    "the Binomial model price converges to the Black–Scholes price. "
    "This is because the binomial approach approximates the continuous-time "
    "process assumed in Black–Scholes. "
    "Note: The x-axis is scaled by log2 because an options distribution "
    "is logarithmic (browse the internet if you're curious why). "
)



