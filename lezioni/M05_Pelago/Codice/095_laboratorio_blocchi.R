r95 <- lab_blocchi(length = 8,
  rho = .7, B = 200, seed = 17)
r95$indicatori
r95b <- lab_blocchi(length = 1,
  rho = .7, B = 200, seed = 17)
r95b$indicatori
identical(r95$campione,
          r95b$campione) # TRUE
