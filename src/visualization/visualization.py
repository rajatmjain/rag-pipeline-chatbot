import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def connectToDatabase(databasePath):
    return sqlite3.connect(databasePath)

def fetchDataFromDatabase(conn, tableName):
    query = f"SELECT * from {tableName}"
    return pd.read_sql_query(query, conn)

def generateWeeklyPlot(df, outputPath):
    weeklyData = df.tail(n=7)

    # Convert the "Date" column to a datetime object
    df["Date"] = pd.to_datetime(df["Date"])


    # Weekly Stats
    weeklyStats = weeklyData.describe()
    weeklyOpenMax = weeklyStats["Open"]["max"]
    weeklyCloseMax = weeklyStats["Close"]["max"]
    
    # Create a new figure for the weekly plot
    plt.figure(figsize=(10, 5))  # Adjust the figure size
    plt.plot(weeklyData["Date"], weeklyData["Open"])
    plt.xticks(rotation=25,fontsize=10)  # Rotate x-axis labels for readability

    # Format date labels to display only the date without time
    date_format = DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.savefig(outputPath)  # Save the weekly plot

    # Clear the figure
    plt.clf()

def generateLast52WeeksPlot(df, outputPath):
    last52WeeksData = df.tail(n=52 * 7)

    # Last 52 Week Statistics
    last52WeeksStats = last52WeeksData.describe()
    last52WeeksOpenMax = last52WeeksStats["Open"]["max"]
    last52WeeksCloseMax = last52WeeksStats["Close"]["max"]

    # Create a new figure for the last 52 weeks plot
    plt.figure(figsize=(15, 5))  # Adjust the figure size
    plt.plot(last52WeeksData["Date"], last52WeeksData["Open"])
    plt.xticks(rotation=25,fontsize=10)  # Rotate x-axis labels for readability

    # Format date labels to display only the date without time
    date_format = DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.savefig(outputPath)  # Save the last 52 weeks plot

    # Clear the figure
    plt.clf()

def main():
    databasePath = "data/database.db"
    tableName = "gold_prices"
    outputPathWeekly = "public/weekly_plot.png"
    outputPathLast52Weeks = "public/last_52_weeks_plot.png"

    conn = connectToDatabase(databasePath)
    df = fetchDataFromDatabase(conn, tableName)

    generateWeeklyPlot(df, outputPathWeekly)
    generateLast52WeeksPlot(df, outputPathLast52Weeks)

    conn.close()

if __name__ == "__main__":
    main()
