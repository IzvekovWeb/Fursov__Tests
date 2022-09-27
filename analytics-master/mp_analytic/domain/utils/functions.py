def price_formatting(price):
    return {price[0][i]: int(price[1][i]) if price[1][i] else '-' for i in range(1, len(price[0]))}