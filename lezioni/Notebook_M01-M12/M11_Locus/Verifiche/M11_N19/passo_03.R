osservato <- d$concentrazione[te]
metriche_test <- as.data.frame(do.call(rbind,lapply(previsioni[,4:6],function(pr) metriche(osservato,pr))))
metriche_test$metodo <- rownames(metriche_test);rownames(metriche_test) <- NULL
metriche_test
previsioni$osservato <- osservato;previsioni$errore_IDW <- osservato-pred_idw
stile_grafico()
plot(previsioni$x_m,previsioni$errore_IDW,pch=19,col=palette_geo[1],
  xlab="x del bersaglio escluso (m)",ylab="Osservato - IDW p2 (u.a.)",main="Errori nel settore Est escluso")
abline(h=0,lty=2,col="grey50")
write.csv(metriche_test,percorso_risultati("metriche_test_spaziale.csv"),row.names=FALSE)
write.csv(previsioni,percorso_risultati("previsioni_test_spaziale.csv"),row.names=FALSE)
