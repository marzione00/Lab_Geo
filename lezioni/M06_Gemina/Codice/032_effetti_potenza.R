# Sensibilita' a tre effetti prefissati
sapply(c(0.2, 0.5, 0.8), function(d) {
  power.t.test(n = 60, delta = d,
    sd = 1, sig.level = 0.05,
    type = "two.sample",
    strict = TRUE)$power
})
