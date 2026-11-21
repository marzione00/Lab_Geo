set.seed(19066)
B66 <- 2000
# Ogni colonna usa innovazioni nuove.
rw66 <- replicate(B66, cumsum(rnorm(100)))
# Varianza tra repliche, a tempo fissato.
v66 <- apply(rw66, 1, var)
round(v66[c(1, 25, 100)], 1)
