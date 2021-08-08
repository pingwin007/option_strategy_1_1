import numpy as np

import helpers
import model_pricing
import model_trading
import my_data
import strategy_breakthrough
import strategy_resistance
import strategy_strong_signal


def open_positions(open_positions_pf, financial_properties_df, position_in_dates, percentage_change,
                   selected_title, curr_title_cfg, model_cfg, list_of_quotes, list_of_RSI_quotes,
                   list_of_quotes_from_delay_in_trading, quote_struct, dates):
    todays_quote, yesterdays_quote, yesterdays_rsi = quote_struct.todays_close, quote_struct.yesterdays_quote, quote_struct.yesterdays_rsi
    position_name, option_premium_price, first_exit_check, second_exit_check, call_in_scope, put_in_scope, resistance_in_scope, breakthrough_in_scope, strong_signal_in_scope, signal_in_scope, RSI_threshold_regular, RSI_threshold_increased, daily_trading_call_in_scope, daily_trading_put_in_scope \
        = my_data.extract_stock_cfg(curr_title_cfg)
    days_delay_in_trading, factor_remaining_time_value, mult_breakthrough, mult_upside, multiple_of_one_deal, option_duration_in_days, option_premium_bm, option_sensitivity_to_strike, return_threshold, selected_start_date, daily_fluctuation_percentage, early_termination_enabled, early_termination_threshold_return \
        = my_data.unpack_model_config(model_cfg)

    adj_option_premium_ratio = option_premium_price / option_premium_bm

    # below code function -> goes to seperate function of opening
    # -------------------------------------------------------------------------------------------------------------
    if resistance_in_scope == 1:

        resistance_code = strategy_resistance.verify_resistance_transaction_type(open_positions_pf,
                                                                                 financial_properties_df,
                                                                                 position_in_dates, todays_quote,
                                                                                 yesterdays_quote, percentage_change,
                                                                                 option_premium_bm, selected_title,
                                                                                 adj_option_premium_ratio,
                                                                                 list_of_quotes_from_delay_in_trading,
                                                                                 factor_remaining_time_value,
                                                                                 option_duration_in_days,
                                                                                 option_sensitivity_to_strike,
                                                                                 multiple_of_one_deal,
                                                                                 days_delay_in_trading,
                                                                                 option_premium_price, mult_upside, )
    else:
        resistance_code = 0
    # set of fix parameters -> if necessary change here
    if breakthrough_in_scope == 1:
        breakthrough_code = strategy_breakthrough.verify_breakthrough(position_in_dates, todays_quote, yesterdays_quote,
                                                                      percentage_change, option_premium_bm,
                                                                      selected_title, adj_option_premium_ratio,
                                                                      list_of_quotes_from_delay_in_trading,
                                                                      option_sensitivity_to_strike,
                                                                      multiple_of_one_deal, days_delay_in_trading,
                                                                      option_premium_price, mult_upside,
                                                                      mult_breakthrough, list_of_quotes)
    else:
        breakthrough_code = 0
    if strong_signal_in_scope == 1:
        strong_signal_code = strategy_strong_signal.verify_strong_signal_type(list_of_quotes, list_of_RSI_quotes,
                                                                              todays_quote, percentage_change,
                                                                              list_of_quotes_from_delay_in_trading,
                                                                              yesterdays_rsi, option_premium_price,
                                                                              mult_upside, RSI_threshold_regular)
    else:
        strong_signal_code = 0
    if strong_signal_code == 0 and signal_in_scope == 1:
        # signal_code=verify_signal_type(position_in_dates, todays_quote, yesterdays_quote, percentage_change,
        #              option_premium_bm, selected_title,adj_option_premium_ratio, list_of_quotes_from_delay_in_trading,
        #              option_sensitivity_to_strike,multiple_of_one_deal,days_delay_in_trading,option_premium_price,mult_upside)
        signal_code = 0
    else:
        signal_code = 0
    if (resistance_code == 1) or (strong_signal_code == 1) or (signal_code == 1) or (breakthrough_code == 1):

        transaction_type = helpers.determine_transaction_type_from_codes(percentage_change, resistance_code)

        # transaction_type=check_transaction_type(resistance_code,percentage_change)

        option_strike = model_pricing.compute_option_strike_precised(transaction_type, todays_quote,
                                                                     option_premium_price)

        position_in_open_pf_found = verify_if_position_in_open_pf_found(open_positions_pf, position_in_dates,
                                                                        mult_upside, option_premium_price,
                                                                        option_strike, second_exit_check,
                                                                        transaction_type, todays_quote, position_name)
        # green light - implementation of in or out for certain transaction direction

        green_light = helpers.check_if_transaction_inscope(transaction_type, call_in_scope, put_in_scope)
        if position_in_open_pf_found == 0 and green_light == 1:
            entry_option_price = model_pricing.compute_entry_option_price(option_strike, todays_quote, transaction_type,
                                                                          option_premium_price,
                                                                          option_sensitivity_to_strike)

            entry_type = model_trading.return_entry_type(resistance_code, strong_signal_code, signal_code,
                                                         breakthrough_code)

            transaction_value_in_and_boost_flag = model_trading.compute_transaction_value_in(entry_option_price,
                                                                                             financial_properties_df,
                                                                                             strong_signal_code,
                                                                                             RSI_threshold_increased,
                                                                                             yesterdays_rsi)
            transaction_value_in = transaction_value_in_and_boost_flag[0]
            boost_flag = transaction_value_in_and_boost_flag[1]
            date_in = dates[position_in_dates]
            day_in, month_in, year_in = date_in.split('.')
            nr_entry_row = int(np.where(dates == date_in)[0] + 1)

            option_deal_to_be_added = [position_name, transaction_type, option_strike, todays_quote, "", "",
                                       entry_option_price, "", option_duration_in_days,
                                       entry_type, transaction_value_in, "", "", date_in, "", "", "", percentage_change,
                                       yesterdays_rsi,
                                       int(year_in), boost_flag, 0, 0, 0, nr_entry_row, todays_quote]
            open_positions_pf.loc[len(open_positions_pf.index)] = option_deal_to_be_added
            # section where financial stats are updated
            financial_properties_to_be_added = my_data.update_financial_properties_for_opening(
                financial_properties_df,
                transaction_value_in, date_in)
            financial_properties_df.loc[
                len(financial_properties_df.index)] = financial_properties_to_be_added
    return open_positions_pf, financial_properties_df


