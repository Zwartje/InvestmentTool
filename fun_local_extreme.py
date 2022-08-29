import numpy as np
import pandas as pd


def obtain_historical_window(data_series, window_in_days):
    """
    this function generates the data frame that rolls the historical price backward and forward by the number of window.
    An illustration is given as below with price column represented by column :math:`t`, and window_in_days is 2:

    +------------+-----+-----+---+-----+-----+
    | date       | t-2 | t-1 | t | t+1 | t+2 |
    +============+=====+=====+===+=====+=====+
    | 2020-01-01 | NA  | NA  | 1 | 2   | 3   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-02 | NA  | 1   | 2 | 3   | 4   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-03 | 1   | 2   | 3 | 4   | 5   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-04 | 2   | 3   | 4 | 5   | 6   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-05 | 3   | 4   | 5 | 6   | 7   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-06 | 4   | 5   | 6 | 7   | 8   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-07 | 5   | 6   | 7 | 8   | 9   |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-08 | 6   | 7   | 8 | 9   | NA  |
    +------------+-----+-----+---+-----+-----+
    | 2020-01-09 | 7   | 8   | 9 | NA  | NA  |
    +------------+-----+-----+---+-----+-----+

    :param data_series: the price of interest to find the local extremes. Note that it can only contain a single column
    with numerical values, with the index being a datetime series with format 'yyyy-mm-dd'
    :param window_in_days: the 2-sided horizon length
    :return: returns a dataframe with the historical price and its rolling window as above
    """

    number_of_dates = len(data_series)
    stock_price_window = data_series.rename(columns={data_series.columns[0]: "t"}, errors="raise")
    if window_in_days < number_of_dates:
        for i in range(-window_in_days, window_in_days + 1):
            if i < 0:
                column_name = 't-' + str(-i)
                stock_price_window.loc[:, column_name] = np.NaN
                stock_price_window.loc[stock_price_window.index[-i:number_of_dates], column_name] = \
                    stock_price_window.loc[stock_price_window.index[0:number_of_dates + i], 't'].tolist()
            elif i > 0:
                column_name = 't+' + str(i)
                stock_price_window.loc[:, column_name] = np.NaN
                stock_price_window.loc[stock_price_window.index[0:number_of_dates - i], column_name] = \
                    stock_price_window.loc[stock_price_window.index[i:number_of_dates], 't'].tolist()
    else:
        raise Exception(
            "The number of dates is " + str(number_of_dates) + " which is not as long as the length of window: "
            + str(window_in_days) + ". The run is aborted.")
    return stock_price_window


def find_local_minimum(data_series, window_in_days):
    """
    This type of local minimum is motivated from the very basic way of defining local extremes by visual inspection.
    Given a horizon H, at any time t, one can look for the local min as the minimum within the time interval [t-H, t+H]:

    +------------+-----+-----+---+-----+-----+-----------+
    | date       | t-2 | t-1 | t | t+1 | t+2 | local_min |
    +============+=====+=====+===+=====+=====+===========+
    | 2020-01-01 | NA  | NA  | 1 | 2   | 3   | 1         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-02 | NA  | 1   | 2 | 3   | 4   | 1         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-03 | 1   | 2   | 3 | 4   | 5   | 1         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-04 | 2   | 3   | 4 | 5   | 6   | 2         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-05 | 3   | 4   | 5 | 6   | 7   | 3         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-06 | 4   | 5   | 6 | 7   | 8   | 4         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-07 | 5   | 6   | 7 | 8   | 9   | 5         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-08 | 6   | 7   | 8 | 9   | NA  | 6         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-09 | 7   | 8   | 9 | NA  | NA  | 7         |
    +------------+-----+-----+---+-----+-----+-----------+

    .. math::

        RPmin_{t, H} = min_s\{S_s | s\in[t-H, t+H]\}

    If s happens to be equal to t, then :math:`S_t` is called a plain local min.

    :param data_series: the price of interest to find the local extremes.
    :param window_in_days: the 2-sided horizon length
    :return: pl_min: the location (i.e. date & price) of the plain local minimums.
    """

    historical_price_window = obtain_historical_window(data_series, window_in_days)
    local_minimum = historical_price_window.min(axis=1)

    return local_minimum


