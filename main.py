from configparser import ConfigParser, ExtendedInterpolation
import yfinance as yf

# initiate configuration
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('configuration.ini')

root_folder = config['general']['root_folder']
test_extension = config['general']['test_extension']

# obtain market data from yahoo finance
apple = yf.Ticker("aapl")
