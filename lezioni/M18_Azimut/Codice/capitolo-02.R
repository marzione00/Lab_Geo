d <- read.csv('dati/correnti_v1.csv')
a <- d$azimut * pi / 180
f <- function(x) {
  C <- mean(cos(x)); S <- mean(sin(x))
  R <- sqrt(C^2 + S^2)
  c(dir = (atan2(S, C) * 180/pi) %% 360,
    R = R,
    sd = sqrt(-2 * log(R)) * 180/pi)
}
round(sapply(split(a, d$stazione), f), 2)
