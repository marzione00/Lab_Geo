# Livello predefinito: 0.05
r34 <- power.t.test(delta = 0.5,
  sd = 1, power = 0.8,
  type = "two.sample", strict = TRUE)
ceiling(r34$n)  # 64 per gruppo
