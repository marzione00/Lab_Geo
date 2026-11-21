# Nuovo esempio: tipo T e segnale S
N15 <- 1000
nT15 <- N15 * .10
segnali15 <- c(T = nT15*.90,
  altri = (N15-nT15)*.05)
segnali15           # 90 e 45
segnali15["T"] / sum(segnali15)
# Due terzi dei segnali attesi
