p24 <- c(0.049, 0.051)
t24 <- qt(1 - p24 / 2, df = 20)
data.frame(p = p24, t = t24,
  rifiuto = p24 <= 0.05)
