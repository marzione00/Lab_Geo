source("setup.R", encoding = "UTF-8")
range(wk$data)
nrow(wk)
sum(is.na(wk$co2))
# 2284 date, di cui 59 prive di valore.
c(osservati = sum(!is.na(wk$co2)),
  mancanti = sum(is.na(wk$co2)))
