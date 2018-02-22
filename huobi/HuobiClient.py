from huobi.HuobiServices import *


# 换币利率排行
def get_trade_top():
    trade_top = {}
    trade_groups = ALL_TRADE_GROUP
    for trade_group in trade_groups:
        trade_list = trade_group.split('-')
        detail_result0 = get_detail(trade_list[0])
        detail_result1 = get_detail(trade_list[1])
        detail_result2 = get_detail(trade_list[2])
        if detail_result0 and detail_result0.get('status') == 'ok' and detail_result1 and detail_result1.get(
                'status') == 'ok' and detail_result2 and detail_result2.get('status') == 'ok':
            first_coins_start = trade_list[0][:trade_list[0].find('usdt')]
            trade_amount = 0
            if trade_list[1].startswith(first_coins_start):
                trade_amount = 1 / float(detail_result0.get('tick').get('close')) * float(
                    detail_result1.get('tick').get('close')) * float(detail_result2.get('tick').get('close'))
            elif trade_list[1].endswith(first_coins_start):
                trade_amount = 1 / float(detail_result0.get('tick').get('close')) / float(
                    detail_result1.get('tick').get('close')) * float(detail_result2.get('tick').get('close'))
            trade_top[trade_group] = [detail_result0.get('tick').get('close'), detail_result1.get('tick').get('close'),
                                      detail_result2.get('tick').get('close'), trade_amount * 0.994 - 1]
    trade_top = sorted(trade_top.items(), key=lambda x: x[1][3], reverse=True)
    return trade_top


# 获取某个换币组合的利率
def get_one_detail(trade_group=None):
    trade_list = trade_group.split('-')
    detail_result0 = get_detail(trade_list[0])
    detail_result1 = get_detail(trade_list[1])
    detail_result2 = get_detail(trade_list[2])
    if detail_result0 and detail_result0.get('status') == 'ok' and detail_result1 and detail_result1.get(
            'status') == 'ok' and detail_result2 and detail_result2.get('status') == 'ok':
        first_coins_start = trade_list[0][:trade_list[0].find('usdt')]
        trade_amount = 0
        if trade_list[1].startswith(first_coins_start):
            trade_amount = 1 / float(detail_result0.get('tick').get('close')) * float(
                detail_result1.get('tick').get('close')) * float(detail_result2.get('tick').get('close'))
        elif trade_list[1].endswith(first_coins_start):
            trade_amount = 1 / float(detail_result0.get('tick').get('close')) / float(
                detail_result1.get('tick').get('close')) * float(detail_result2.get('tick').get('close'))
        return trade_amount * 0.998 * 0.998 * 0.998 - 1


# 获取某个币种的现货余额
def get_coin_balance(coin_name=None):
    result_data = get_balance()
    if result_data and result_data.get('status') == 'ok':
        balance_list = result_data.get('data').get('list')
        for balance_coin in balance_list:
            if balance_coin and balance_coin.get('currency') == coin_name and balance_coin.get('type') == 'trade':
                return balance_coin.get('balance')


# 创建订单
def create_order(amount, symbol, _type, price=0):
    result_data = send_order(amount=amount, symbol=symbol, source='api', _type=_type, price=price)
    if result_data and result_data.get('status') == 'ok':
        order_id = result_data.get('data')
        return order_id
    else:
        print('创建订单失败，', amount, symbol, _type, price, result_data)


# 执行一组换币交易
def trade_process():
    trade_top_list = get_trade_top()
    trade_top_first = trade_top_list[0]

    trade_first_value = trade_top_first[1]
    top_rate = float(trade_first_value[3])
    if top_rate > 0.01:
        trade_first_key = trade_top_first[0]
        trade_list = trade_first_key.split('-')
        create_order(1, trade_list[0], 'buy-limit', trade_first_value[0])
        coin_amount = 1 * 0.998 / float(trade_first_value[0])
        if trade_list[1].endswith('btc') or trade_list[1].endswith('eth'):
            create_order(coin_amount, trade_list[1], 'buy-limit', trade_first_value[1])
            coin_amount = coin_amount * 0.998 / trade_first_value[1]
        else:
            create_order(coin_amount, trade_list[1], 'sell-limit', trade_first_value[1])
            coin_amount = coin_amount * 0.998 * trade_first_value[1]
        create_order(coin_amount, trade_list[3], 'sell-limit', trade_first_value[2])
        coin_amount = coin_amount * trade_first_value[2] * 0.998 - 1


def get_coin_close(coin_group=None):
    detail_result = get_detail(coin_group)
    if detail_result and detail_result.get('status') == 'ok':
        return detail_result.get('tick').get('close')
    else:
        print('获取币种当前价格出错，', coin_group, detail_result)


# 测试一组换币交易
def trade_process_test(min_rate=1):
    trade_top_list = get_trade_top()
    trade_top_first = trade_top_list[0]

    trade_first_value = trade_top_first[1]
    top_rate = float(trade_first_value[3])
    print(trade_top_first)
    if top_rate >= min_rate:
        i = 0
        while i < 15:
            i = i + 1
            trade_top_first = trade_top_list[0]
            trade_first_key = trade_top_first[0]
            trade_list = trade_first_key.split('-')
            first_close = get_coin_close(trade_list[0])
            second_close = get_coin_close(trade_list[1])
            third_close = get_coin_close(trade_list[2])
            coin_amount = 1 * 0.998 / float(first_close)
            if trade_list[0].startswith('btc') or (trade_list[0].startswith('eth') and trade_list[1].endswith('eth')):
                coin_amount = coin_amount * 0.998 / float(second_close)
            else:
                coin_amount = coin_amount * 0.998 * float(second_close)
            coin_amount = coin_amount * float(third_close) * 0.998 - 1
            print(first_close, second_close, third_close, coin_amount)


def get_symbols_list():
    result_data = get_symbols()
    response_data = {}
    if result_data and result_data.get('status') == 'ok':
        data_list = result_data.get('data')
        for one_data in data_list:
            response_data[one_data.get('base-currency') + one_data.get('quote-currency')] = one_data.get(
                'amount-precision')
        return response_data


if __name__ == '__main__':
    # print(get_symbols_list())
    # print(get_symbol_list())
    # for symbol_group in get_symbol_list():
    #     print(symbol_group)
    trade_top_list = get_trade_top()
    print(type(trade_top_list))
    for trade_top1 in trade_top_list:
        print(trade_top1)
    # print(get_accounts())
    # print(get_balance())
    # for xx in get_symbol_list():
    #     print(xx)
    # for trade_group in get_trade_group():
    #     print(trade_group)
    # print(get_trade_group())
    # print(get_one_detail('ethusdt-cvceth-cvcusdt'))
    # print(get_symbols())
    # print(get_coin_balance('usdt'))
    # trade_process_test(0.001)
    # print(AMOUNT_PRECISION.get('omgusdt'))
    # print(create_order('{:.4f}'.format(1 / 10.01), 'omgusdt', 'buy-limit', 10.01))
    # print(order_info(1296036671))
