set.seed(19064)
e64 <- rnorm(150)
# X0 = 0. cumsum conserva gli shock.
rw64 <- c(0, cumsum(e64))
plot(0:150, rw64, type = "l",
     xlab = "Tempo", ylab = "X")
stopifnot(isTRUE(all.equal(
  diff(rw64), e64)))
