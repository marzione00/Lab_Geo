# Due modelli con media e varianza 1
set.seed(17)
a27 <- rnorm(200, mean = 1, sd = 1)
b27 <- rexp(200, rate = 1)
c(mean(a27), var(a27))
c(mean(b27), var(b27))
