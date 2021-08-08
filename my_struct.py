from dataclasses import dataclass


@dataclass
class Quote:
    """Class for keeping track of an item in inventory."""
    symbol: str
    todays_close: float
    todays_lo: float
    todays_hi: float
    yesterdays_quote: float
    yesterdays_rsi: float
    tomorrows_min_quote: float = float('NaN')
    tomorrows_max_quote: float = float('NaN')


# adjusted structure for additional columns
DEAL_PROPERTIES_DICT = {"position_name": [], "transaction_type": [], "option_strike": [], "entry_quote": [],
                        "sale_quote": [], "pecentage_gain_quote": [], "entry_option_price": [],
                        "sale_option_price": [],
                        "duration_of_option": [], "entry_type": [], "transaction_value_in": [],
                        "transaction_value_out": [],
                        "pecentage_gain": [], "date_in": [], "date_out": [],
                        "duration": [], "phase_of_closing": [], "quote_in_pr_to_enter": [], "RSI_in": [],
                        "year": [], "boost_flag": [], "early_termination_flag": [], "daily_trading_flag": [],
                        "strike_modified_flag": [], "entry_row_idx": [], 'entry_price': []
                        }
# ,"quote_in_pr_to_enter":[]
FINANCIAL_PROPERTIES_DICT = {"Date": [], "Balance": [], "trx_nr": [], "Invested": [], "Cash": [], "deal_size": [],
                             "total_gain": [], "signal_trx_nr": [], "signal_trx_gain": [],
                             "strong_signal_trx_nr": [], "strong_signal_trx_gain": [], "resistance_trx_nr": [],
                             "resistance_trx_gain": [], "breakthrough_trx_nr": [], "breakthrough_trx_gain": [],
                             "daily_trading_call_trx_nr": [], "daily_trading_call": [],
                             "daily_trading_put_trx_nr": [], "daily_trading_put": []
                             }
