import math

import helpers
import model_trading
import my_data
import tags


def remove_expired_positions(position_in_dates, open_positions_pf, financial_properties_df, option_duration_in_days,
                             historical_positions_pf, curr_title_cfg, quote_struct, curr_date):
    correct_index = 0
    extra_correction = 0

    first_exit_check = int(curr_title_cfg[tags.COL_FIRST_EXIT_CHECK])
    second_exit_check = int(curr_title_cfg[tags.COL_SECOND_EXIT_CHECK])

    for index, single_position in open_positions_pf.iterrows():
        sale_quote = quote_struct.todays_close
        date_out = curr_date
        # duration_in_days -> current holding age (current date - purchase date)
        duration_in_days = helpers.duration_of_position(position_in_dates, single_position["entry_row_idx"])
        index = index - correct_index
        correct_index = 0

        if duration_in_days >= option_duration_in_days:
            option_sign = helpers.verify_type_of_transaction(single_position)
            entry_quote = float(single_position["entry_quote"])
            option_strike_K = float(single_position["option_strike"])
            closing_shares_movement = math.log(sale_quote / entry_quote)
            sale_option_price = max(0, option_sign * (sale_quote - option_strike_K))

            current_phase_of_closing = model_trading.verify_current_phase_of_opening(duration_in_days, first_exit_check,
                                                                                     second_exit_check)
            capital_in = float(single_position["transaction_value_in"])
            gain_on_investment_in_pr = (sale_option_price / float(single_position["entry_option_price"])) - 1
            capital_out = (1 + gain_on_investment_in_pr) * capital_in
            position_to_be_closed = [single_position["position_name"], single_position["transaction_type"],
                                     single_position["option_strike"],
                                     single_position["entry_quote"], sale_quote, closing_shares_movement,
                                     single_position["entry_option_price"],
                                     sale_option_price, option_duration_in_days,
                                     single_position["entry_type"], capital_in, capital_out,
                                     gain_on_investment_in_pr, single_position["date_in"], date_out, duration_in_days,
                                     current_phase_of_closing, single_position["quote_in_pr_to_enter"],
                                     single_position["RSI_in"],
                                     single_position["year"], single_position["boost_flag"], 0,
                                     single_position["daily_trading_flag"], single_position["strike_modified_flag"],
                                     single_position["entry_row_idx"]]
            historical_positions_pf = historical_positions_pf.append(position_to_be_closed)
            last_financial_record = financial_properties_df[-1:]

            financial_properties_to_be_added = my_data.get_fin_properties_to_append(last_financial_record,
                                                                                    capital_in, capital_out, date_out,
                                                                                    single_position)
            financial_properties_df.loc[len(financial_properties_df.index)] = financial_properties_to_be_added
            open_positions_pf = open_positions_pf.drop(open_positions_pf.index[index])
            open_positions_pf = open_positions_pf.reset_index(drop=True)
            extra_correction = extra_correction + 1
            correct_index = extra_correction

    return open_positions_pf, historical_positions_pf, financial_properties_df
