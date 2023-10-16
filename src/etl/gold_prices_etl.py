import os
import yfinance as yf
import pandas as pd
import sqlite3

def connectToDatabase(databasePath):
    return sqlite3.connect(databasePath)

def createYFinanceObject(tickerSymbol):
    return yf.Ticker(tickerSymbol)

def extractData(yFinanceObject, databaseConnection):
    tableNameQuery = "SELECT name FROM sqlite_master WHERE type='table';"
    tableExists = "gold_prices" in pd.read_sql_query(tableNameQuery, databaseConnection)["name"].values

    if not tableExists:
        # If the table doesn't exist, get all historic data
        historicData = yFinanceObject.history(period="max")
        historicData.to_csv("data/temp.csv")
    else:
        # Get the last date in the existing data
        lastDateQuery = "SELECT MAX(Date) FROM gold_prices"
        lastDateStr = pd.read_sql_query(lastDateQuery, databaseConnection)["MAX(Date)"][0]
        lastDate = pd.to_datetime(lastDateStr)

        # Calculate the date for the offset (e.g., 1 day)
        offsetDate = lastDate + pd.DateOffset(days=1)

        # Convert the offset date back to a string
        offsetDateStr = offsetDate.strftime('%Y-%m-%d')

        # Get new data starting from the offset date
        newData = yFinanceObject.history(start=offsetDateStr)
        newData.to_csv("data/temp.csv")

def cleanDataAndSaveToDb(databaseConnection):
    df = pd.read_csv("data/temp.csv")
    df = df.drop(columns=["Dividends", "Stock Splits"])
    df.to_sql("gold_prices", databaseConnection, if_exists="append", index=False)

def closeDatabaseConnection(databaseConnection):
    databaseConnection.close()

def deleteTempFile():
    os.remove("data/temp.csv")

def main():
    databasePath = "data/database.db"
    tickerSymbol = "GC=F"
    conn = connectToDatabase(databasePath)
    yFinanceObject = createYFinanceObject(tickerSymbol)

    extractData(yFinanceObject, conn)
    cleanDataAndSaveToDb(conn)
    closeDatabaseConnection(conn)
    deleteTempFile()

if __name__ == "__main__":
    main()