metriche <- function(osservato, previsto) {
  e <- osservato - previsto
  c(MAE = mean(abs(e)),
    RMSE = sqrt(mean(e^2)))
}
# Esempio con scarti noti.
metriche(c(0, 0, 0), c(1, 1, 4))
