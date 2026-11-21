# E[X^2] per X normale standard
set.seed(17)
B57 <- 5000
x57 <- rnorm(B57)
y57 <- x57^2
c(stima = mean(y57), teoria = 1)
