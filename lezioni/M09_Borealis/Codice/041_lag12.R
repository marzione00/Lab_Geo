n41 <- nrow(d)
coppie12 <- data.frame(
  data = d$data[13:n41],
  passato = head(d$co2_ppm, -12),
  presente = tail(d$co2_ppm, -12))
head(coppie12, 3)
stopifnot(nrow(coppie12) == 192L)
