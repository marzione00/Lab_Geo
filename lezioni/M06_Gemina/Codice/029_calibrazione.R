set.seed(6029)
# Z standard normale sotto H0
z29 <- rnorm(5000)
p29 <- 2 * pnorm(-abs(z29))
mean(p29 <= 0.05)
# Frequenza Monte Carlo, non identita'
