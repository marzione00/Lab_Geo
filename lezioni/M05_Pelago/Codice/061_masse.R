x61 <- c(4, 5, 7, 8)
p61 <- rep(1/4, 4)
sum(p61)       # Probabilita totale
sum(x61*p61)   # Media empirica: 6
# Ogni posizione ha probabilita 1/4
data.frame(valore = x61, p = p61)
