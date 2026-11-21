registro <- data.frame(
  data = d$data,
  co2_ppm = d$co2_ppm,
  n_settimane = d$n_settimane)
attr(registro, "definizione") <-
  "Media delle settimane assegnate al mese"
head(registro, 3)
# Le colonne derivate verranno aggiunte dopo.
