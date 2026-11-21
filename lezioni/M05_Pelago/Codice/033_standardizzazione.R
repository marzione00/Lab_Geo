set.seed(17)
n33 <- 60
m33 <- replicate(1000,
  mean(rexp(n33)))
z33 <- sqrt(n33) * (m33 - 1)
c(media = mean(z33), sd = sd(z33))
