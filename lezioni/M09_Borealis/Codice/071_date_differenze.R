dy71 <- diff(y)
# Ogni differenza assume la data finale.
tab71 <- data.frame(
  data = tail(d$data, -1),
  incremento_ppm = as.numeric(dy71))
head(tab71)
c(n = length(dy71), start(dy71))
