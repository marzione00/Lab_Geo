e <- read.csv('dati/eruzioni_v1.csv')
n <- nrow(e)
T <- 3.75
g <- seq(0, 10, length.out = 4001)
dg <- g[2] - g[1]
pri <- rep(1, length(g))
ver <- dpois(n, g * T)
post <- pri * ver / sum(pri * ver * dg)
cdf <- cumsum(post * dg)
c(media = sum(g * post * dg),
  inf = g[which.max(cdf >= .025)],
  sup = g[which.max(cdf >= .975)])
