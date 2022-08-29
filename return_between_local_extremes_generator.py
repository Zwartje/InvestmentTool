import os
from configparser import ConfigParser, ExtendedInterpolation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import data_parser as dp

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
data_df = dp.read_investing_data(data_file)
extreme_returns = pd.DataFrame(data=data_df[price_type], index=data_df.index)

# obtain local extremes and its location
local_extreme_window = int(config['local_extreme']['historical_window'])
extreme_returns['local_minimum'] = extreme_returns.Price.rolling(window=local_extreme_window * 2,
                                                                 min_periods=local_extreme_window, center=True).min()
extreme_returns['local_maximum'] = extreme_returns.Price.rolling(window=local_extreme_window * 2,
                                                                 min_periods=local_extreme_window, center=True).max()
extreme_returns['is_local_minimum'] = (extreme_returns['local_minimum'] == extreme_returns['Price'])
extreme_returns['is_local_maximum'] = (extreme_returns['local_maximum'] == extreme_returns['Price'])
extreme_returns['is_extreme'] = extreme_returns.is_local_minimum | extreme_returns.is_local_maximum
extreme_summary = extreme_returns[extreme_returns['is_extreme']]

# keep only the unique instance of extreme
# TODO add local algorithm to find the real extreme when multiple extremes are present
extreme_summary['is_local_minimum_previous'] = extreme_summary['is_local_minimum'].shift(1)
extreme_summary['is_local_maximum_previous'] = extreme_summary['is_local_maximum'].shift(1)
extreme_summary['is_duplicate_minimum'] = (
        extreme_summary['is_local_minimum'] == extreme_summary['is_local_minimum_previous'])
extreme_summary['is_duplicate_maximum'] = (
        extreme_summary['is_local_maximum'] == extreme_summary['is_local_maximum_previous'])
extreme_summary['is_not_duplicate'] = (~extreme_summary['is_duplicate_minimum']) & \
                                      (~extreme_summary['is_duplicate_maximum'])
extreme_summary_unique = extreme_summary[extreme_summary['is_not_duplicate']]

# calculate extreme return
extreme_summary_unique['extreme_return'] = extreme_summary.iloc[:, 0].pct_change()
extreme_summary_unique.loc[extreme_summary_unique['is_local_minimum'], 'extreme_return_type'] = 'loss'
extreme_summary_unique.loc[extreme_summary_unique['is_local_maximum'], 'extreme_return_type'] = 'gain'
extreme_summary_unique['number_of_days'] = pd.to_datetime(extreme_summary_unique.index).to_series().diff().dt.days

# plot historical price and local extremes
plot_length = int(config['local_extreme']['plot_length'])
plot_width = int(config['local_extreme']['plot_width'])
plt.figure(figsize=(plot_length, plot_width))
plt.subplot(121)
local_minimum_dates = extreme_summary_unique[extreme_summary_unique['is_local_minimum']].index.tolist()
local_maximum_dates = extreme_summary_unique[extreme_summary_unique['is_local_maximum']].index.tolist()
# plt.plot(local_minimum, color='g')
# plt.plot(local_maximum, color='r')
plt.plot(extreme_returns.iloc[:, 0])
ax = plt.gca()
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
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
trend_summary = extreme_summary_unique[['number_of_days', 'extreme_return', 'extreme_return_type']].dropna()
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
