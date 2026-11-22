set.seed(101037)
x_arma <- arima.sim(
  list(ar=0.65,ma=0.4), n=240)
acf(x_arma, plot=FALSE)$acf[1:6]
