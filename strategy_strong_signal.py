import math

import numpy as np

import helpers


def verify_strong_signal_type(list_of_quotes, list_of_RSI_quotes, todays_quote, percentage_change,
                              list_of_quotes_from_delay_in_trading, yesterdays_rsi, option_premium_price, mult_upside,
                              RSI_threshold_regular):
    signal_call_percentil = 77
    signal_put_percentil = 23
    # RSI_floor_percentil=15
    # RSI_ceiling_percentil=85 #Ive reduced RSI by 5% from 95 to 90 and from 5 to 10

    daily_returns_list = helpers.covert_string_quotes_into_returns(list_of_quotes)
    signal_call = np.percentile(daily_returns_list, signal_call_percentil)
    signal_put = np.percentile(daily_returns_list, signal_put_percentil)

    list_of_RSI_quotes = convert_into_float(list_of_RSI_quotes)
    # RSI_floor=np.percentile(list_of_RSI_quotes,RSI_floor_percentil)
    # RSI_ceiling=np.percentile(list_of_RSI_quotes,RSI_ceiling_percentil)
    RSI_floor = RSI_threshold_regular
    RSI_ceiling = 100 - RSI_threshold_regular
    strong_signal_trx = 0
    if percentage_change > signal_call:  # scenario for possible call option
        max_in_list_of_quotes_from_delay_in_trading = float(max(list_of_quotes_from_delay_in_trading))
        upside_space = math.log(max_in_list_of_quotes_from_delay_in_trading / todays_quote)
        if (RSI_floor >= yesterdays_rsi) and (upside_space >= mult_upside * option_premium_price):
            strong_signal_trx = 1
    elif percentage_change < signal_put:
        min_in_list_of_quotes_from_delay_in_trading = float(min(list_of_quotes_from_delay_in_trading))
        upside_space = -math.log(min_in_list_of_quotes_from_delay_in_trading / todays_quote)
        if (yesterdays_rsi >= RSI_ceiling) and (upside_space >= mult_upside * option_premium_price):
            strong_signal_trx = 1
    return strong_signal_trx


def convert_into_float(list_quotes):
    float_list = []
    for el in range(1, len(list_quotes), 1):
        float_list.append(float(list_quotes[el]))
    float_list = np.asarray(float_list)
    return float_list
