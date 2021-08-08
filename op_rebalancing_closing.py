import math

import numpy as np

import helpers
# from helpers import verify_type_of_transaction, duration_of_position, covert_string_quotes_into_returns
import model_pricing
import model_trading
import my_data
import op_daily_trading
import tags


def portfolio_rebalancing(open_positions_pf, historical_positions_pf, financial_properties_df, position_in_dates,
                          selected_title, curr_title_cfg, model_cfg, curr_symbol, quote_struct, dates, list_of_quotes):
    if open_positions_pf.empty:
        return open_positions_pf, historical_positions_pf, financial_properties_df

    col_close, col_hi, col_lo, col_rsi = helpers.get_cols_for_stock(curr_symbol)

    days_delay_in_trading, factor_remaining_time_value, mult_breakthrough, mult_upside, multiple_of_one_deal, option_duration_in_days, option_premium_bm, option_sensitivity_to_strike, return_threshold, selected_start_date, daily_fluctuation_percentage, early_termination_enabled, early_termination_threshold_return \
        = my_data.unpack_model_config(model_cfg)

    correct_index = 0
    extra_correction = 0
    # adj_option_premium_ratio -> model_parameters_scaling_factor

    option_premium_price = float(curr_title_cfg[tags.COL_OPTION_PREMIUM])

    adj_option_premium_ratio = option_premium_price / option_premium_bm
    for index, single_position in open_positions_pf.iterrows():
        position_in_dates0 = position_in_dates  # DEBUG
        print(single_position)
        early_termination_executed = 0
        # if correct_index != 0:
        index = index - correct_index
        # adjusting positions to the layout of corresponding data input file

        ##############################
        ##############################
        # FIXME
        entry_date = single_position["date_in"]
        nr_entry_row = int(single_position['entry_row_idx'])
        duration_in_days = helpers.duration_of_position(position_in_dates, nr_entry_row)
        entry_quote = single_position['entry_price']
        date_out = dates[position_in_dates]

        yesterdays_quote = quote_struct.yesterdays_quote
        # reading min / max -----------------------------------------------------------
        daily_returns_list = helpers.covert_string_quotes_into_returns(list_of_quotes)
        ##############################
        ##############################
        option_premium_price = float(curr_title_cfg[tags.COL_OPTION_PREMIUM])
        first_exit_check = int(curr_title_cfg[tags.COL_FIRST_EXIT_CHECK])
        second_exit_check = int(curr_title_cfg[tags.COL_SECOND_EXIT_CHECK])

        todays_quote = quote_struct.todays_close
        todays_min_quote = quote_struct.todays_lo
        todays_max_quote = quote_struct.todays_hi
        # yesterday's extrema
        # today's extrema
        # both values will be further send to the functions

        tomorrows_min_quote = quote_struct.tomorrows_min_quote
        tomorrows_max_quote = quote_struct.tomorrows_max_quote

        # ------------------------------------------------------------------------------
        # pr_move_to_max=math.log(float(quotes.iloc[0,1])/float(quotes.iloc[0,3]))
        # ------------------ code below needs to be sent to a function
        if single_position[1] == 'call':
            quote_extremum = todays_max_quote
        elif single_position[1] == 'put':
            quote_extremum = todays_min_quote
        if early_termination_enabled == 1:
            # wyznaczenie dzisiejszego quote
            # closing_shares_movement=math.log(float(quote_extremum)/float(single_position["entry_quote"]))
            # return to be added for price

            sign_of_option = helpers.verify_type_of_transaction(single_position)

            current_phase_of_closing = model_trading.verify_current_phase_of_opening(duration_in_days, first_exit_check,
                                                                                     second_exit_check)
            entry_option_price = single_position["entry_option_price"]
            option_strike = single_position["option_strike"]
            # to be send to seperate function---------------------------
            option_in_the_money = is_option_itm(option_strike, quote_extremum, sign_of_option)
            # ---------------------------------------------------------
            if option_in_the_money:

                current_sale_option_price = model_pricing.compute_sale_option_price(duration_in_days, sign_of_option,
                                                                                    entry_quote,
                                                                                    factor_remaining_time_value,
                                                                                    option_premium_price,
                                                                                    option_premium_bm,
                                                                                    option_duration_in_days,
                                                                                    entry_option_price, option_strike,
                                                                                    option_sensitivity_to_strike,
                                                                                    quote_extremum)
                current_return_on_option = (current_sale_option_price - entry_option_price) / entry_option_price
                # to be send to seperate function
                if current_return_on_option >= early_termination_threshold_return:
                    current_return_on_option = early_termination_threshold_return
                    early_termination_executed = 1
                    sale_quote = todays_quote
                    capital_in = float(single_position["transaction_value_in"])
                    gain_on_investment_in_pr = current_return_on_option
                    capital_out = (1 + gain_on_investment_in_pr) * capital_in
                    closing_shares_movement = math.log(float(sale_quote) / float(single_position["entry_quote"]))
                    current_sale_option_price = entry_option_price * (1 + early_termination_threshold_return)
                    position_to_be_closed = [single_position["position_name"], single_position["transaction_type"],
                                             single_position["option_strike"],
                                             single_position["entry_quote"], quote_extremum, closing_shares_movement,
                                             single_position["entry_option_price"],
                                             current_sale_option_price, option_duration_in_days,
                                             single_position["entry_type"], capital_in, capital_out,
                                             gain_on_investment_in_pr, single_position["date_in"], date_out,
                                             duration_in_days,
                                             current_phase_of_closing, single_position["quote_in_pr_to_enter"],
                                             single_position["RSI_in"],
                                             single_position["year"], single_position["boost_flag"], 1,
                                             single_position["daily_trading_flag"],
                                             single_position["strike_modified_flag"]]
                    historical_positions_pf.loc[len(historical_positions_pf.index)] = position_to_be_closed
                    last_financial_record = financial_properties_df[-1:]
                    # -------------------------------------------------

                    financial_properties_df = update_financial_properties_df(last_financial_record,
                                                                             financial_properties_df,
                                                                             single_position,
                                                                             capital_in, capital_out,
                                                                             multiple_of_one_deal, date_out)
                    # ----------------------------------------------------------------
                    open_positions_pf = open_positions_pf.drop(open_positions_pf.index[index])
                    open_positions_pf = open_positions_pf.reset_index(drop=True)
                    extra_correction = extra_correction + 1
                    correct_index = extra_correction
                    print("sale")
                    # threshold
                # ----------------------------------
            # correct_index=0
        # --------------------------------------------------------------------------------------------------
        # introduce warunek na ruch kursu aby rozwarzyc daily trading czy miec pewnosc, ze transakcja by sie wykonala
        # jesli sie warunek bylby spelniony zmienie cene zamkniecia na cene max dziennego
        # -----code will be sent to a function verify_daily_trading
        daily_trading_executed = op_daily_trading.verify_daily_trading_executed(list_of_quotes,
                                                                                single_position['transaction_type'],
                                                                                quote_struct)
        daily_trading_executed = 0
        signal_call_percentil = 95
        signal_put_percentil = 5

        signal_call = np.percentile(daily_returns_list, signal_call_percentil)
        signal_put = np.percentile(daily_returns_list, signal_put_percentil)
        if single_position[1] == 'call':
            quote_fluctuation = math.log(todays_max_quote / yesterdays_quote)
            if quote_fluctuation > signal_call:
                daily_trading_executed = 1
        elif single_position[1] == 'put':
            quote_fluctuation = math.log(todays_min_quote / yesterdays_quote)
            if quote_fluctuation < signal_put:
                daily_trading_executed = 1
        if early_termination_executed == 0 and (
                (duration_in_days == first_exit_check) or (duration_in_days == second_exit_check) or (
                duration_in_days > second_exit_check) or daily_trading_executed == 1):
            position_name = single_position["position_name"]

            sign_of_option = helpers.verify_type_of_transaction(single_position)

            current_phase_of_closing = model_trading.verify_current_phase_of_opening(duration_in_days, first_exit_check,
                                                                                     second_exit_check)
            # check liquidating position conditions

            liquidate_positon = verify_liquidating_position(sign_of_option, current_phase_of_closing,
                                                            option_premium_price, option_premium_bm, return_threshold,
                                                            position_name, todays_quote, entry_quote)
            # correct_index=0
            if liquidate_positon == 1:
                #
                # what do I need to
                entry_option_price = single_position["entry_option_price"]
                option_strike = single_position["option_strike"]
                single_position["transaction_type"]  # FIXME ???

                sale_option_price = model_pricing.compute_sale_option_price(duration_in_days, sign_of_option,
                                                                            entry_quote, factor_remaining_time_value,
                                                                            option_premium_price, option_premium_bm,
                                                                            option_duration_in_days, entry_option_price,
                                                                            option_strike, option_sensitivity_to_strike,
                                                                            todays_quote)
                # complete a list of historical options - all the values need to be recalculated and be ready to processed
                sale_quote = todays_quote
                capital_in = float(single_position["transaction_value_in"])
                gain_on_investment_in_pr = (sale_option_price / float(single_position["entry_option_price"])) - 1
                capital_out = (1 + gain_on_investment_in_pr) * capital_in
                closing_shares_movement = math.log(float(sale_quote) / float(single_position["entry_quote"]))
                position_to_be_closed = [single_position["position_name"], single_position["transaction_type"],
                                         single_position["option_strike"],
                                         single_position["entry_quote"], float(sale_quote), closing_shares_movement,
                                         single_position["entry_option_price"],
                                         sale_option_price, option_duration_in_days,
                                         single_position["entry_type"], capital_in, capital_out,
                                         gain_on_investment_in_pr, single_position["date_in"], date_out,
                                         duration_in_days,
                                         current_phase_of_closing, single_position["quote_in_pr_to_enter"],
                                         single_position["RSI_in"],
                                         single_position["year"], single_position["boost_flag"],
                                         single_position["early_termination_flag"],
                                         single_position["daily_trading_flag"], single_position["strike_modified_flag"],
                                         int(single_position["entry_row_idx"])]
                historical_positions_pf = historical_positions_pf.append(position_to_be_closed)
                last_financial_record = financial_properties_df[-1:]
                # -------------------------------------------------

                financial_properties_df = update_financial_properties_df(last_financial_record,
                                                                         financial_properties_df,
                                                                         single_position,
                                                                         capital_in, capital_out,
                                                                         multiple_of_one_deal, date_out)
                # ----------------------------------------------------------------
                open_positions_pf = open_positions_pf.drop(open_positions_pf.index[index])
                open_positions_pf = open_positions_pf.reset_index(drop=True)
                extra_correction = extra_correction + 1
                correct_index = extra_correction
                print("sale")
            else:
                # I need to write a function which will basically verify if position can be filled the same day
                # 1 scenario -> the same day position is filled

                daily_trading_filled_at_closing = op_daily_trading.verify_daily_trading_filled_at_closing(
                    single_position, sign_of_option, adj_option_premium_ratio, daily_fluctuation_percentage,
                    single_position['transaction_type'], quote_struct)
                if daily_trading_filled_at_closing == 1:
                    pass
                    # kroki ktore musze zrealizowac, zeby zamknac scenario 1:
                    # musze stworzyc pozycje bez zamykania obecnej czyli dzieje sie na cos rodzaju side bet nie
                    # wplywajacego na biznes
                    # majac zgode na biznes wiem, ze moj kurs sprzedazy jest nastepujacy
                    #
    return open_positions_pf, historical_positions_pf, financial_properties_df


