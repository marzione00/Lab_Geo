alternativo <- arima(train,order=c(0,1,0),
  seasonal=list(order=c(0,1,1),period=12),include.mean=FALSE,method="ML")
stopifnot(is.null(alternativo$code)||alternativo$code==0L)
data.frame(modello=c("MA1 e MA stagionale","Solo MA stagionale"),
           AIC=c(AIC(fit),AIC(alternativo)))
