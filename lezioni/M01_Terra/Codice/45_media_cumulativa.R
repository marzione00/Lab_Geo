set.seed(17)
x <- rexp(1000, rate = 1)
# Medie delle prime 1, 2, ..., 1000 misure
m <- cumsum(x) / seq_along(x)
