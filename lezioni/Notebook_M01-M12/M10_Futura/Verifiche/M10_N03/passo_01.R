c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
 fit <- stats::arima(train,order=c(0,1,1),
   seasonal=list(order=c(0,1,1),period=12),
   include.mean=FALSE,method="ML")
 fit
 stopifnot(is.null(fit$code) || fit$code==0L)
