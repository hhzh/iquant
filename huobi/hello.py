from huobi.HuobiServices import *

# name = 'omgusdt'
# print(name.replace('usdt', 'btc'))
# print(name)
# print(name[len('omg'):])
# print('{a:.{b}f}'.format(a=1 / 11, b=AMOUNT_PRECISION.get('omgusdt')))
# print(1 / 11.01)

try:
    ab = 9 / 0
except Exception as e:
    print(e)
    print(type(e))