def is_option_itm(option_strike, quote_extremum, sign_of_option):
    if sign_of_option == 1 and (quote_extremum > option_strike):
        return True
    elif sign_of_option == 0 and (quote_extremum < option_strike):
        return True
    else:
        return False


def unpack_row_from_currently_analysed_position(row_from_list_currently_analysed_position):
    # w tym momencie musze przeliczyc wszystkie dane inputowe na dynamiczna mode------------------------
    # percentage_change = math.log(todays_quote / yesterdays_quote) #ignored
    option_premium_price = float(row_from_list_currently_analysed_position[2])
    first_exit_check = int(row_from_list_currently_analysed_position[3])
    second_exit_check = int(row_from_list_currently_analysed_position[4])
    return first_exit_check, option_premium_price, second_exit_check


def verify_liquidating_position(sign_of_option, current_phase_of_opening, option_premium_price, option_premium_bm,
                                return_threshold, position_name, todays_quote, entry_quote):
    curr_symbol = position_name  # FIXME
    col_close, col_hi, col_lo, col_rsi = helpers.get_cols_for_stock(curr_symbol)

    percentage_change = sign_of_option * (math.log(todays_quote / entry_quote))
    # if todays_quote==65.86:
    if current_phase_of_opening == 1:
        threshold_absolute = float(return_threshold[0])
        threshold_adjusted = threshold_absolute * (option_premium_price / option_premium_bm)
        if percentage_change >= threshold_adjusted:
            deal_boolean = 1
            return deal_boolean
        else:
            deal_boolean = 0
            return deal_boolean
    elif current_phase_of_opening == 2:
        threshold_absolute = float(return_threshold[1])
        threshold_adjusted = threshold_absolute * (option_premium_price / option_premium_bm)
        if percentage_change >= threshold_adjusted:
            deal_boolean = 1
            return deal_boolean
        else:
            deal_boolean = 0
            return deal_boolean
    elif current_phase_of_opening == 3:
        threshold_absolute = float(return_threshold[2])
        threshold_adjusted = threshold_absolute * (option_premium_price / option_premium_bm)
        if percentage_change >= threshold_adjusted:
            deal_boolean = 1
            return deal_boolean
        else:
            deal_boolean = 0
            return deal_boolean


