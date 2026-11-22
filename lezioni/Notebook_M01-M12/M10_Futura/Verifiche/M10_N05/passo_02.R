dettaglio <- do.call(rbind,lapply(origini,function(o) {
  tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
  obs <- as.numeric(train)[(o+1):(o+12)]
  mod <- stima_sarima(tr)
  pr <- as.numeric(predict(mod,n.ahead=12)$pred)
  sn <- as.numeric(tail(tr,12))
  data.frame(origine=o,h=1:12,osservato=obs,SARIMA=pr,Stagionale=sn)
}))
cv <- do.call(rbind,lapply(split(dettaglio,dettaglio$origine),function(d) {
  data.frame(origine=d$origine[1],RMSE_SARIMA=metriche(d$osservato,d$SARIMA)["RMSE"],
             RMSE_Stagionale=metriche(d$osservato,d$Stagionale)["RMSE"])
}))
rownames(cv) <- NULL
cv
