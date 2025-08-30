# Enable Python to find modules from the parent directory (OptionPricingApp)
import sys, os
sys.path.append(os.path.abspath(".."))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# Import both Black Scholes models as well as the Binomial Model (for Convergence visualization)
from models.black_scholes import call_price, put_price
from models.binomial import binomial_price


# Explain to users what the purpose of this page is
st.title("Black–Scholes Pricing Model")
st.write("""
This page demonstrates the Black–Scholes option pricing model.
Feel free to play around with the parameters on the left! Explore
the effects of the parameters on the option price and the diagrams
below! Have fun :)
"""
)

# PARAMETER SLIDERS (except prices so the user can type in a number)!!!
st.sidebar.header("Black-Scholes Parameters")
type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
S = st.sidebar.number_input("Current Asset Price (S)", min_value = 0.01, value = 100.0)
K = st.sidebar.number_input("Strike Price (K)", min_value = 0.01, value = 100.0)
r = st.sidebar.slider("Risk-free Interest Rate (r)", 0.0, 0.1, 0.01, step = 0.005)
T = st.sidebar.slider("Time to Expiration (T in years)", 0.0, 5.0, 1.0, step = 0.1)
sigma = st.sidebar.slider("Volatility (σ)", 0.0, 1.0, 0.2, step = 0.01)
# The option type is binary so I used a drop down menu (selectbox instead of radio)

# Calculate & Display Black-Scholes Price
# Note: Since I made a separate function for call and put prices for BS, I need to use an if-else statement here:
if type == "Call":
    # Round to nearest Hundredth (since we want it in cents)
    bs_price = round(call_price(S, K, r, T, sigma), 2)
else:
    bs_price = round(put_price(S, K, r, T, sigma), 2)
# Displaying in bold (using **)
st.subheader(f"**{type} Option Price:** :yellow[${bs_price}]")






# PAYOFF DIAGRAM
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
    binomial_price(S, K, r, T, sigma, steps = s, type = "Call", american = False)
    for s in steps_list
]
# Instead of using plt for everything I ran the line of code below bc otherwise Streamlit would be confused
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(steps_list, bino_prices, marker = "o", label = "Binomial Prices (European)")
ax.axhline(bs_price, linestyle = "--", label = "Black Scholes Price")
ax.set_xscale("log", base = 2) # Reminder that options distribution is Logarithmic!
ax.set_xlabel("Binomial Steps") 
ax.set_ylabel("Call Price ($)") 
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

