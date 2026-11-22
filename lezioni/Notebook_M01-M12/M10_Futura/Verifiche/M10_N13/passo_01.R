f <- carica_dati("fossili_simulati.csv"); s <- prepara_fossili(f)
tr <- s$train; te <- s$test
mod <- lm(diametro_int_um~diametro_tot_um,data=tr)
prev <- as.numeric(predict(mod,newdata=te))
base <- rep(mean(tr$diametro_int_um),nrow(te))
m0 <- metriche(te$diametro_int_um,base); m1 <- metriche(te$diametro_int_um,prev)
confronto <- data.frame(modello=c("Media_train","Regressione"),
  MAE=c(m0["MAE"],m1["MAE"]),RMSE=c(m0["RMSE"],m1["RMSE"]))
audit <- data.frame(controllo=c("ID unici","Diametri completi","Totale positivo","Interno entro totale"),
  esito=c(!anyDuplicated(f$id),!anyNA(f[c("diametro_tot_um","diametro_int_um")]),
    all(f$diametro_tot_um>0),all(f$diametro_int_um>0 & f$diametro_int_um<=f$diametro_tot_um)))
stopifnot(all(audit$esito))
confronto
