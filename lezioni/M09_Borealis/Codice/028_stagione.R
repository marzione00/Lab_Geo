# Una linea per ogni anno del segmento.
yr <- as.integer(format(d$data, "%Y"))
mo <- as.integer(format(d$data, "%m"))
matplot(1:12, sapply(c(1985, 1992, 2001),
  function(a) d$co2_ppm[yr == a]),
  type = "l", lty = 1, xlab = "Mese",
  ylab = "CO2 (ppm)")
