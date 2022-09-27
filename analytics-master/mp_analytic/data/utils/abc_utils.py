def get_profit(value):
    if type(value) != int:
        return '-'
    result = 'C'
    if 20 < value <= 40:
        result = 'B'
    elif value > 40:
        result = 'A'
    return result


def get_turnover(value):
    if type(value) != int:
        return '-'
    result = 'A'
    if 30 < value <= 60:
        result = 'B'
    elif value > 60:
        result = 'C'
    return result


def get_abc(profit, turnover):
    if profit not in ['A', 'B', 'C'] and turnover not in ['A', 'B', 'C']:
        return '-'
    if profit == 'A' and turnover == 'C' or profit == 'C' and turnover == 'A':
        return 'B'
    return max(profit, turnover)


def get_row_for_abc(op, rub, dynamic, stocks) -> list:
    profit = '-'
    if not isinstance(op, str) and not isinstance(rub, str):
        if rub != 0:
            profit = round(op / rub * 100)
            if op < 0 and rub < 0:
                profit *= -1
    profit_letter = get_profit(profit) if not isinstance(profit, str) else '-'

    turnover = '-'
    if not isinstance(dynamic, str) and not isinstance(stocks, str):
        if dynamic != 0:
            turnover = round(stocks / (dynamic / 7) * 100)
    turnover_letter = get_turnover(turnover) if not isinstance(turnover, str) else '-'

    abc = '-'
    if profit_letter != '-' and turnover_letter != '-':
        abc = get_abc(profit_letter, turnover_letter)

    return [profit_letter, turnover_letter, abc]

