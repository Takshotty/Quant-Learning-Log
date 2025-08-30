import streamlit as st

st.title("Tak's Interactive Option Pricer")
st.subheader("Best viewed on laptop/desktop (not optimized for mobile)")

st.write("""
This web app demonstrates two fundamental option pricing models: 
- The **Black–Scholes** Model
    - Calculates option prices using a formula based on stock price, time, volatility, and interest rates.
    - Best for European options that can only be exercised at expiration.
- The **Binomial Tree** Model
    - Estimates option prices by simulating step-by-step stock price movements in a tree.
    - Flexible for European and American options that can be exercised early.

Use the sidebar to navigate between pages. Enjoy!
""")

