d <- read.csv('dati/correnti_v1.csv')
a <- d$azimut * pi / 180
A <- function(k) besselI(k, 1, TRUE) /
  besselI(k, 0, TRUE)
kap <- function(x) {
  R <- sqrt(mean(cos(x))^2 +
    mean(sin(x))^2)
  uniroot(function(k) A(k) - R,
    c(1e-6, 500))$root
}
k <- sapply(split(a, d$stazione), kap)
round(k, 2)
