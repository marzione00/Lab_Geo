set.seed(6035)
x35 <- rnorm(100)  # H0: media zero
n35 <- seq(10, 100, 10)
z35 <- cumsum(x35)[n35] / sqrt(n35)
any(abs(z35) > qnorm(0.975))
# Un percorso; la figura ne ripete 5000.
