# Una prova: evento presente = 1
set.seed(17)
x26 <- rbinom(12, size = 1,
             prob = .3)
x26
mean(x26)  # Frequenza osservata
# Media e varianza del modello
c(media = .3, varianza = .3*.7)
