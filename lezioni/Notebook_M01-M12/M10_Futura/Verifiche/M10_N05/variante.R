o <- 156L
tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
obs <- as.numeric(train)[157:168]
pr <- as.numeric(predict(stima_sarima(tr),n.ahead=12)$pred)
rbind(SARIMA=metriche(obs,pr),Stagionale=metriche(obs,tail(tr,12)))
