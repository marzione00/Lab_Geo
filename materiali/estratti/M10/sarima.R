d <- read.csv('dati/co2_1985_2001.csv')
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
tr <- window(y,end=c(1998,12))
f <- arima(tr,order=c(0,1,1),
 seasonal=list(order=c(0,1,1),period=12),
 include.mean=FALSE,method='ML')
stopifnot(f$code==0)
coef(f)
sqrt(diag(f$var.coef))
