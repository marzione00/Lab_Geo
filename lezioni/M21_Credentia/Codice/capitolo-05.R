e <- read.csv('dati/eruzioni_v1.csv')
n <- nrow(e)
k <- sum(e$tipo == 'esplosiva')
pri <- rbind(uniforme = c(1, 1),
  jeffreys = c(.5, .5),
  analoghi = c(6.685, 13.354))
a1 <- pri[, 1] + k; b1 <- pri[, 2] + n - k
round(cbind(media = a1 / (a1 + b1),
  inf = qbeta(.025, a1, b1),
  sup = qbeta(.975, a1, b1)), 3)
