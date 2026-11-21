# Confronto sul segmento completo.
forme76 <- list(livelli = y,
  ordinaria = diff(y),
  stagionale = diff(y, lag = 12),
  combinata = diff(diff(y, lag = 12)))
sapply(forme76, length)
sapply(forme76, start)
