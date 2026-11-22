# Modello costruito per un conteggio
k08 <- 0:2
p08 <- c(.2, .5, .3)
sum(p08)           # normalizzazione
sum(k08 * p08)     # E(K) = 1.1
set.seed(17)
x08 <- sample(k08, 1000,
  replace = TRUE, prob = p08)
mean(x08)          # media simulata
