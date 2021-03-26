import numpy as np

def obtain_historical_window(stock_price_history_close, window_in_days):
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
    :return: returns a dataframe with the historical price and its rolling window as above
    """
    number_of_dates = len(stock_price_history_close)
    stock_price_window = stock_price_history_close.rename(columns={"Close": "t"}, errors="raise")
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


def find_local_minimum(price, window_in_days):
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
    :return: pl_min: the location (i.e. date & price) of the plain local minimums.
    """

    historical_price_window = obtain_historical_window(price, window_in_days)
    local_minimum = historical_price_window.min(axis=1)
    return local_minimum


def find_local_maximum(price, window_in_days):
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
    :return: local_max: the location (i.e. date & price) of the plain local maximums.
    """

    historical_price_window = obtain_historical_window(price, window_in_days)
    local_maximum = historical_price_window.max(axis=1)
    return local_maximum


