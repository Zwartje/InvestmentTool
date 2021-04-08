import numpy as np
import pandas as pd


def obtain_historical_window(stock_price_history_close, window_in_days, price_type):
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


    :param stock_price_history_close: the price of interest to find the local extremes.
    :param window_in_days: the 2-sided horizon length
    :param price_type: the price type
    :return: returns a dataframe with the historical price and its rolling window as above
    """
    number_of_dates = len(stock_price_history_close)
    stock_price_window = stock_price_history_close.rename(columns={price_type: "t"}, errors="raise")
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


def find_local_minimum(price, window_in_days, price_type):
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

    :param price: the price of interest to find the local extremes.
    :param window_in_days: the 2-sided horizon length
    :param price_type: the price type
    :return: pl_min: the location (i.e. date & price) of the plain local minimums.
    """

    historical_price_window = obtain_historical_window(price, window_in_days, price_type)
    local_minimum = historical_price_window.min(axis=1)

    return local_minimum


def find_local_maximum(price, window_in_days, price_type):
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

    :param price: the price of interest to find the local extremes.
    :param window_in_days: the 2-sided horizon length
    :param price_type: the price type
    :return: local_max: the location (i.e. date & price) of the plain local maximums.
    """

    historical_price_window = obtain_historical_window(price, window_in_days, price_type)
    local_maximum = historical_price_window.max(axis=1)
    return local_maximum


def calculate_return_between_nearest_local_minimum_and_maximum(stock_price_history_close, local_minimum, local_maximum,
                                                               price_type):
    """
    The return can be catogorized into 2 types: a loss (local maximum->local minimum) and a gain (local minimum->local
    maximum).

    The uniqueness of local maximum and minimum is required, i.e. there shouldn't be more than 1 local minimum
    between 2 local maximum.

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

    :param stock_price_history_close: the price of interest to find the local extremes.
    :param local_minimum: local minimum.
    :param local_maximum: local minimum.
    :param price_type: price type.
    :return: return the unique extreme values and the return between 2 nearest extreme values.
    """
    is_local_minimum = (stock_price_history_close[price_type] == local_minimum)
    is_local_maximum = (stock_price_history_close[price_type] == local_maximum)
    is_local_extreme = is_local_minimum | is_local_maximum

    extreme_summary = pd.DataFrame(data=stock_price_history_close[price_type])
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
    extreme_summary = extreme_summary[extreme_summary['is_not_duplicate']]
    extreme_summary['extreme_return'] = extreme_summary[price_type].pct_change()
    extreme_summary.loc[extreme_summary['is_local_minimum'] == True, 'extreme_return_type'] = 'loss'
    extreme_summary.loc[extreme_summary['is_local_maximum'] == True, 'extreme_return_type'] = 'gain'
    extreme_summary['number_of_days'] = extreme_summary.index.to_series().diff().dt.days
    return extreme_summary

