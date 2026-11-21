# Tre scale per la stessa probabilita'.
p72 <- c(0.2, 0.5, 0.8)
data.frame(
  probabilita = p72,
  odds = p72 / (1 - p72),
  logit = qlogis(p72))
# La funzione inversa recupera p.
plogis(qlogis(p72))
