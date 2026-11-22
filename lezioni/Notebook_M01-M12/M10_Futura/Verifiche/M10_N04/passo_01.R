c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
fit <- stima_sarima(train)
 res <- as.numeric(residuals(fit))
 res <- res[seq.int(14,length(res))]
 res <- res[is.finite(res)]
 data.frame(n=length(res),media=mean(res),sd=sd(res),min=min(res),max=max(res))
 stile_grafico()
 plot(res,type="l",col=palette_geo[1],xlab="Indice residuo",ylab="Residuo (ppm)",
      main="Innovazioni stimate nel train")
 abline(h=0,lty=2)
