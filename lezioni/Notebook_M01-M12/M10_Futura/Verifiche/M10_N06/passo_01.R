c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
fit <- stima_sarima(train)
 fc <- predict(fit,n.ahead=h)
 previsione <- data.frame(data=c2$date_test,h=1:h,
   media=as.numeric(fc$pred),se=as.numeric(fc$se))
 head(previsione,6)
 stopifnot(all(is.finite(previsione$se)),all(previsione$se>=0))
