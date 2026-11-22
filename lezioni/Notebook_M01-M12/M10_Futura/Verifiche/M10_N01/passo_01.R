d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
stopifnot(!anyDuplicated(d$data), !anyNA(d$co2_ppm))
stopifnot(identical(d$data,seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")))
data.frame(prima=min(d$data),ultima=max(d$data),mesi=nrow(d),
           minimo_settimane=min(d$n_settimane))
