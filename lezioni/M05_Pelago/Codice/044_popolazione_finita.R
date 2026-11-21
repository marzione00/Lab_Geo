pop44 <- c(2, 4, 6, 8, 10)
m44 <- colMeans(combn(pop44, 2))
# Varianza esatta sui 10 campioni
mean((m44-mean(pop44))^2)
# Formula senza reinserimento
(1-2/length(pop44))*var(pop44)/2
