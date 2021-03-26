from configparser import ConfigParser, ExtendedInterpolation
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import local_extreme

# read configuration
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('configuration.ini')

# obtain the historical stock price
ticker_name = config['ticker']['ticker_name']
stock_ticker = yf.Ticker(ticker_name)
stock_price_history = stock_ticker.history(start=config['parameter']['historical_price_start_date'],
                                           end=datetime.today().strftime('%Y-%m-%d'))
stock_price_history_close = pd.DataFrame(data=stock_price_history['Close'], index=stock_price_history.index)

# obtain local extremes
local_extreme_window = int(config['local_extreme']['historical_window'])
ticker_name
test = local_extreme.obtain_historical_window(stock_price_history_close, local_extreme_window)
local_minimum = local_extreme.find_local_minimum(stock_price_history_close, local_extreme_window)
local_maximum = local_extreme.find_local_maximum(stock_price_history_close, local_extreme_window)
plt.plot(stock_price_history['Close'])
plt.plot(local_minimum)
plt.plot(local_maximum)
plt.legend(["historical", "local minimum, window: " + str(local_extreme_window), "local maximum, window: " +
            str(local_extreme_window)], loc="upper left")
plt.title(ticker_name)
plt.show(block=False)

