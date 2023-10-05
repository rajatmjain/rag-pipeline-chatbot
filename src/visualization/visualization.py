import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Fetch data
df = pd.read_csv("data/historicPrices.csv")
weeklyData = df.tail(n=7)
last52WeeksData = df.tail(n=52 * 7)

# Convert the "Date" column to a datetime object
df["Date"] = pd.to_datetime(df["Date"])

# Weekly Stats
weeklyStats = weeklyData.describe()
weeklyOpenMax = weeklyStats["Open"]["max"]
weeklyCloseMax = weeklyStats["Close"]["max"]
print("\nWeekly Stats \n", weeklyStats)

# Create a new figure for the weekly plot
plt.figure(figsize=(10, 5))  # Adjust the figure size
plt.plot(weeklyData["Date"], weeklyData["Open"])
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Format date labels to display only the date without time
date_format = DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_formatter(date_format)
plt.savefig("src/products/weekly_plot.png")  # Save the weekly plot

# Clear the figure
plt.clf()

# Last 52 Week Statistics
last52WeeksStats = last52WeeksData.describe()
last52WeeksOpenMax = last52WeeksStats["Open"]["max"]
last52WeeksCloseMax = last52WeeksStats["Close"]["max"]
print("\nLast 52 Weeks Data \n", last52WeeksStats)

# Create a new figure for the last 52 weeks plot
plt.figure(figsize=(15, 5))  # Adjust the figure size
plt.plot(last52WeeksData["Date"], last52WeeksData["Open"])
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Format date labels to display only the date without time
plt.gca().xaxis.set_major_formatter(date_format)
plt.savefig("src/products/last_52_weeks_plot.png")  # Save the last 52 weeks plot


# Clear the figure
plt.clf()
