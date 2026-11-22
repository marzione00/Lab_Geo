set.seed(19082)
t82 <- 1:200
x82 <- 10 + 0.04 * t82 + rnorm(200)
r82 <- residuals(lm(x82 ~ t82))
d82 <- diff(x82)
# Lo stesso input, due resti differenti.
c(detrend = acf(r82, plot = FALSE)$acf[2],
  differenza = acf(d82, plot = FALSE)$acf[2])
