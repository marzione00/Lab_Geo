confronto <- data.frame(
  data = d$data,
  livello = as.numeric(y),
  diff1 = c(NA, as.numeric(delta1)),
  diff12 = c(rep(NA, 12), as.numeric(delta12)),
  combinata = c(rep(NA, 13), as.numeric(deltaC)))
head(confronto, 15)
