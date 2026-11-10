d <- read.csv('dati/co2_1985_2001.csv')
tr <- ts(d$co2_ppm[1:168],start=c(1985,1),frequency=12)
f <- arima(tr,c(0,1,1),seasonal=list(order=c(0,1,1),
 period=12),include.mean=FALSE,method='ML')
p <- predict(f,n.ahead=36)
media <- as.numeric(p$pred); se <- as.numeric(p$se)
limiti <- cbind(media-1.96*se,media+1.96*se)
stopifnot(length(media)==36,all(se>0))
