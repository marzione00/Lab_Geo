massa = [107.2, 121.95, 132.5]
volume = [40, 45, 50]
print([round(m/v, 2) for m, v
       in zip(massa, volume, strict=True)])
