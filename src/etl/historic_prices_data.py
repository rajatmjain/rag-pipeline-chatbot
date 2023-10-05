import yfinance as yf
import pandas as pd
import sqlite3

# Define the ticker symbol for Gold Futures
tickerSymbol = "GC=F"

# Create a yfinance object for the Gold ticker symbol
goldData = yf.Ticker(tickerSymbol)

# Fetch historical data
historicalData = goldData.history(period="max")
df = pd.DataFrame(historicalData)

# Data cleaning
df = df.drop(columns=["Dividends", "Stock Splits"])

# Connect to the SQLite database
conn = sqlite3.connect("data/historic_prices.db")

# Save the DataFrame to the SQLite database
df.to_sql("historic_prices", conn, if_exists="replace", index=False)

# Close the database connection
conn.close()