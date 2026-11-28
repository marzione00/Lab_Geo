a <- read.csv('dati/analoghi_v1.csv')
Ta <- a$anni_osservati / 100
nll <- function(q) -sum(dnbinom(
  a$eruzioni, size = exp(q[1]),
  mu = exp(q[1] - q[2]) * Ta, log = TRUE))
q <- optim(c(1, 0), nll,
  control = list(reltol = 1e-12))$par
A <- exp(q[1]); B <- exp(q[2])
A1 <- A + 9; B1 <- B + 3.75
round(c(A = A, B = B, A1 = A1, B1 = B1,
  media = A1 / B1), 3)
round(qgamma(c(.025, .975), A1, B1), 3)
