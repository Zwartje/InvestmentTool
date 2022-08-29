# This version: 22/08/2022
# This file contains functions that streamlines data from a.o.
#   -- Investing.com, where financial data has to be downloaded manually;
#   -- stlouisfed.org, where economic data are downloaded manually for the moment.

# imports
import os
import pandas as pd


def read_investing_data(file_path):
    """
    For the moment the financial data from investing.com are downloaded manually into the data folder.
    :param file_path: the name of the file of interest, with the file extension (e.g. .csv).
    :return: the data series with a single column of numerical values as prices and a datetime index with format 'yyyy-
    mm-dd'.
    """

    data_file = os.path.abspath(os.path.join(file_path))
    data_df = pd.read_csv(data_file, index_col='Date', thousands=',')
    # data_df['Date'] = pd.to_datetime(data_df.index, format='%b %d, %Y', utc=True).strftime('%Y-%m-%d')
    data_df['Date'] = pd.to_datetime(data_df.index, format='%b %d, %Y', utc=True)
    data_df.set_index('Date', inplace=True)
    data_df.sort_index(inplace=True)

    return data_df

