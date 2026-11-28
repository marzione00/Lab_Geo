e <- read.csv('dati/eruzioni_v1.csv')
n <- nrow(e); T <- (2025 - 1650) / 100
c(eruzioni = n, secoli = T, stima = n / T)
# intervallo esatto al 95%
c(qchisq(.025, 2 * n) / 2 / T,
  qchisq(.975, 2 * n + 2) / 2 / T)
# almeno un'eruzione in mezzo secolo
1 - exp(-0.5 * n / T)
