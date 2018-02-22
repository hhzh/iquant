d = {'zhang': 13, 'li': 88, 'uu': 33}
d = sorted(d.items(), key=lambda x: x[1], reverse=True)
print(d)
print('你好\tdfef')
for vv in d:
    print(vv[0] + '\t' + str(vv[1]))
