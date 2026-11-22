mese_w <- format(wk$data, "%Y-%m")
gruppi_w <- split(wk$co2, mese_w)
media_m <- vapply(gruppi_w, function(v) {
  if (all(is.na(v))) NA_real_
  else mean(v, na.rm = TRUE)
}, numeric(1))
n_m <- vapply(gruppi_w, function(v)
  sum(!is.na(v)), integer(1))
head(cbind(media_m, n_m))
