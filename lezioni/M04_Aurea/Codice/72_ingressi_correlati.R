set.seed(17)
s72 <- .1; c72 <- .7
z72 <- matrix(rnorm(4000), ncol = 2)
u72 <- z72[, 1]
v72 <- c72*u72 +
  sqrt(1-c72^2)*z72[, 2]
x72 <- exp(log(10)+s72*u72)
y72 <- exp(log(5)+s72*v72)
r72 <- x72/y72
sd(r72)
