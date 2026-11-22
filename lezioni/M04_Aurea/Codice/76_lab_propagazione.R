a76 <- lab_propagazione(
  rho = 0, cv = .1, seed = 17)
b76 <- lab_propagazione(
  rho = .7, cv = .1, seed = 17)
c76 <- lab_propagazione(
  rho = 0, cv = .3, seed = 17)
rbind(A = a76$indicatori,
      B = b76$indicatori,
      C = c76$indicatori)
