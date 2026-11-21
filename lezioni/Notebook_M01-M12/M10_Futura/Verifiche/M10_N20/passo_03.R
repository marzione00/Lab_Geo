obs18 <- as.numeric(test)[1:h18]
fit <- stima_sarima(train)
ar18 <- as.numeric(predict(fit,n.ahead=h18)$pred)
rbind(Stagionale=metriche(obs18,pred18),SARIMA=metriche(obs18,ar18))
write.csv(data.frame(data=c2$date_test[1:h18],osservato=obs18,
  stagionale=pred18,SARIMA=ar18),percorso_risultati("baseline_18_mesi.csv"),row.names=FALSE)
