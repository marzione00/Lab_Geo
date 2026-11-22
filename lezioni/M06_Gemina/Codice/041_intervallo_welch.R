q41 <- qt(0.975, df = nu40)
ic41 <- d39 + c(-1, 1) * q41 * se38
p41 <- 2 * pt(-abs(t39), df = nu40)
c(minimo = ic41[1], massimo = ic41[2],
  p = p41)
