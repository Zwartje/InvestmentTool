def reflection_min(price, window_in_days, start_date, end_date):
    """
    This type of local minimum is motivated from the very basic way of defining local extremes by visual inspection.
    Given a horizon H, at any time t, one can look for the local min as the minimum within the time interval [t-H, t+H]:

    .. math::

        RPmin_{t, H} = min_s\{S_s | s\in[t-H, t+H]\}

    If s happens to be equal to t, then :math:`S_t` is called a plain local min.

    :param price: the price of interest to find the local extremes.
    :param window_in_days: the one-sided horizon length
    :param start_date: the start date of the price history. If left empty then the price from the very beginning will be used.
    :param end_date: the end date of the price history. If left empty then the price until the most recent will be used.
    :return: pl_min: the location (i.e. date & price) of the plain local minimums.
    """
    test = price + window_in_days
    return RP_min

def reflection_max(price, window_in_days, start_date, end_date):
    """
    This type of local maximum is motivated from the very basic way of defining local extremes by visual inspection.
    Given a horizon H, at any time t, one can look for the local max as the maximum within the time interval [t-H, t+H]:

    .. math::

        RPmax_{t, H} = max_s\{S_s | s\in[t-H, t+H]\}

    If s happens to be equal to t, then :math:`S_t` is called a plain local max.

    :param price: the price of interest to find the local extremes.
    :param window_in_days: the one-sided horizon length
    :param start_date: the start date of the price history. If left empty then the price from the very beginning will be used.
    :param end_date: the end date of the price history. If left empty then the price until the most recent will be used.
    :return: pl_max: the location (i.e. date & price) of the plain local maximums.
    """
    test = price + window_in_days
    return RP_max