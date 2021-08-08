import tags


def get_fin_properties_to_append(last_financial_record, capital_in, capital_out, date_out, single_position):
    # finance specific postions
    last_balance = float(last_financial_record["Balance"])
    last_trx_nr = int(last_financial_record["trx_nr"])
    last_Invested_capital = float(last_financial_record["Invested"])
    last_Cash_balance = float(last_financial_record["Cash"])
    last_total_gain = float(last_financial_record["total_gain"])
    last_deal_size = float(last_financial_record["deal_size"])
    # breakdown among transactions type
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
    last_Invested_capital = last_Invested_capital - capital_in
    last_Cash_balance = last_Cash_balance + capital_out
    last_balance = last_balance + (capital_out - capital_in)
    last_trx_nr = last_trx_nr + 1
    last_total_gain = last_total_gain + (capital_out - capital_in)
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
    financial_properties_to_be_added = [date_out, last_balance, last_trx_nr, last_Invested_capital,
                                        last_Cash_balance, last_deal_size, last_total_gain,
                                        last_signal_nr, last_signal_gain, last_strong_signal_nr,
                                        last_strong_signal_gain,
                                        last_resistance_nr, last_resistance_gain,
                                        last_breakthrough_nr, last_breakthrough_gain,
                                        last_daily_trading_call_trx_nr, last_daily_trading_call_gain,
                                        last_daily_trading_put_trx_nr, last_daily_trading_put_gain]
    return financial_properties_to_be_added


def update_financial_properties_for_opening(financial_properties_df, transaction_value_in, date_in):
    last_financial_record = financial_properties_df[-1:]
    # finance specific postions
    last_balance = float(last_financial_record["Balance"])
    last_trx_nr = int(last_financial_record["trx_nr"])
    last_Invested_capital = float(last_financial_record["Invested"])
    last_Cash_balance = float(last_financial_record["Cash"])
    last_total_gain = float(last_financial_record["total_gain"])
    last_deal_size = float(last_financial_record["deal_size"])
    # breakdown among transactions type
    last_strong_signal_nr = int(last_financial_record["strong_signal_trx_nr"])
    last_strong_signal_gain = float(last_financial_record["strong_signal_trx_gain"])
    last_signal_nr = int(last_financial_record["signal_trx_nr"])
    last_signal_gain = float(last_financial_record["signal_trx_gain"])
    last_resistance_nr = int(last_financial_record["resistance_trx_nr"])
    last_resistance_gain = float(last_financial_record["resistance_trx_gain"])
    last_breakthrough_nr = int(last_financial_record["breakthrough_trx_nr"])
    last_breakthrough_gain = float(last_financial_record["breakthrough_trx_gain"])
    last_daily_trading_call_trx_nr = int(last_financial_record["daily_trading_call_trx_nr"])
    last_daily_trading_call = float(last_financial_record["daily_trading_call"])
    last_daily_trading_put_trx_nr = int(last_financial_record["daily_trading_put_trx_nr"])
    last_daily_trading_put = float(last_financial_record["daily_trading_put"])
    last_Invested_capital = last_Invested_capital + transaction_value_in
    last_Cash_balance = last_Cash_balance - transaction_value_in
    financial_properties_to_be_added = [date_in, last_balance, last_trx_nr, last_Invested_capital,
                                        last_Cash_balance, last_deal_size, last_total_gain,
                                        last_signal_nr, last_signal_gain, last_strong_signal_nr,
                                        last_strong_signal_gain,
                                        last_resistance_nr, last_resistance_gain,
                                        last_breakthrough_nr, last_breakthrough_gain,
                                        last_daily_trading_call_trx_nr,
                                        last_daily_trading_call,
                                        last_daily_trading_put_trx_nr,
                                        last_daily_trading_put]
    return financial_properties_to_be_added


