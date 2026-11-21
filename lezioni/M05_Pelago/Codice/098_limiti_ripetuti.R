set.seed(17)
x98 <- rlnorm(30, 0, .6)
q98 <- replicate(30, {
  b <- replicate(200,
    mean(sample(x98, replace = TRUE)))
  quantile(b, .975, type = 7)
})
sd(q98)  # Variabilita numerica
