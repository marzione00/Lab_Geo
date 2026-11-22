n39 <- 60
rho39 <- .2
deff39 <- 1 + (n39-1)*rho39
c(SE = sqrt(deff39/n39),
  n_eff = n39/deff39)
# Varianza marginale fissata a 1