def update_financial_properties_df(last_financial_record, financial_properties_df, single_position,
                                   capital_in, capital_out, multiple_of_one_deal, date_out):
    last_Cash_balance, last_Invested_capital, last_balance, last_breakthrough_gain, last_breakthrough_nr, last_daily_trading_call_gain, last_daily_trading_call_trx_nr, last_daily_trading_put_gain, last_daily_trading_put_trx_nr, last_deal_size, last_resistance_gain, last_resistance_nr, last_signal_gain, last_signal_nr, last_strong_signal_gain, last_strong_signal_nr, last_total_gain, last_trx_nr = unpack_last_fin_record(
        last_financial_record)
    # update values
    last_balance = last_balance + (capital_out - capital_in)
    last_trx_nr = last_trx_nr + 1
    last_Invested_capital = last_Invested_capital - capital_in
    last_Cash_balance = last_Cash_balance + capital_out
    last_total_gain = last_total_gain + (capital_out - capital_in)

    adj_deal_size = model_trading.compute_deal_size(last_deal_size, multiple_of_one_deal, last_balance)
    if single_position["entry_type"] == "strong_signal":
        last_strong_signal_nr = last_strong_signal_nr + 1
        last_strong_signal_gain = last_strong_signal_gain + (capital_out - capital_in)
    elif single_position["entry_type"] == "signal":
        last_signal_nr = last_strong_signal_nr + 1
        last_signal_gain = last_signal_gain + (capital_out - capital_in)
    elif single_position["entry_type"] == "resistance":
        last_resistance_nr = last_resistance_nr + 1
        last_resistance_gain = last_resistance_gain + (capital_out - capital_in)
    elif single_position["entry_type"] == "breakthrough":
        last_breakthrough_nr = last_breakthrough_nr + 1
        last_breakthrough_gain = last_breakthrough_gain + (capital_out - capital_in)
    elif single_position["entry_type"] == "daily_trading_call":
        last_daily_trading_call_trx_nr = last_daily_trading_call_trx_nr + 1
        last_daily_trading_call_gain = last_daily_trading_call_gain + (capital_out - capital_in)
    elif single_position["entry_type"] == "daily_trading_put":
        last_daily_trading_put_trx_nr = last_daily_trading_put_trx_nr + 1
        last_daily_trading_put_gain = last_daily_trading_put_gain + (capital_out - capital_in)
    # list needs to be updated for new
    financial_properties_to_be_added = [date_out, last_balance, last_trx_nr, last_Invested_capital,
                                        last_Cash_balance, adj_deal_size, last_total_gain,
                                        last_signal_nr, last_signal_gain, last_strong_signal_nr,
                                        last_strong_signal_gain,
                                        last_resistance_nr, last_resistance_gain,
                                        last_breakthrough_nr, last_breakthrough_gain,
                                        last_daily_trading_call_trx_nr, last_daily_trading_call_gain,
                                        last_daily_trading_put_trx_nr, last_daily_trading_put_gain]
    financial_properties_df.loc[len(financial_properties_df.index)] = financial_properties_to_be_added
    return financial_properties_df


