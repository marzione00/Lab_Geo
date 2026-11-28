# Regressione di York e colleghi (2004) con errori non correlati.
york <- function(x, sx, y, sy) {
  wx <- 1 / sx^2; wy <- 1 / sy^2
  b <- coef(lm(y ~ x))[[2]]
  for (k in 1:100) {
    W <- wx * wy / (wx + b^2 * wy)
    X <- sum(W * x) / sum(W)
    Y <- sum(W * y) / sum(W)
    U <- x - X; V <- y - Y
    be <- W * (U / wy + b * V / wx)
    b <- sum(W * be * V) / sum(W * be * U)
  }
  a <- Y - b * X
  u <- be - sum(W * be) / sum(W)
  sb <- sqrt(1 / sum(W * u^2))
  sa <- sqrt(1 / sum(W) + (X + sum(W * be) / sum(W))^2 * sb^2)
  S <- sum(W * (y - a - b * x)^2)
  c(a = a, sa = sa, b = b, sb = sb,
    mswd = S / (length(x) - 2))
}
