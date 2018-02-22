def get_price_list():
    result = get_symbols()
    result_data = result['data']
    if result_data and 'ok' == result.get('status'):
        # print(type(result_data))
        # print(len(result_data))
        range_prices = {}
        for data in result_data:
            # data = result_data[0]
            symbol = data.get('base-currency') + data.get('quote-currency')
            if data.get('quote-currency') == 'eth' or data.get('quote-currency') == 'btc' or data.get(
                    'quote-currency') == 'usdt':
                # print(symbol)
                detail_result = get_detail(symbol)
                if detail_result and detail_result.get('status') == 'ok' and detail_result.get(
                        'tick') and detail_result.get('tick').get('high'):
                    price_range = (float(detail_result.get('tick').get('high')) - float(
                        detail_result.get('tick').get('low'))) / float(detail_result.get('tick').get('open')) * 100
                    range_prices[symbol] = [price_range, detail_result.get('tick').get('open'),
                                            detail_result.get('tick').get('close'),
                                            detail_result.get('tick').get('high'), detail_result.get('tick').get('low')]
        range_prices = sorted(range_prices.items(), key=lambda x: x[1], reverse=True)
        print('币对\t涨跌幅/%\t开盘价\t收盘价\t最高价\t最低价')
        for vv in range_prices:
            print(vv[0] + '\t' + str(vv[1][0]) + '\t' + str(vv[1][1]) + '\t' + str(vv[1][2]) + '\t' + str(
                vv[1][3]) + '\t' + str(vv[1][4]))


# 获取所有交易对
def get_symbol_list():
    symbol_group = []
    result = get_symbols()
    if result.get('data') and 'ok' == result.get('status'):
        for data in result.get('data'):
            symbol_group.append(data.get('base-currency') + data.get('quote-currency'))
    return symbol_group


# 获取所有换币组合
def get_trade_group():
    result_group = []
    symbol_group_list = ALL_TRADE_PAIRS
    for symbol_group1 in symbol_group_list:
        if symbol_group1.endswith('usdt'):
            first_coin = symbol_group1[:symbol_group1.find('usdt')]
            for symbol_group2 in symbol_group_list:
                if symbol_group2 != symbol_group1:
                    if symbol_group2.endswith(first_coin):
                        start_coin = symbol_group2[0:symbol_group2.find(first_coin)]
                        third_coin = start_coin + 'usdt'
                        if third_coin in symbol_group_list:
                            result_group.append(symbol_group1 + '-' + symbol_group2 + '-' + third_coin)
                    elif symbol_group2.startswith(first_coin):
                        end_coin = symbol_group2[len(first_coin):]
                        third_coin = end_coin + 'usdt'
                        if third_coin in symbol_group_list:
                            result_group.append(symbol_group1 + '-' + symbol_group2 + '-' + third_coin)
    return result_group