def verify_if_position_in_open_pf_found(open_positions_pf, position_in_dates, mult_upside, option_premium_price,
                                        option_strike, second_exit_check, transaction_type, todays_quote,
                                        position_name):
    position_in_open_pf_found = 0
    if not open_positions_pf.empty:
        for index, single_position in open_positions_pf.iterrows():
            transaction_type_from_pf = single_position["transaction_type"]
            position_name_from_pf = single_position["position_name"]
            if transaction_type_from_pf == transaction_type and position_name_from_pf == position_name:
                entry_date = single_position["date_in"]
                nr_entry_row = int(single_position['entry_row_idx'])
                duration_in_days = helpers.duration_of_position(position_in_dates, nr_entry_row)
                option_strike_from_pf = single_position["option_strike"]
                tolerance_between_strikes = mult_upside * option_premium_price * todays_quote
                if transaction_type_from_pf == "call":
                    difference_between_strikes = option_strike_from_pf - option_strike
                elif transaction_type_from_pf == "put":
                    difference_between_strikes = option_strike - option_strike_from_pf
                    # bm 79 moj quote 77 25.108.191.181
                    # 25.108.191. 181
                if (difference_between_strikes < tolerance_between_strikes) and (
                        duration_in_days < second_exit_check - 1):
                    position_in_open_pf_found = 1
                    return position_in_open_pf_found
    else:
        position_in_open_pf_found = 0
    return position_in_open_pf_found
