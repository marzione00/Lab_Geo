c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
fit <- stima_sarima(train)
 fc <- predict(fit,n.ahead=h)
 p <- data.frame(data=c2$date_test,h=1:h,osservato=as.numeric(test),
   previsto=as.numeric(fc$pred),se=as.numeric(fc$se))
 p$inferiore <- p$previsto-qnorm(.975)*p$se
 p$superiore <- p$previsto+qnorm(.975)*p$se
 p$errore <- p$osservato-p$previsto
 p$dentro95 <- p$osservato>=p$inferiore & p$osservato<=p$superiore
 head(p,4)
