set.seed(17)
lab_x <- rlnorm(200, 1, 0.5)
lab_assenti <- rank(lab_x) > 140
c(mancanti = sum(lab_assenti),
  completa = mean(lab_x),
  disponibile = mean(
    lab_x[!lab_assenti]))
