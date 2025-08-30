# Option Pricing App

Hi, I'm Takeshi! I'm an incoming sophomore at Northwestern University studying Data Science and Mathematics. This project is my journey into quantitative finance. 

Throughout this Summer (2025), taking advantage of many available free resources online, I've self-taught myself basic options theory, along with data visualization and analysis skills with Python (numpy, pandas, matplotlib, seaborn). Combining that with my prior knowledge of statistics & probability, during the final three weeks before my sophomore year begins, I’ll be putting my newfound skills to the test by building an interactive website app that implements three classic option pricing models. The models are as follows:

- Black-Scholes (European Options)
- Binomial Tree (European & American Options)
- Monte Carlo Simulation (European Options)

## Project Structure
- `models/` —> pricing model implementations (`black_scholes.py`, `binomial.py`, `monte_carlo.py`)
- `tests/` —> unit tests to verify correctness
- `notebooks/` —> Jupyter notebooks for exploration and visualization
- `app/` —> Streamlit app for interactivity

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   .\.venv\Scripts\Activate.ps1 # Windows PowerShell