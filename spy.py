import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the ticker symbol and date range
ticker_symbol = input("Enter a stock ticker: ")
# ticker_symbol = "GOOGL"

# Calculate the end date as the current date
end_date = datetime.now()

# Calculate the start date as one year ago from the end date
start_date = end_date - timedelta(days=5000)

# Fetch historical data for the past year
data = yf.download(ticker_symbol, start=start_date,
                   end=end_date.strftime("%Y-%m-%d"))

# Calculate the 200-day moving average for the past year
data['200_MA'] = data['Close'].rolling(window=200).mean()

# Determine if the closing price is above or below the 200-day moving average
data['Above_200_MA'] = data['Close'] > data['200_MA']

# Create a Matplotlib figure
plt.figure(figsize=(12, 6))

# Plot closing prices
plt.plot(data.index, data['Close'], label='Closing Price', alpha=0.7)

# Plot the 200-day moving average for the past year
plt.plot(data.index, data['200_MA'],
         label='200-day MA', linestyle='--', alpha=0.7)

# Highlight buy (above MA) and sell (below MA) signals for the past year
plt.fill_between(data.index, data['Close'], data['200_MA'],
                 where=data['Above_200_MA'], facecolor='green', alpha=0.3, label='Buy Signal')
plt.fill_between(data.index, data['Close'], data['200_MA'], where=~
                 data['Above_200_MA'], facecolor='red', alpha=0.3, label='Sell Signal')

# Add a legend
plt.legend()

# Customize the plot
plt.title(f"{ticker_symbol} Price and 200-day Moving Average (Past Year)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)

# Determine the current position relative to the moving average
print(f"Ticker: {ticker_symbol}")
if data['Above_200_MA'].iloc[-1]:
    print("Above moving average, BUY")
else:
    print("Below moving average, SELL")

# Calculate the number of days since the last crossover for the past year
cross_over_date = data[data['Above_200_MA'] !=
                       data['Above_200_MA'].shift(1)].index[-1]
days_since_last_crossover = (end_date - cross_over_date).days

# Show the plot
plt.show()
