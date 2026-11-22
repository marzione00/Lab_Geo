G41 <- 6   # Stazioni indipendenti
m41 <- 4   # Provini per stazione
rho41 <- .6
deff41 <- 1 + (m41-1)*rho41
n41 <- G41*m41
c(DEFF = deff41, n_eff = n41/deff41)
