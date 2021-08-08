import math

import numpy as np

import helpers


def compute_transaction_value_in(entry_option_price, financial_properties_df, strong_signal_code,
                                 RSI_threshold_increased, yesterdays_rsi):
    bundle_size = 100
    boost_flag = 0
    if strong_signal_code == 1 and (
            (yesterdays_rsi < RSI_threshold_increased) or (yesterdays_rsi > (100 - RSI_threshold_increased))):
        multiplicator_for_strong_signal = 1.5
        boost_flag = 1
    else:
        multiplicator_for_strong_signal = 1
    last_financial_record = financial_properties_df[-1:]
    last_deal_size = float(last_financial_record["deal_size"])
    options_bundles_quantity = last_deal_size / (entry_option_price * bundle_size)
    options_bundles_quantity_rounded = math.ceil(options_bundles_quantity)
    transaction_value_in = options_bundles_quantity_rounded * bundle_size * entry_option_price * multiplicator_for_strong_signal
    return transaction_value_in, boost_flag


def verify_signal_type(todays_quote, percentage_change, list_of_quotes_from_delay_in_trading, option_premium_price,
                       mult_upside, list_of_quotes):
    # signal_call_percentil=87
    # signal_put_percentil=13

    signal_call_percentil = 77
    signal_put_percentil = 23

    daily_returns_list = helpers.covert_string_quotes_into_returns(list_of_quotes)
    signal_call = np.percentile(daily_returns_list, signal_call_percentil)
    signal_put = np.percentile(daily_returns_list, signal_put_percentil)
    signal_trx = 0
    if percentage_change > signal_call:  # scenario for possible call option
        max_in_list_of_quotes_from_delay_in_trading = float(max(list_of_quotes_from_delay_in_trading))
        upside_space = math.log(max_in_list_of_quotes_from_delay_in_trading / todays_quote)
        if (upside_space >= mult_upside * option_premium_price):
            signal_trx = 1
    elif percentage_change < signal_put:
        min_in_list_of_quotes_from_delay_in_trading = float(min(list_of_quotes_from_delay_in_trading))
        upside_space = -math.log(min_in_list_of_quotes_from_delay_in_trading / todays_quote)
        if (upside_space >= mult_upside * option_premium_price):
            signal_trx = 1
    return signal_trx


def compute_deal_size(last_deal_size, multiple_of_one_deal, last_balance):
    # increase_of_deal=500
    # upper_investment_threshold=last_balance/multiple_of_one_deal
    # factor=upper_investment_threshold // increase_of_deal
    new_deal_size = last_balance / multiple_of_one_deal
    # new_deal_size=increase_of_deal*factor
    # if new_deal_size<last_deal_size:
    #    new_deal_size=last_deal_size
    return new_deal_size


def verify_current_phase_of_opening(duration_in_days, first_exit_check, second_exit_check):
    if duration_in_days == first_exit_check:
        current_phase = 1
    elif duration_in_days == second_exit_check:
        current_phase = 2
    else:
        current_phase = 3
    return current_phase


def return_entry_type(resistance_code, strong_signal_code, signal_code, breakthrough_code):
    if strong_signal_code == 1:
        return "strong_signal"
    elif signal_code == 1:
        return "signal"
    elif resistance_code == 1:
        return "resistance"
    elif breakthrough_code == 1:
        return "breakthrough"
    else:
        raise RuntimeError
