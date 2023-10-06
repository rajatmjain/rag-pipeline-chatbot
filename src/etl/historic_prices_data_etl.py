import os
import yfinance as yf
import pandas as pd
import sqlite3

# Define the ticker symbol for Gold Futures
tickerSymbol = "GC=F"

# Connect to the SQLite database
conn = sqlite3.connect("data/historic_prices.db")

# Create a yfinance object for the Gold ticker symbol
goldData = yf.Ticker(tickerSymbol)

# Data Extraction
if "historic_prices" not in pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)["name"].values:
    # Get all historic data
    historicData = goldData.history(period="max")
    historicData.to_csv("data/temp.csv")
    df = pd.read_csv("data/temp.csv")
  
else:
    # Get the last date in the existing data
    query = "SELECT MAX(Date) FROM historic_prices"
    lastDateStr = pd.read_sql_query(query, conn)["MAX(Date)"][0][:10]
    lastDate = pd.to_datetime(lastDateStr)
    
    # Calculate the date for the offset (e.g., 1 day)
    offsetDate = lastDate + pd.DateOffset(days=1)
    
    # Convert the offset date back to a string
    offsetDateStr = offsetDate.strftime('%Y-%m-%d')
    
    # Get new data starting from the offset date
    newData = goldData.history(start=offsetDateStr)

    newData.to_csv("data/temp.csv")
    df = pd.read_csv("data/temp.csv")

    
# Data cleaning
df = df.drop(columns=["Dividends", "Stock Splits"])

# Save the DataFrame to the SQLite database
df.to_sql("historic_prices", conn, if_exists="append", index=False)

# Close the database connection
conn.close()

# Delete Temp file
os.remove("data/temp.csv")