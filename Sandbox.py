import os
import data_parser as dp
import pandas as pd
import fun_local_extreme

current_folder = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.abspath(os.path.join(current_folder, 'data'))
output_folder = os.path.abspath(os.path.join(current_folder, 'output'))
financial_folder = os.path.abspath(os.path.join(data_folder, 'financial'))
economic_folder = os.path.abspath(os.path.join(data_folder, 'economic'))

ticker_name = 'US 500 Cash Historical Data.csv'
data_file = os.path.abspath(os.path.join(financial_folder, ticker_name))
data_df = dp.read_investing_data(data_file)
stock_ticker = pd.DataFrame(data=data_df['Price'], index=data_df.index)

stock_ticker['Rolling_min'] = stock_ticker.Price.rolling(window=40, min_periods=20, center=True).min()
stock_ticker['Rolling_max'] = stock_ticker.Price.rolling(window=40, min_periods=20, center=True).max()
stock_ticker['is_min'] = (stock_ticker['Rolling_min'] == stock_ticker['Price'])
stock_ticker['is_max'] = (stock_ticker['Rolling_max'] == stock_ticker['Price'])
stock_ticker['is_extreme'] = stock_ticker.is_min | stock_ticker.is_max

# extreme_summary = fun_local_extreme.calculate_return_between_nearest_local_minimum_and_maximum(stock_price_history_close,
#                                                                                            local_minimum,
#                                                                                            local_maximum)

stock_ticker.loc[stock_ticker.loc['2006-05-04':'2006-06-04'].Price.idxmax()].is_max = True


