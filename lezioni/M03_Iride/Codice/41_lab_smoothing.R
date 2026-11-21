sA <- lab_smoothing(bins = 18,
  bw = .5, seed = 17)
sB <- lab_smoothing(bins = 8,
  bw = .5, seed = 17)
sC <- lab_smoothing(bins = 8,
  bw = 1.5, seed = 17)
identical(sA$dati, sB$dati)  # TRUE
identical(sA$dati, sC$dati)  # TRUE
