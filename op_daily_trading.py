import math

import numpy as np

import helpers


def verify_daily_trading_filled_at_closing(single_position, sign_of_option, adj_option_premium_ratio,
                                           daily_fluctuation_percentage, transaction_type, quote_struct):
    if transaction_type == 'call':
        quote_extremum = quote_struct.todays_hi
    elif transaction_type == 'put':
        quote_extremum = quote_struct.todays_lo
    absolute_difference_extremum_closing = sign_of_option * (quote_extremum - quote_struct.todays_close)
    absolute_fluctuation_value = adj_option_premium_ratio * daily_fluctuation_percentage * quote_extremum
    if absolute_difference_extremum_closing > absolute_fluctuation_value:
        daily_trading_filled_at_closing = 1
    else:
        daily_trading_filled_at_closing = 0
    return daily_trading_filled_at_closing


def verify_daily_trading_executed(list_of_quotes, transaction_type, quote_struct):
    daily_trading_executed = 0
    signal_call_percentil = 95
    signal_put_percentil = 5

    daily_returns_list = helpers.covert_string_quotes_into_returns(list_of_quotes)
    signal_call = np.percentile(daily_returns_list, signal_call_percentil)
    signal_put = np.percentile(daily_returns_list, signal_put_percentil)
    if transaction_type == 'call':
        quote_fluctuation = math.log(quote_struct.todays_hi / quote_struct.yesterdays_quote)
        if quote_fluctuation > signal_call:
            daily_trading_executed = 1
    elif transaction_type == 'put':
        quote_fluctuation = math.log(quote_struct.todays_lo / quote_struct.yesterdays_quote)
        if quote_fluctuation < signal_put:
            daily_trading_executed = 1
    return daily_trading_executed
