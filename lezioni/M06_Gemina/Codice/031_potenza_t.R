# n indica la numerosita' di ogni gruppo
pt31 <- power.t.test(n = 30,
  delta = 0.5, sd = 1, sig.level = 0.05,
  type = "two.sample",
  alternative = "two.sided",
  strict = TRUE)
pt31$power
