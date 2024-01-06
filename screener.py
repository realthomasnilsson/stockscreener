# Stock screener that searches for stocks using screens developed by
# Minervini, Stockbee, and others.

import yfinance as yf
import pandas as pd

# Define a list of stock tickers to screen
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # You can add more tickers

# Define a function to check Minervini's criteria
def check_minervini_criteria(ticker):
    # Fetch historical data
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")

    # Calculate moving averages and other criteria
    hist['150MA'] = hist['Close'].rolling(window=150).mean()
    hist['200MA'] = hist['Close'].rolling(window=200).mean()
    hist['50MA'] = hist['Close'].rolling(window=50).mean()
    current_close = hist.iloc[-1]['Close']
    high_52week = hist['Close'].max()

    # Criteria checks
    within_25pct_52week_high = current_close >= 0.75 * high_52week
    above_150MA = current_close > hist.iloc[-1]['150MA']
    above_200MA = current_close > hist.iloc[-1]['200MA']
    ma_trend = (hist.iloc[-1]['50MA'] > hist.iloc[-1]['150MA'] > hist.iloc[-1]['200MA'])
    ma150_upward = hist['150MA'].iloc[-30] < hist['150MA'].iloc[-1]

    return all([within_25pct_52week_high, above_150MA, above_200MA, ma_trend, ma150_upward])

# Screen each stock
screen_results = {ticker: check_minervini_criteria(ticker) for ticker in tickers}

# Print the results
for ticker, passed in screen_results.items():
    print(f"{ticker}: {'Passed' if passed else 'Failed'}")

