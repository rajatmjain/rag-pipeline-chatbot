import yfinance as yf
import pandas as pd

# Define the ticker symbol for Gold Futures
tickerSymbol = "GC=F"

# Create a yfinance object for the Gold ticker symbol
goldData = yf.Ticker(tickerSymbol)

# Fetch historical data
historicalData = goldData.history(period="max")
df = pd.DataFrame(historicalData)

# Data cleaning
df = df.drop(columns=["Dividends","Stock Splits"])

# Save data
df.to_csv("data/historicPrices.csv")