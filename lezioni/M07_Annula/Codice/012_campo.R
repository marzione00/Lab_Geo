# Stessa legge, due campi del predittore.
set.seed(17)
u <- runif(1000, -4, 4)
v <- 2 * u + rnorm(1000)
centrali <- abs(u) < 1
c(intero = cor(u, v),
  ristretto = cor(u[centrali],
                 v[centrali]))
