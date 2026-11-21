head(d, 5)
str(d)
# Tre ruoli: data, concentrazione, copertura.
stopifnot(inherits(d$data, "Date"),
  is.numeric(d$co2_ppm),
  all(d$n_settimane >= 0))
