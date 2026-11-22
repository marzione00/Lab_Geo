# Modello didattico con media nota
mu06 <- 10
set.seed(17)
x06 <- rnorm(6,mean=mu06,sd=2)
mean(x06)  # stima ottenuta dai dati
# La regola vale per ogni campione.
stimatore06 <- function(x) mean(x)
stimatore06(x06)
