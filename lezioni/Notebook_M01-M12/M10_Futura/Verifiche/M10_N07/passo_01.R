c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
fit <- stima_sarima(train)
 pred <- baseline_co2(train,h)[c("Ultimo","Stagionale","Deriva")]
 pred$SARIMA <- as.numeric(predict(fit,n.ahead=h)$pred)
 stopifnot(all(vapply(pred,length,integer(1))==length(test)))
 data.frame(h=1:3,osservato=as.numeric(test)[1:3],
            previsto_SARIMA=pred$SARIMA[1:3])
