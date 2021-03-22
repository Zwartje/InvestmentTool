import yfinance as yf

stock_ticker = yf.Ticker("AAPL")
hist = stock_ticker.history(period="max")
hist['Close'].plot(title="Apple's stock price")

