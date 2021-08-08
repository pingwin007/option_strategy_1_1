import math


def verify_resistance_transaction_type(open_positions_pf, financial_properties_df, position_in_dates,
                                       todays_quote, yesterdays_quote, percentage_change, option_premium_bm,
                                       selected_title, adj_option_premium_ratio, list_of_quotes_from_delay_in_trading,
                                       factor_remaining_time_value, option_duration_in_days,
                                       option_sensitivity_to_strike, multiple_of_one_deal, days_delay_in_trading,
                                       option_premium_price, mult_upside, list_of_quotes_trend_back):
    ceiling_adj = 0.0035 * adj_option_premium_ratio
    floor_adj = 0.006 * adj_option_premium_ratio
    drop_factor = 0.5
    # ceiling
    position_in_dates = position_in_dates + 1  # adjusting the position in excel file

    resistance_trx = 0
    if percentage_change > 0:  # scenario for possible put option
        max_in_list_of_quotes_from_delay_in_trading = float(max(list_of_quotes_from_delay_in_trading))
        tolerance_for_resistance = max_in_list_of_quotes_from_delay_in_trading * ceiling_adj
        if (todays_quote <= max_in_list_of_quotes_from_delay_in_trading) and (
                max_in_list_of_quotes_from_delay_in_trading - tolerance_for_resistance <= todays_quote):
            min_in_list_of_quotes_from_delay_in_trading = float(min(list_of_quotes_from_delay_in_trading))
            upside_space = -math.log(min_in_list_of_quotes_from_delay_in_trading / todays_quote)
            min_in_list_of_quotes_trend_back = float(min(list_of_quotes_trend_back))
            loss_in_trend = math.log(todays_quote / min_in_list_of_quotes_trend_back)
            if (upside_space >= mult_upside * option_premium_price) and (
                    loss_in_trend >= drop_factor * option_premium_price):
                resistance_trx = 1
    elif percentage_change <= 0:  # scenario for possible call option
        min_in_list_of_quotes_from_delay_in_trading = float(min(list_of_quotes_from_delay_in_trading))
        tolerance_for_resistance = min_in_list_of_quotes_from_delay_in_trading * floor_adj
        if (todays_quote >= min_in_list_of_quotes_from_delay_in_trading) and (
                tolerance_for_resistance + min_in_list_of_quotes_from_delay_in_trading >= todays_quote):
            # in above if 3 condition included (distance to resistance)
            # first condition - exists space
            max_in_list_of_quotes_from_delay_in_trading = float(max(list_of_quotes_from_delay_in_trading))
            upside_space = math.log(max_in_list_of_quotes_from_delay_in_trading / todays_quote)
            # second condition - the quote drop
            max_in_list_of_quotes_trend_back = float(max(list_of_quotes_trend_back))
            loss_in_trend = -math.log(todays_quote / max_in_list_of_quotes_trend_back)
            # check condition 1 & 2:
            if (upside_space >= mult_upside * option_premium_price) and (
                    loss_in_trend >= drop_factor * option_premium_price):
                resistance_trx = 1
    return resistance_trx


def check_transaction_type(resistance_code, percentage_change):  # unused!
    if resistance_code == 1:
        if percentage_change > 0:
            type_of_transaction = "put"
        else:
            type_of_transaction = "call"
    else:
        if percentage_change > 0:
            type_of_transaction = "call"
        else:
            type_of_transaction = "put"
    return type_of_transaction
