# Esattamente 2 successi su 3
p28 <- .3
choose(3, 2) * p28^2 * (1-p28)
dbinom(2, size = 3, prob = p28)
# Esattamente 8 su 20
dbinom(8, size = 20, prob = .3)
