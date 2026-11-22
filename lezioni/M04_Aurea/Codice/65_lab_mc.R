a65 <- lab_monte_carlo(
  B = 200, prob = .1, seed = 17)
b65 <- lab_monte_carlo(
  B = 800, prob = .1, seed = 17)
a65$indicatori
b65$indicatori
a65$indicatori["se_mc_teorico"] /
  b65$indicatori["se_mc_teorico"]
