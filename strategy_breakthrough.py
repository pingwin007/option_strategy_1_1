import math

import helpers


def verify_breakthrough(position_in_dates, todays_quote, yesterdays_quote, percentage_change, option_premium_bm,
                        selected_title, adj_option_premium_ratio, list_of_quotes_from_delay_in_trading,
                        option_sensitivity_to_strike, multiple_of_one_deal, days_delay_in_trading, option_premium_price,
                        mult_upside, mult_breakthrough, list_of_quotes):
    col_close, _, _, _ = helpers.get_cols_for_stock(selected_title)

    breakthrough_trx = 0
    if percentage_change >= 0:  # scenario for possible call option
        max_in_list_of_quotes_from_delay_in_trading = float(max(list_of_quotes_from_delay_in_trading))
        counter = 0
        for element_in_list in range(len(list_of_quotes_from_delay_in_trading), 0, -1):
            counter = counter + 1
            element_t = float(list_of_quotes_from_delay_in_trading[element_in_list - 1])
            element_t_minues_one = float(list_of_quotes_from_delay_in_trading
                                         [element_in_list - 2])
            if element_t < element_t_minues_one:
                quote_where_trend_starts = element_t
                break
        list_of_quotes_from_delay_in_trading = list_of_quotes[(position_in_dates - days_delay_in_trading):(
                position_in_dates - counter)]
        max_in_list_of_quotes_from_delay_in_trading = float(max(list_of_quotes_from_delay_in_trading))
        breakthrough_in_pr = math.log(todays_quote / max_in_list_of_quotes_from_delay_in_trading)
        if (breakthrough_in_pr >= mult_breakthrough * option_premium_price) and (
                todays_quote > max_in_list_of_quotes_from_delay_in_trading):
            breakthrough_trx = 1
    elif percentage_change < 0:  # scenario for possible put option
        min_in_list_of_quotes_from_delay_in_trading = float(min(list_of_quotes_from_delay_in_trading))
        counter = 0
        for element_in_list in range(len(list_of_quotes_from_delay_in_trading), 0, -1):
            counter = counter + 1
            element_t = float(list_of_quotes_from_delay_in_trading[element_in_list - 1])
            element_t_minues_one = float(list_of_quotes_from_delay_in_trading[element_in_list - 2])
            if element_t > element_t_minues_one:
                quote_where_trend_starts = element_t
                break
        list_of_quotes_from_delay_in_trading = list_of_quotes[(position_in_dates - days_delay_in_trading):(
            # PROBLEMATIC: counter
                position_in_dates - counter)]
        min_in_list_of_quotes_from_delay_in_trading = float(min(list_of_quotes_from_delay_in_trading))
        breakthrough_in_pr = -math.log(todays_quote / min_in_list_of_quotes_from_delay_in_trading)
        if breakthrough_in_pr >= mult_breakthrough * option_premium_price and (
                todays_quote < min_in_list_of_quotes_from_delay_in_trading):
            breakthrough_trx = 1
    return breakthrough_trx
