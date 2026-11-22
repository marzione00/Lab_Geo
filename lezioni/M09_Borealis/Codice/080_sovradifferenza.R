set.seed(19080)
e80 <- rnorm(10000)
de80 <- diff(e80)
r80 <- acf(de80, lag.max = 10,
           plot = FALSE)$acf
round(c(varianza = var(de80),
        acf1 = r80[2]), 3)
acf(de80, lag.max = 10)
