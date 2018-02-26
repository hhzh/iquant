from huobi.HuobiServices import *
import datetime
import time


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
    try:
        result_data = send_order(amount=amount, symbol=symbol, source='api', _type=_type, price=price)
        if result_data and result_data.get('status') == 'ok':
            order_id = result_data.get('data')
            print(str(datetime.datetime.now()), '创建订单成功', amount, symbol, _type, price, order_id)
            return order_id
        else:
            print(str(datetime.datetime.now()), '创建订单失败', amount, symbol, _type, price, result_data)
            return 0
    except Exception as e:
        print(str(datetime.datetime.now()), '创建订单异常', amount, symbol, _type, price, e)
        return 0


# 执行一组换币交易
def trade_process(order_amount=1, min_rate=0.01):
    trade_top_list = get_trade_top()
    trade_top_first = trade_top_list[0]

    trade_first_value = trade_top_first[1]
    top_rate = float(trade_first_value[3])
    print(str(datetime.datetime.now()), '最高利率的换币组合', trade_top_first)
    if top_rate >= min_rate:
        trade_first_key = trade_top_first[0]
        trade_list = trade_first_key.split('-')
        first_close = get_coin_close(trade_list[0])  # 重新获取当前价格
        second_close = get_coin_close(trade_list[1])
        third_close = get_coin_close(trade_list[2])

        if first_close > 0 and second_close > 0 and third_close > 0:
            # 格式化价格精度
            first_close = '{a:.{b}f}'.format(a=first_close, b=PRICE_PRECISION.get(trade_list[0]))
            second_close = '{a:.{b}f}'.format(a=second_close, b=PRICE_PRECISION.get(trade_list[1]))
            third_close = '{a:.{b}f}'.format(a=third_close, b=PRICE_PRECISION.get(trade_list[2]))

            coin_amount = order_amount * 0.998 / float(first_close)
            if trade_list[0].startswith('btc') or (trade_list[0].startswith('eth') and trade_list[1].endswith('eth')):
                coin_amount = coin_amount * 0.998 / float(second_close)
            else:
                coin_amount = coin_amount * 0.998 * float(second_close)
            coin_amount = coin_amount * float(third_close) * 0.998 - 1
            if coin_amount >= min_rate:
                trade_amount = order_amount / float(first_close)
                trade_amount = ('{:.' + str(AMOUNT_PRECISION.get(trade_list[0])) + 'f}').format(trade_amount)
                order_id = create_order(trade_amount, trade_list[0], 'buy-limit', first_close)

                first_coin = trade_list[0][:len('usdt') - 1]
                for i in range(300):
                    first_coin_amount = get_coin_balance(first_coin)
                    if float(first_coin_amount) > float(trade_amount):
                        break
                    time.sleep(0.01)

                if int(order_id) > 0:
                    trade_amount = float(trade_amount) * 0.998
                    if trade_list[0].startswith('btc') or (
                                trade_list[0].startswith('eth') and trade_list[1].endswith('eth')):
                        trade_amount = trade_amount / float(second_close)
                        trade_amount = ('{:.' + str(AMOUNT_PRECISION.get(trade_list[1])) + 'f}').format(trade_amount)
                        order_id = create_order(trade_amount, trade_list[1], 'buy-limit', second_close)
                        trade_amount = float(trade_amount) * 0.998
                    else:
                        trade_amount = ('{:.' + str(AMOUNT_PRECISION.get(trade_list[1])) + 'f}').format(trade_amount)
                        order_id = create_order(trade_amount, trade_list[1], 'sell-limit', second_close)
                        trade_amount = float(trade_amount) * float(second_close)
                        trade_amount = float(trade_amount) * 0.998
                    if int(order_id) > 0:
                        third_coin = trade_list[2][:len('usdt') - 1]
                        for i in range(300):
                            third_coin_amount = get_coin_balance(third_coin)
                            if float(third_coin_amount) > float(trade_amount):
                                break
                            time.sleep(0.01)

                        trade_amount = ('{:.' + str(AMOUNT_PRECISION.get(trade_list[2])) + 'f}').format(trade_amount)
                        create_order(trade_amount, trade_list[2], 'sell-limit', third_close)
                        trade_amount = float(trade_amount) * float(third_close)
                        trade_amount = float(trade_amount) * 0.998 - 1
                        print(str(datetime.datetime.now()), '当前赚取利率', first_close, second_close, third_close,
                              trade_amount)


def get_coin_close(coin_group=None):
    try:
        detail_result = get_detail(coin_group)
        if detail_result and detail_result.get('status') == 'ok':
            return detail_result.get('tick').get('close')
        else:
            print('获取币价失败', coin_group, detail_result)
            return 0
    except Exception as e:
        print('获取币价异常', coin_group, e)
        return 0


# 测试一组换币交易
def trade_process_demo(min_rate=1):
    trade_top_list = get_trade_top()
    trade_top_first = trade_top_list[0]

    trade_first_value = trade_top_first[1]
    top_rate = float(trade_first_value[3])
    print(str(datetime.datetime.now()), '最高利率的换币组合', trade_top_first)
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
            print(str(datetime.datetime.now()), '当前利率', first_close, second_close, third_close, coin_amount)


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
    # trade_top_list = get_trade_top()
    # for trade_top1 in trade_top_list:
    #     print(trade_top1)
    # print(get_accounts())
    # print(get_balance())
    # for xx in get_symbol_list():
    #     print(xx)
    # for trade_group in get_trade_group():
    #     print(trade_group)
    # print(get_trade_group())
    # print(get_one_detail('ethusdt-cvceth-cvcusdt'))
    # print(get_symbols())
    # trade_process_demo(0.001)
    # print(AMOUNT_PRECISION.get('omgusdt'))
    # print(create_order('{:.4f}'.format(1 / 10.01), 'omgusdt', 'buy-limit', 10.01))
    # print(order_info(1296036671))
    print(get_coin_balance('usdt'))
    # for i in range(20):
    #     trade_process(2, 0.003)
    #     print(get_coin_balance('usdt'))
