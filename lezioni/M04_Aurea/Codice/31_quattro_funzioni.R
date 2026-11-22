# d: probabilita del valore
dbinom(8, 20, .3)
# p: probabilita cumulata
pbinom(8, 20, .3)
# q: primo k con F(k) >= .95
qbinom(.95, 20, .3)
# r: cinque conteggi simulati
set.seed(17)
rbinom(5, size = 20, prob = .3)
