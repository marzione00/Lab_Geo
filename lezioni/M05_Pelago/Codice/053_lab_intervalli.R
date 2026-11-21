b53 <- lab_intervalli(
  n = 30, B = 200, rho = .2,
  level = .95, seed = 17)
b53$indicatori
c53 <- mean(b53$dati$copre)
# SE Monte Carlo della copertura
sqrt(c53*(1-c53)/200)
