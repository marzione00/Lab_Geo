f <- carica_dati("fossili_simulati.csv")
s <- prepara_fossili(f); tr <- s$train; te <- s$test
data.frame(insieme=c("Train","Test"),n=c(nrow(tr),nrow(te)))
stopifnot(nrow(tr)==128L,nrow(te)==32L,!any(tr$id %in% te$id))
table(insieme=ifelse(f$id %in% te$id,"Test","Train"),morfotipo=f$morfotipo)
