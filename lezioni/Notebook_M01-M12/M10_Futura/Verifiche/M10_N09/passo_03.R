ritorno <- read.csv(percorso_risultati("previsioni_test.csv"),stringsAsFactors=FALSE)
fit2 <- readRDS(percorso_risultati("modello_SARIMA.rds"))
stopifnot(nrow(ritorno)==36L,identical(ritorno$data,tab$data),
  isTRUE(all.equal(ritorno$previsto,tab$previsto,tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(predict(fit2,n.ahead=h)$pred),tab$previsto)))
data.frame(controllo=c("36 righe","Date identiche","Valori riletti","Previsione da RDS"),esito=TRUE)