def find_local_maximum(data_series, window_in_days):
    """
    This type of local maximum is motivated from the very basic way of defining local extremes by visual inspection.
    Given a horizon H, at any time t, one can look for the local max as the maximum within the time interval [t-H, t+H]:

    +------------+-----+-----+---+-----+-----+-----------+
    | date       | t-2 | t-1 | t | t+1 | t+2 | local_max |
    +============+=====+=====+===+=====+=====+===========+
    | 2020-01-01 | NA  | NA  | 1 | 2   | 3   | 3         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-02 | NA  | 1   | 2 | 3   | 4   | 4         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-03 | 1   | 2   | 3 | 4   | 5   | 5         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-04 | 2   | 3   | 4 | 5   | 6   | 6         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-05 | 3   | 4   | 5 | 6   | 7   | 7         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-06 | 4   | 5   | 6 | 7   | 8   | 8         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-07 | 5   | 6   | 7 | 8   | 9   | 9         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-08 | 6   | 7   | 8 | 9   | NA  | 9         |
    +------------+-----+-----+---+-----+-----+-----------+
    | 2020-01-09 | 7   | 8   | 9 | NA  | NA  | 9         |
    +------------+-----+-----+---+-----+-----+-----------+

    .. math::

        RPmax_{t, H} = max_s\{S_s | s\in[t-H, t+H]\}

    If s happens to be equal to t, then :math:`S_t` is called a plain local max.

    :param data_series: the price of interest to find the local extremes.
    :param window_in_days: the 2-sided horizon length
    :return: local_max: the location (i.e. date & price) of the plain local maximums.
    """

    historical_price_window = obtain_historical_window(data_series, window_in_days)
    local_maximum = historical_price_window.max(axis=1)
    return local_maximum


def supplement_extremes(data_series, local_minimum, local_maximum):

    is_local_minimum = (data_series.iloc[:, 0] == local_minimum)
    is_local_maximum = (data_series.iloc[:, 0] == local_maximum)
    is_local_extreme = is_local_minimum | is_local_maximum

    data_series['local_minimum'] = local_minimum
    data_series['local_maximum'] = local_maximum
    data_series['is_local_minimum'] = is_local_minimum
    data_series['is_local_maximum'] = is_local_maximum
    data_series['is_local_extreme'] = is_local_extreme


def calculate_return_between_nearest_local_minimum_and_maximum(data_series, local_minimum, local_maximum):
    """
    The return can be categorized into 2 types: a loss (local maximum->local minimum) and a gain (local minimum->local
    maximum).

    The uniqueness of local maximum and minimum is required, i.e. there shouldn't be more than 1 local minimum
    between 2 local maximum, and vice versa.

    The implementation is summarized as below:

    +------------+-------+------------+------------+-------------+--------+----------------+
    | date       | Close | is_minimum | is_maximum | return_type | return | number_of_days |
    +============+=======+============+============+=============+========+================+
    | 2020-01-01 | 1     | True       | False      | loss        | Nan    | Nan            |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-02 | 2     | False      | True       | gain        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-03 | 3     | True       | False      | loss        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-04 | 4     | False      | True       | gain        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-05 | 5     | True       | False      | loss        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-06 | 6     | False      | True       | gain        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-07 | 7     | True       | False      | loss        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-08 | 8     | False      | True       | gain        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+
    | 2020-01-09 | 9     | True       | False      | loss        | 1      | 1              |
    +------------+-------+------------+------------+-------------+--------+----------------+

    :param data_series: the price of interest to find the local extremes.
    :param local_minimum: local minimum.
    :param local_maximum: local maximum.
    :return: return the unique extreme values and the return between 2 nearest extreme values.
    """
    is_local_minimum = (data_series.iloc[:, 0] == local_minimum)
    is_local_maximum = (data_series.iloc[:, 0] == local_maximum)
    is_local_extreme = is_local_minimum | is_local_maximum

    extreme_summary = pd.DataFrame(data=data_series.iloc[:, 0])
    extreme_summary['local_minimum'] = local_minimum
    extreme_summary['local_maximum'] = local_maximum
    extreme_summary['is_local_minimum'] = is_local_minimum
    extreme_summary['is_local_maximum'] = is_local_maximum
    extreme_summary['is_local_extreme'] = is_local_extreme
    extreme_summary = extreme_summary[extreme_summary['is_local_extreme']]
    number_of_dates = len(extreme_summary)
    extreme_summary['is_local_minimum_previous'] = extreme_summary['is_local_minimum'].shift(1)
    extreme_summary['is_not_duplicate'] = (
                extreme_summary['is_local_minimum'] != extreme_summary['is_local_minimum_previous'])
    # extreme_summary = extreme_summary[extreme_summary['is_not_duplicate']]
    extreme_summary['extreme_return'] = extreme_summary.iloc[:, 0].pct_change()
    extreme_summary.loc[extreme_summary['is_local_minimum'] == True, 'extreme_return_type'] = 'loss'
    extreme_summary.loc[extreme_summary['is_local_maximum'] == True, 'extreme_return_type'] = 'gain'
    extreme_summary['number_of_days'] = pd.to_datetime(extreme_summary.index).to_series().diff().dt.days
    return extreme_summary

