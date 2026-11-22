rapporto <- c("PROGETTO MORFOMETRICO: DATI SINTETICI",
   "Domanda: prevedere il diametro interno a partire dal totale.",
   sprintf("Train: %d individui; test: %d, ogni quinta riga.",nrow(tr),nrow(te)),
   sprintf("Retta stimata: interno = %.4f + %.4f * totale (micrometri).",coef(mod)[1],coef(mod)[2]),
   sprintf("RMSE media train: %.4f micrometri; regressione: %.4f.",m0["RMSE"],m1["RMSE"]),
   sprintf("Differenza RMSE riferimento meno modello: %.4f micrometri.",m0["RMSE"]-m1["RMSE"]),
   "Limiti: dati simulati, misure geometricamente legate, un solo holdout noto.",
   "La previsione non dimostra causalita fisica; servono nuovi dati e un protocollo prospettico.")
 cat(paste(rapporto,collapse="
"))
