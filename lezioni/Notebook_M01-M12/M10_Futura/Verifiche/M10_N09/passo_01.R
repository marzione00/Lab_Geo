c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
fit <- stima_sarima(train)
 fc <- predict(fit,n.ahead=h)
 tab <- data.frame(origine="1998-12-01",data=as.character(c2$date_test),h=1:h,
   osservato=as.numeric(test),previsto=as.numeric(fc$pred),
   inferiore95=as.numeric(fc$pred-qnorm(.975)*fc$se),
   superiore95=as.numeric(fc$pred+qnorm(.975)*fc$se),unita="ppm")
 write.csv(tab,percorso_risultati("previsioni_test.csv"),row.names=FALSE)
 pr <- baseline_co2(train,h)[c("Ultimo","Stagionale","Deriva")]
 pr$SARIMA <- tab$previsto
 met <- as.data.frame(do.call(rbind,lapply(pr,function(z) metriche(tab$osservato,z))))
 met$modello <- rownames(met); rownames(met) <- NULL
 write.csv(met,percorso_risultati("metriche_test.csv"),row.names=FALSE)
 head(tab,3)
 met
