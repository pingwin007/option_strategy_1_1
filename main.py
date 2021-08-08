# import yfinance as yf #not used
import math

import pandas as pd

import data_io
import helpers
import my_data
import my_struct
import op_open_new_positions
import op_rebalancing_closing
import op_remove_expired
import tags


def engine():
    data_to_operate, model_cfg, position_matrix_df = data_io.read_inputs()

    # building structure for operating on investment portfolios: dictionary -> pandas ->
    financial_properties_df, historical_positions_pf, open_positions_pf = initialize_main_dfs()

    # transposed_data = list(map(list, zip(*data))) #unused
    days_delay_in_trading, _, _, _, _, _, _, _, _, _, _, _, _ = my_data.unpack_model_config(model_cfg)
    selected_start_date = model_cfg.loc[tags.PARAM_SIM_START,][0]
    dates = data_to_operate.iloc[:, 0]
    nr_row = data_to_operate.loc[data_to_operate['Dates'] == selected_start_date].index[0] - 1

    # adjust_here_starting_parameters_for_simulation
    financial_properties_df.loc[len(financial_properties_df.index)] = [selected_start_date, 50000, 0, 0, 50000, 2000, 0,
                                                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # for-loop below needs to finish one day before the last row will be reached
    # index of current date - e.g. 31.05.2015 -> integer: 1536
    for position_in_dates in range(nr_row, len(data_to_operate) - 1, 1):
        curr_date = data_to_operate['Dates'][position_in_dates]
        # current_title -> current_stoc //to be renamed
        for title_idx, curr_title_cfg in position_matrix_df.iterrows():
            curr_symbol = curr_title_cfg[tags.COL_STOCK_SYMBOL]
            selected_title_pidx = title_idx + 1
            in_scope = int(curr_title_cfg[tags.COL_STOCK_ENABLED])
            if in_scope != 1:
                continue  # skip to next stocks
            col_close, _, _, col_rsi = helpers.get_cols_for_stock(curr_symbol)
            list_of_quotes = data_to_operate.loc[:, col_close]
            list_of_RSI_quotes = data_to_operate.loc[:, col_rsi]
            list_of_quotes_from_delay_in_trading = data_to_operate.iloc[
                                                   (position_in_dates - days_delay_in_trading):(position_in_dates)][
                col_close]
            # --------------------------------------------------------
            ############################################################################################################
            ############################################################################################################
            # STEP 0: identify index
            ############################################################################################################
            quote_struct, percentage_change = extract_current_quote(data_to_operate, position_in_dates, curr_symbol,
                                                                    False)
            open_positions_pf, historical_positions_pf, financial_properties_df = op_rebalancing_closing.portfolio_rebalancing(
                open_positions_pf, historical_positions_pf, financial_properties_df, position_in_dates,
                selected_title_pidx, curr_title_cfg, model_cfg, curr_symbol, quote_struct, dates, list_of_quotes)
            # financial_properties_df -> portfolio financial overview
            ############################################################################################################
            # STEP 2: open new positions
            open_positions_pf, financial_properties_df = op_open_new_positions.open_positions(open_positions_pf,
                                                                                              financial_properties_df,
                                                                                              position_in_dates,
                                                                                              percentage_change,
                                                                                              selected_title_pidx,
                                                                                              curr_title_cfg, model_cfg,
                                                                                              list_of_quotes,
                                                                                              list_of_RSI_quotes,
                                                                                              list_of_quotes_from_delay_in_trading,
                                                                                              quote_struct, dates)
            ############################################################################################################
            # STEP 3: remove expired positions
            option_duration_in_days = int(model_cfg.loc[tags.PARAM_OPTION_LIVESPAN,][0])
            open_positions_pf, historical_positions_pf, financial_properties_df = op_remove_expired.remove_expired_positions(
                position_in_dates, open_positions_pf, financial_properties_df, option_duration_in_days,
                historical_positions_pf, curr_title_cfg, quote_struct, curr_date)
            ############################################################################################################
            ############################################################################################################

    data_io.write_outputs(open_positions_pf, historical_positions_pf, financial_properties_df)


def initialize_main_dfs():
    # daily_trading_call_trx_nr	daily_trading_call	daily_trading_put_trx_nr	daily_trading_put
    open_positions_pf = pd.DataFrame(my_struct.DEAL_PROPERTIES_DICT)  # live pf will be stored
    historical_positions_pf = pd.DataFrame(my_struct.DEAL_PROPERTIES_DICT)  # closed deals will be stored
    financial_properties_df = pd.DataFrame(my_struct.FINANCIAL_PROPERTIES_DICT)
    return financial_properties_df, historical_positions_pf, open_positions_pf


def extract_current_quote(data_to_operate, position_in_dates, curr_symbol, look_forward=False):
    col_close, col_hi, col_lo, col_rsi = helpers.get_cols_for_stock(curr_symbol)
    todays_close = float(data_to_operate.iloc[position_in_dates][col_close])
    todays_lo = float(data_to_operate.iloc[position_in_dates][col_lo])
    todays_hi = float(data_to_operate.iloc[position_in_dates][col_hi])
    yesterdays_quote = float(data_to_operate.iloc[(position_in_dates - 1)][col_close])
    yesterdays_rsi = float(data_to_operate.iloc[position_in_dates - 1][col_rsi])

    quote = my_struct.Quote(symbol=curr_symbol, todays_close=float(todays_close), todays_lo=float(todays_lo),
                            todays_hi=float(todays_hi),
                            yesterdays_quote=float(yesterdays_quote), yesterdays_rsi=float(yesterdays_rsi))
    quote.dict = {tags.SUFFIX_CLOSE: col_close, tags.SUFFIX_LO: col_lo, tags.SUFFIX_HI: col_hi}
    if look_forward:
        quote.tomorrows_min_quote = float(data_to_operate.iloc[position_in_dates + 1][col_lo])
        quote.tomorrows_max_quote = float(data_to_operate.iloc[position_in_dates + 1][col_hi])

    percentage_change = math.log(quote.todays_close / quote.yesterdays_quote)
    # block of variables for early termination / daily trading
    # yesterday's extrema
    # today's extrema
    # both values will be further send to the functions

    return quote, percentage_change


# execution of the main function
if __name__ == "__main__":
    engine()