def unpack_last_fin_record(last_financial_record):
    last_balance = float(last_financial_record["Balance"])
    last_trx_nr = int(last_financial_record["trx_nr"])
    last_Invested_capital = float(last_financial_record["Invested"])
    last_Cash_balance = float(last_financial_record["Cash"])
    last_total_gain = float(last_financial_record["total_gain"])
    last_deal_size = float(last_financial_record["deal_size"])
    last_strong_signal_nr = int(last_financial_record["strong_signal_trx_nr"])
    last_strong_signal_gain = float(last_financial_record["strong_signal_trx_gain"])
    last_signal_nr = int(last_financial_record["signal_trx_nr"])
    last_signal_gain = float(last_financial_record["signal_trx_gain"])
    last_resistance_nr = int(last_financial_record["resistance_trx_nr"])
    last_resistance_gain = float(last_financial_record["resistance_trx_gain"])
    last_breakthrough_nr = int(last_financial_record["breakthrough_trx_nr"])
    last_breakthrough_gain = float(last_financial_record["breakthrough_trx_gain"])
    last_daily_trading_call_trx_nr = int(last_financial_record["daily_trading_call_trx_nr"])
    last_daily_trading_call_gain = float(last_financial_record["daily_trading_call"])
    last_daily_trading_put_trx_nr = int(last_financial_record["daily_trading_put_trx_nr"])
    last_daily_trading_put_gain = float(last_financial_record["daily_trading_put"])
    return last_Cash_balance, last_Invested_capital, last_balance, last_breakthrough_gain, last_breakthrough_nr, last_daily_trading_call_gain, last_daily_trading_call_trx_nr, last_daily_trading_put_gain, last_daily_trading_put_trx_nr, last_deal_size, last_resistance_gain, last_resistance_nr, last_signal_gain, last_signal_nr, last_strong_signal_gain, last_strong_signal_nr, last_total_gain, last_trx_nr
