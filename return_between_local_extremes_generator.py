import os
from configparser import ConfigParser, ExtendedInterpolation
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import data_parser as dp
import fun_local_extreme

# read configuration
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('configuration.ini')

# folders
current_folder = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.abspath(os.path.join(current_folder, 'data'))
output_folder = os.path.abspath(os.path.join(current_folder, 'output'))
financial_folder = os.path.abspath(os.path.join(data_folder, 'financial'))
economic_folder = os.path.abspath(os.path.join(data_folder, 'economic'))

# obtain the historical stock price
ticker_name = config['ticker']['ticker_name']
price_type = config['parameter']['price_type']
data_file = os.path.abspath(os.path.join(financial_folder, ticker_name))
data_df = dp.fun_investing_data_reader(data_file)
stock_ticker = pd.DataFrame(data=data_df[price_type], index=data_df.index)
start_date = config['parameter']['historical_price_start_date']
end_date = datetime.today().strftime('%Y-%m-%d')
stock_ticker.sort_index(inplace=True)
stock_price_history = stock_ticker.truncate(before=start_date, after=end_date)
stock_price_history_close = pd.DataFrame(data=stock_price_history[price_type], index=stock_price_history.index)

# obtain local extremes and its location
local_extreme_window = int(config['local_extreme']['historical_window'])
test = fun_local_extreme.obtain_historical_window(stock_price_history_close, local_extreme_window)
local_minimum = fun_local_extreme.find_local_minimum(stock_price_history_close, local_extreme_window)
local_maximum = fun_local_extreme.find_local_maximum(stock_price_history_close, local_extreme_window)
is_local_minimum = (stock_price_history_close.iloc[:, 0] == local_minimum)
is_local_maximum = (stock_price_history_close.iloc[:, 0] == local_maximum)
extreme_summary = fun_local_extreme.calculate_return_between_nearest_local_minimum_and_maximum(stock_price_history_close,
                                                                                           local_minimum,
                                                                                           local_maximum)

# plot historical price and local extremes
plot_length = int(config['local_extreme']['plot_length'])
plot_width = int(config['local_extreme']['plot_width'])
plt.figure(figsize=(plot_length, plot_width))
plt.subplot(121)
local_minimum_dates = stock_price_history_close.index[is_local_minimum].tolist()
local_maximum_dates = stock_price_history_close.index[is_local_maximum].tolist()
# plt.plot(local_minimum, color='g')
# plt.plot(local_maximum, color='r')
plt.plot(stock_price_history.iloc[:, 0])
ax = plt.gca()
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
# ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m-%y'))
plt.xticks(rotation=45)

plt.legend(["historical", "local minimum, window: " + str(local_extreme_window), "local maximum, window: " +
            str(local_extreme_window)], loc="upper left")
for extreme_date in local_minimum_dates:
    plt.axvline(x=extreme_date, color='g', linestyle='--')
for extreme_date in local_maximum_dates:
    plt.axvline(x=extreme_date, color='r', linestyle='--')
plt.xlabel('date')
plt.ylabel('price')
# create a summary containing a summary of trend
plt.subplot(122)
trend_summary = extreme_summary[['number_of_days', 'extreme_return', 'extreme_return_type']].dropna()
for return_type in trend_summary['extreme_return_type'].unique():
    x_values = trend_summary.loc[trend_summary['extreme_return_type'] == return_type, 'number_of_days']
    y_values = trend_summary.loc[trend_summary['extreme_return_type'] == return_type, 'extreme_return']
    plt.scatter(x_values, y_values, label=return_type, alpha=0.3, edgecolors='none')
x_values = trend_summary['number_of_days']
y_values = trend_summary['extreme_return']
trend_line = np.polyfit(x_values, y_values, 1)
trend_line_function = np.poly1d(trend_line)
y_fitted_values = trend_line_function(x_values)
plt.plot(x_values, y_fitted_values, "k--")
plt.xlabel('number of days')
plt.ylabel('returns between 2 local extremes')
plt.legend()
plt.grid(True)
plt.suptitle(ticker_name + ' momentum return')
plt.savefig(output_folder + '\\' + ticker_name + '_return_between_2_extremes.png')
plt.show()