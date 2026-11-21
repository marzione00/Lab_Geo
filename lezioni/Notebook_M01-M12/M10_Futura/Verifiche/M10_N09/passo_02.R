saveRDS(fit,percorso_risultati("modello_SARIMA.rds"))
 cv <- do.call(rbind,lapply(c(120L,132L,144L),function(o) {
   tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
   osservato <- as.numeric(train)[o+1:12]
   previsto <- as.numeric(predict(stima_sarima(tr),n.ahead=12)$pred)
   stagionale <- as.numeric(tail(tr,12))
   data.frame(origine=o,RMSE_SARIMA=metriche(osservato,previsto)["RMSE"],
     RMSE_stagionale=metriche(osservato,stagionale)["RMSE"])
 }))
 rownames(cv) <- NULL
 write.csv(cv,percorso_risultati("validazione_interna_train.csv"),row.names=FALSE)
 cv
 protocollo <- c("CO2 storica: aggregazione mensile del corso, ppm.",
   "Train 1985-01/1998-12. Test 1999-01/2001-12.",
   "Origine fissa dicembre 1998, 36 mesi, nessun aggiornamento nel test.",
   "SARIMA(0,1,1)(0,1,1)[12], ML, senza drift.",
   "Intervalli gaussiani puntuali condizionali. Incertezza dei parametri esclusa.",
   paste("Runtime:",R.version.string),capture.output(met))
 writeLines(protocollo,percorso_risultati("protocollo.txt"),useBytes=TRUE)
 cat(paste(protocollo,collapse="
"))
