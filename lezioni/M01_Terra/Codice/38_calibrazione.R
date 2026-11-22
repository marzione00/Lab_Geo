# Letture didattiche in gradi C
letture <- c(20.2, 20.3, 20.4)
riferimento <- 20
scarto <- mean(letture) - riferimento
sd(letture)  # Dispersione ripetizioni
# Correzione dello scarto accertato
corrette <- letture - scarto
mean(corrette)
