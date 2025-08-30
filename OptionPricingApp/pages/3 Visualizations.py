# Enable Python to find modules from the parent directory (OptionPricingApp)
import sys, os
sys.path.append(os.path.abspath(".."))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Import both Black Scholes models as well as the Binomial Model (for Convergence visualization)
# Also import the greeks for the greeks visualization
from models.black_scholes import call_price, put_price, greeks
from models.binomial import binomial_price

# Page Introduction
st.title("Option Pricing Visualizations")
st.write("""
This page provides **visualizations** to better understand how option prices behave.
Explore the interactive heatmaps and comparisons between models!
""")

# Sidebar: I will allow the user to select the option type as well as visualization
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
visualization = st.sidebar.selectbox("Choose Visualization", ["K vs. σ Heatmap", "Greeks Visualization"])

# Shared parameters for both visualizations
S = st.sidebar.number_input("Current Asset Price (S)", min_value = 0.01, value = 100.0)
K = st.sidebar.number_input("Strike Price (K)", min_value = 0.01, value = 100.0)
r = st.sidebar.slider("Risk-free Interest Rate (r)", 0.0, 0.1, 0.01, step = 0.005)
T = st.sidebar.slider("Time to Expiration (T in years)", 0.0, 5.0, 1.0, step = 0.1)
sigma = st.sidebar.slider("Volatility (σ)", 0.05, 1.0, 0.2, step=0.05)

# Heatmap
if visualization == "K vs. σ Heatmap":
    st.subheader(f"{option_type} Option Price Heatmap (Strike Price vs Volatility)")
    st.write("Note: The heatmap prices are determined by the Black-Scholes Model")

    K_values = np.linspace(K * 0.5, K * 1.5, 100)
    sigma_values = np.linspace(sigma * 0.5, sigma * 1.5, 100)
    # Create the numpy array of prices of 100x100 (to reflect size of K_values and sigma_values)
    # Note that I'm going to eventually fill in the array
    prices = np.zeros((len(sigma_values), len(K_values)))

    # I'm going to use the Black Scholes Model to determine heat map prices
    # Using enumerate to retrive both the index and the actual values in sigma_values and K_values
    for i, sigma in enumerate(sigma_values):
        for j, k in enumerate(K_values):
            if option_type == "Call":
                prices[i, j] = call_price(S, k, r, T, sigma)
            else:
                prices[i, j] = put_price(S, k, r, T, sigma)

    fig, ax = plt.subplots()
    # Creating heatmap using .imshow(name of array, bounding box (extent = [))
    c = ax.imshow(prices, 
                  # bounding box
                  extent = [K_values.min(), K_values.max(),
                                  sigma_values.min(), sigma_values.max()],
                  # make sure that the first index of the array [0, 0] is found on the bottom left
                  origin = "lower", 
                  # if I didn't have this line of code everything would be squashed (no clue why)
                  aspect = "auto",
                  # I decided to choose the Red, Yellow, Green color scheme (thought it was easiest to visualize) 
                  cmap = "RdYlGn")
    # This line maps my data values for my heatmap c (using prices for my values) to my chosen colorscheme RdYlGn
    fig.colorbar(c, ax = ax, label = "Option Price")
    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Volatility (σ)")
    ax.set_title(f"{option_type} Price Heatmap")
    st.pyplot(fig)

# GREEKS VISUALIZATION
else:
    st.subheader("Greeks Visualization")
    st.write("Scroll down to the bottom of the parameters to select which Greek you'd like to plot.")

    # Sidebar: Greek selection
    greek_choice = st.sidebar.selectbox(
        "Select Greek to Plot",
        ["Delta", "Gamma", "Theta", "Vega", "Rho"]
    )

    # Dictionary of Greek descriptions
    greek_descriptions = {
        "Delta": "Sensitivity of option price to underlying asset price (hedge ratio).",
        "Gamma": "Rate of change of Delta (convexity of option value).",
        "Theta": "Sensitivity of option price to time decay (time value erosion).",
        "Vega": "Sensitivity of option price to volatility (volatility exposure).",
        "Rho": "Sensitivity of option price to interest rate changes."
    }

    # Show description dynamically (after they choose the greek to plot)
    st.write(greek_choice, ": ", greek_descriptions[greek_choice])

    # Making a stock price range for plotting Greeks (I'm going to make this more modest)
    S_values = np.linspace(0.5 * K, 1.5 * K, 200)

    # Compute all Greeks across S_values
    all_greeks = [greeks(S, K, r, T, sigma) for S in S_values]

    # Extract chosen Greek
    greek_map = {
        "Delta": [g["delta"] for g in all_greeks],
        "Gamma": [g["gamma"] for g in all_greeks],
        "Theta": [g["theta"] for g in all_greeks],
        "Vega":  [g["vega"] for g in all_greeks],
        "Rho":   [g["rho"] for g in all_greeks],
    }
    greek_values = greek_map[greek_choice]

    # Plot chosen Greek
    fig, ax = plt.subplots()
    ax.plot(S_values, greek_values, label = greek_choice)
    ax.axhline(0, color = "black", linewidth = 1)
    ax.set_title(f"{greek_choice} vs Stock Price")
    ax.set_xlabel("Stock Price ($)")
    ax.set_ylabel(greek_choice)
    ax.legend()
    st.pyplot(fig)
