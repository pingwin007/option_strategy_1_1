import math


def compute_sale_option_price(duration_in_days, sign_of_option, entry_quote, factor_remaining_time_value,
                              option_premium_price, option_premium_bm, option_duration_in_days, entry_option_price,
                              option_strike, option_sensitivity_to_strike, todays_quote):
    # 0.01 ->NODE_Low
    # 0.2 ->NODE_Mid
    # 0.5 ->NODE_High
    # percentage_change -> in_the_money_depth
    percentage_change = sign_of_option * (math.log(todays_quote / option_strike))
    linear_adjustment = (option_premium_price / option_premium_bm)
    # holding_ratio -> option_life_remaining (in_percentage)
    holding_ratio = 1 - (duration_in_days / option_duration_in_days)

    change_threshold1 = float(factor_remaining_time_value[0]) * linear_adjustment
    change_threshold2 = float(factor_remaining_time_value[1]) * (option_premium_price / option_premium_bm)
    change_threshold3 = float(factor_remaining_time_value[2]) * (option_premium_price / option_premium_bm)
    if percentage_change >= change_threshold1:
        remaining_time_value = 0.01 * holding_ratio
    elif percentage_change >= change_threshold2:
        difference_return_threshold = percentage_change - (float(factor_remaining_time_value[1]) * linear_adjustment)
        difference_limits = (float(factor_remaining_time_value[0]) - float(
            factor_remaining_time_value[1])) * linear_adjustment
        remaining_time_value = ((1 - (difference_return_threshold / difference_limits)) * 0.2 + 0.01) * holding_ratio
    elif percentage_change >= change_threshold3:
        difference_return_threshold = percentage_change - (float(factor_remaining_time_value[2]) * linear_adjustment)
        difference_limits = (float(factor_remaining_time_value[1]) - float(
            factor_remaining_time_value[2])) * linear_adjustment
        remaining_time_value = ((1 - (difference_return_threshold / difference_limits)) * 0.5 + 0.2) * holding_ratio
    else:
        difference_return_threshold = (percentage_change - 0)
        difference_limits = (float(factor_remaining_time_value[2]) - 0) * linear_adjustment
        remaining_time_value = ((1 - (difference_return_threshold / difference_limits)) * 0.5 + 0.5) * holding_ratio
        
    option_price = max(0, sign_of_option * (todays_quote - option_strike + (
            option_strike - entry_quote) * option_sensitivity_to_strike) + remaining_time_value * entry_option_price)
    return option_price


def compute_option_strike_precised(transaction_type, todays_quote, option_premium_price):
    if option_premium_price * todays_quote < 1:
        print("insert second comma place rounding compute strike price: 8.54->8.5")
        if transaction_type == "call":
            option_strike = math.ceil(todays_quote * 10) / 10
        else:
            option_strike = math.floor(todays_quote * 10) / 10
    else:
        print("previously conducted rounding: 86.45->86")
        if transaction_type == "call":
            option_strike = math.ceil(todays_quote)
        else:
            option_strike = math.floor(todays_quote)
    return option_strike


def ___deprecated_compute_option_strike___(transaction_type, todays_quote):  # deprecated
    if transaction_type == "call":
        option_strike = math.ceil(todays_quote)
    else:
        option_strike = math.floor(todays_quote)
    return option_strike


def compute_entry_option_price(option_strike, todays_quote, transaction_type, option_premium_price,
                               option_sensitivity_to_strike):
    option_sign = 1
    if transaction_type == "put":
        option_sign = -1
    base_price = todays_quote * option_premium_price
    discount = option_sign * (option_strike - todays_quote) * option_sensitivity_to_strike
    entry_option_price = base_price - discount
    return entry_option_price