def extract_stock_cfg(curr_title_cfg):
    position_name = str(curr_title_cfg[tags.COL_STOCK_NAME])
    option_premium_price = float(curr_title_cfg[tags.COL_OPTION_PREMIUM])
    first_exit_check = int(curr_title_cfg[tags.COL_FIRST_EXIT_CHECK])
    second_exit_check = int(curr_title_cfg[tags.COL_SECOND_EXIT_CHECK])
    call_in_scope = int(curr_title_cfg[tags.COL_CALL_ENABLED])
    put_in_scope = int(curr_title_cfg[tags.COL_PUT_ENABLED])
    resistance_in_scope = int(curr_title_cfg[tags.COL_STRAT_RESISTANCE_ENABLED])
    breakthrough_in_scope = int(curr_title_cfg[tags.COL_STRAT_BREAKTHROUGH_ENABLED])
    strong_signal_in_scope = int(curr_title_cfg[tags.COL_STRAT_STRONG_SIGNAL_ENABLED])
    signal_in_scope = int(curr_title_cfg[tags.COL_STRAT_SIGNAL_ENABLED])
    RSI_threshold_regular = float(curr_title_cfg[tags.COL_RSI_REGULAR])
    RSI_threshold_increased = float(curr_title_cfg[tags.COL_RSI_INCR])
    daily_trading_call_in_scope = int(curr_title_cfg[tags.COL_DAILY_TRADING_CALLS_ENABLED])
    daily_trading_put_in_scope = int(curr_title_cfg[tags.COL_DAILY_TRADING_PUTS_ENABLED])

    return position_name, option_premium_price, first_exit_check, second_exit_check, call_in_scope, put_in_scope, resistance_in_scope, breakthrough_in_scope, strong_signal_in_scope, signal_in_scope, RSI_threshold_regular, RSI_threshold_increased, daily_trading_call_in_scope, daily_trading_put_in_scope


def unpack_model_config(model_cfg):
    def get_cfg(param):
        return model_cfg.loc[param,][0]

    selected_start_date = get_cfg(tags.PARAM_SIM_START)
    # reading parameters from the file -> which will be distributed among procedures / functions
    option_premium_bm = float(get_cfg(tags.PARAM_OPTION_PREMIUM_BM))
    option_duration_in_days = int(get_cfg(tags.PARAM_OPTION_LIVESPAN))
    option_sensitivity_to_strike = float(get_cfg(tags.PARAM_OTM_DISCOUNT_SENSITIVITY))
    return_threshold = (get_cfg(tags.PARAM_FIRST_CHECKIN_STOCK_PRICE_INCREASE_THRESHOLD_TO_LIQUIDATE),
                        get_cfg(tags.PARAM_SECOND_CHECKIN_STOCK_PRICE_INCREASE_THRESHOLD_TO_LIQUIDATE),
                        get_cfg(tags.PARAM_POST_SECOND_CHECKIN_STOCK_PRICE_INCREASE_THRESHOLD_TO_LIQUIDATE))
    factor_remaining_time_value = (
        get_cfg(tags.PARAM_ITM_DEPTH_LO),
        get_cfg(tags.PARAM_ITM_DEPTH_MID),
        get_cfg(tags.PARAM_ITM_DEPTH_HI))
    multiple_of_one_deal = int(get_cfg(tags.PARAM_TOTAL_CASH_TO_SINGLE_DEAL))
    days_delay_in_trading = int(get_cfg(tags.PARAM_LOOKBACK_HORIZON))
    mult_upside = float(get_cfg(tags.PARAM_MODEL_SCALING))
    mult_breakthrough = float(get_cfg(tags.PARAM_BREAKTHROUGH_FACTOR))
    early_termination_enabled = int(get_cfg(tags.PARAM_EARLY_TERMINATION_ENABLED))
    early_termination_threshold_return = float(get_cfg(tags.PARAM_EARLY_TERMINATION_RETURN_THRESHOLD))
    daily_fluctuation_percentage = float(get_cfg(tags.PARAM_REPURCHASE_CONDITION))
    return days_delay_in_trading, factor_remaining_time_value, mult_breakthrough, mult_upside, multiple_of_one_deal, option_duration_in_days, option_premium_bm, option_sensitivity_to_strike, return_threshold, selected_start_date, daily_fluctuation_percentage, early_termination_enabled, early_termination_threshold_return
