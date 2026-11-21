# na40 e nb40: numerosita' gia' calcolate
sp45 <- sqrt(((na40 - 1) * var(a37) +
  (nb40 - 1) * var(b37)) /
  (na40 + nb40 - 2))
d45 <- d39 / sp45
glass45 <- d39 / sd(a37)
c(d_pooled = d45, rispetto_A = glass45)
