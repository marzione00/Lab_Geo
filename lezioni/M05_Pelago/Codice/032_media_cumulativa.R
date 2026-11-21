set.seed(17)
x32 <- rexp(200)
n32 <- seq_along(x32)
mc32 <- cumsum(x32) / n32
plot(n32, mc32, type = "l",
  xlab = "n", ylab = "Media")
abline(h = 1, lty = 2)
