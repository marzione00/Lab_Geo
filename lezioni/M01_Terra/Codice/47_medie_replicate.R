set.seed(17)
n <- 30  # Valori in ogni campione
medie <- replicate(3000, mean(rexp(n)))
z <- sqrt(n) * (medie - 1)
