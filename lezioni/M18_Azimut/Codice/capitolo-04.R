d <- read.csv('dati/correnti_v1.csv')
ray <- function(g) {
  a <- d$azimut[d$stazione == g] * pi/180
  n <- length(a)
  Z <- n * (mean(cos(a))^2 +
    mean(sin(a))^2)
  p <- exp(-Z) * (1 + (2*Z - Z^2)/(4*n) -
    (24*Z - 132*Z^2 + 76*Z^3 - 9*Z^4) /
    (288 * n^2))
  c(n = n, Z = Z, p = p)
}
round(sapply(c('S1', 'S6'), ray), 4)
