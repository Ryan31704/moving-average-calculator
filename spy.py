import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the ticker symbol and date range
ticker_symbol = input("Enter a stock ticker: ")
years = input("How many years: ")
ma_days = input("How many day moving average: ")
# ticker_symbol = "GOOGL"

# Calculate the end date as the current date
end_date = datetime.now()

# Calculate the start date as one year ago from the end date
start_date = end_date - timedelta(days=int(years) * 365 + int(ma_days))

# Fetch historical data for the past year
data = yf.download(ticker_symbol, start=start_date,
                   end=end_date.strftime("%Y-%m-%d"))

# Calculate the 200-day moving average for the past year
data['MA'] = data['Close'].rolling(window=int(ma_days)).mean()

# Determine if the closing price is above or below the 200-day moving average
data['Above_MA'] = data['Close'] > data['MA']

# Create a Matplotlib figure
plt.figure(figsize=(12, 6))

# Plot closing prices
plt.plot(data.index[+ int(ma_days):], data['Close'][+ int(ma_days):],
         label='Closing Price', alpha=0.7)

# Plot the 200-day moving average for the past year
plt.plot(data.index, data['MA'], label=ma_days +
         '-day MA', linestyle='--', alpha=0.7)

# Highlight buy (above MA) and sell (below MA) signals for the past year
plt.fill_between(data.index, data['Close'], data['MA'],
                 where=data['Above_MA'], facecolor='green', alpha=0.3, label='Buy Signal')
plt.fill_between(data.index, data['Close'], data['MA'], where=~
                 data['Above_MA'], facecolor='red', alpha=0.3, label='Sell Signal')

# Add a legend
plt.legend()

# Customize the plot
plt.title(f"{ticker_symbol} Price and " + ma_days + "-day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)

# Determine the current position relative to the moving average
print(f"Ticker: {ticker_symbol}")
if data['Above_MA'].iloc[-1]:
    print("Above moving average, BUY")
else:
    print("Below moving average, SELL")
# Calculate the number of days since the last crossover for the past year
cross_over_date = data[data['Above_MA'] != data['Above_MA'].shift(1)].index[-1]
days_since_last_crossover = (end_date - cross_over_date).days
print(f"{days_since_last_crossover} days ago")


# Show the plot
plt.show()
