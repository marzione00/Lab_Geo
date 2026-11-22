set.seed(17)
x70 <- rlnorm(30, 0, .6)
set.seed(17)
m70 <- replicate(2000,
  median(sample(x70, replace = TRUE)))
median(x70)
quantile(m70, c(.025, .975),
         type = 7)
