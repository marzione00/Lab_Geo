# n: osservazioni; B: campioni
a35 <- lab_distribuzioni(
  n = 12, B = 1000,
  population = "exp", seed = 17)
b35 <- lab_distribuzioni(
  n = 60, B = 1000,
  population = "exp", seed = 17)
a35$indicatori
b35$indicatori
