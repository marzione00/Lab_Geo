x <- c(3.1, 3.4, 2.8, 3, 3.2)
n <- length(x)
errore_std <- sd(x) / sqrt(n)
q <- qt(0.975, df = n - 1)
# Estremi inferiore e superiore
mean(x) + c(-1, 1) * q * errore_std
