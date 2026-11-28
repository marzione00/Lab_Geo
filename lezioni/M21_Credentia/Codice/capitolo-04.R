# parametri a posteriori del frammento 3
A1 <- 14.147; B1 <- 5.557; h <- 0.5
c(predittiva = 1 - (B1 / (B1 + h))^A1,
  con_stima = 1 - exp(-h * 9 / 3.75))
set.seed(1)
l <- rgamma(1e5, A1, B1)
mean(1 - exp(-h * l))
