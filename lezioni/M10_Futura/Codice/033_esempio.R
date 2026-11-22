set.seed(101033)
x_ma <- arima.sim(list(ma=0.6),
                  n=240)
head(x_ma)
