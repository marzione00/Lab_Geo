a52 <- lab_intervalli(
  n = 30, B = 200, rho = 0,
  level = .95, seed = 17)
sum(a52$dati$copre)  # 187 su 200
mean(a52$dati$copre)
a52$indicatori
