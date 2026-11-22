# Ingressi indipendenti, positivi
set.seed(17)
B68 <- 20000
m68 <- rpos(B68, 106, 1)
v68 <- rpos(B68, 40, .6)
d68 <- m68/v68
c(media = mean(d68), SD = sd(d68))
quantile(d68, c(.025, .975))
