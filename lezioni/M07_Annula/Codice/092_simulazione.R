# Nuovi dati dalla stessa legge.
set.seed(17)
sim <- data.frame(
  x = seq(-1, 1, length.out = 24))
sim$y <- sin(3 * sim$x) + rnorm(24)
mp <- lm(y ~ poly(x, 3, raw = TRUE),
         data = sim)
nuovi <- data.frame(
  x = seq(-1, 1, length.out = 150))
nuovi$y <- sin(3 * nuovi$x) + rnorm(150)
metriche(nuovi$y,
  predict(mp, newdata = nuovi))
