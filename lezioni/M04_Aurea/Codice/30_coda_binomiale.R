# Almeno 8: sommare k = 8,...,20
sum(dbinom(8:20, 20, .3))
# lower.tail=FALSE calcola P(K>q)
pbinom(7, size = 20, prob = .3,
       lower.tail = FALSE)
# P(K=8) e' una sola probabilita
dbinom(8, 20, .3)
