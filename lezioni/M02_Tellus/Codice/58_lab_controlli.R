set.seed(17)
temp_lab <- c(rnorm(29, 15, 3), 250)
valido_lab <- temp_lab >= -50 &
              temp_lab <= 60
c(segnalate = sum(!valido_lab),
  media = mean(temp_lab))
# La media usa ancora tutte le righe
