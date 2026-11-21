from statistics import mean
v = [40, None, 50]
ok = [x for x in v if x is not None]
print(len(ok), mean(ok))
