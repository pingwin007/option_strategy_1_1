import math

import numpy as np

import tags


def verify_type_of_transaction(single_position):
    option_type = single_position["transaction_type"]
    if option_type == "put":
        return -1
    elif option_type == "call":
        return 1
    raise RuntimeError


def duration_of_position(position_in_dates, nr_entry_row):
    duration = position_in_dates + 2 - nr_entry_row
    return duration


def covert_string_quotes_into_returns(list_of_quotes):
    float_list = []
    for el in range(1, len(list_of_quotes), 1):
        # pdb.set_trace()
        up = float(list_of_quotes[el + 1])
        down = float(list_of_quotes[el])
        float_list.append(math.log(up / down))
    float_list = np.asarray(float_list)
    return float_list


def determine_transaction_type_from_codes(percentage_change, resistance_code):
    if percentage_change >= 0 and resistance_code == 1:
        transaction_type = "put"
    elif percentage_change >= 0 and resistance_code == 0:
        transaction_type = "call"
    elif percentage_change < 0 and resistance_code == 1:
        transaction_type = "call"
    elif percentage_change < 0 and resistance_code == 0:
        transaction_type = "put"
    return transaction_type


def check_if_transaction_inscope(transaction_type, call_in_scope, put_in_scope):
    if transaction_type == "call" and call_in_scope == 1:
        green_light = 1
    elif transaction_type == "put" and put_in_scope == 1:
        green_light = 1
    else:
        green_light = 0
    return green_light


def get_cols_for_stock(curr_symbol):
    col_close = curr_symbol + tags.SUFFIX_CLOSE
    col_lo = curr_symbol + tags.SUFFIX_LO
    col_hi = curr_symbol + tags.SUFFIX_HI
    col_rsi = curr_symbol + tags.SUFFIX_RSI
    if curr_symbol == 'NOVN':
        col_rsi = col_rsi + '_14'
    return col_close, col_hi, col_lo, col_rsi
