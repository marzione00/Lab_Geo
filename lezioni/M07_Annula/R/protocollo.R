# Formule fissate prima di osservare i risultati sul test.
formule_annula <- function() {
  list(lineare = diametro_int_um ~ diametro_tot_um,
       con_morfotipo = diametro_int_um ~ diametro_tot_um + morfotipo,
       polinomio3 = diametro_int_um ~ poly(diametro_tot_um, 3, raw = TRUE))
}

# Ogni modello usa gli stessi fold del training.
# Restituisce la media delle metriche dei cinque fold, come nel laboratorio.
valida_annula <- function(training, fold, formule) {
  stopifnot(length(fold) == nrow(training), !anyNA(fold))
  risultati <- lapply(names(formule), function(nome) {
    per_fold <- lapply(sort(unique(fold)), function(k) {
      stima <- training[fold != k, , drop = FALSE]
      controllo <- training[fold == k, , drop = FALSE]
      mod <- lm(formule[[nome]], data = stima)
      pred <- predict(mod, newdata = controllo)
      err <- controllo$diametro_int_um - pred
      c(MAE = mean(abs(err)), RMSE = sqrt(mean(err^2)))
    })
    medie <- colMeans(do.call(rbind, per_fold))
    data.frame(modello = nome, MAE = unname(medie["MAE"]),
               RMSE = unname(medie["RMSE"]))
  })
  do.call(rbind, risultati)
}
