from huobi.HuobiServices import *
import sys
import os

# name = 'omgusdt'
# print(name.replace('usdt', 'btc'))
# print(name)
# print(name[len('omg'):])
print('{a:.{b}f}'.format(a=8 / 11, b=AMOUNT_PRECISION.get('omgusdt')))
# print(1 / 11.01)
print(('{:.' + str(AMOUNT_PRECISION.get('omgusdt')) + 'f}').format(8 / 11))
print('{:.4f}'.format(18/11))
print('{:.1f}'.format(18/11))
print('{:.0f}'.format(8/11))

# try:
#     ab = 9 / 0
# except Exception as e:
#     print(e)
#     print(type(e))

# apath = os.path.abspath(__file__)
# print(apath)
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
