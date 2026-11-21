# Esempio di 20 statistiche ordinate
v69 <- seq(1, 2.9, by = .1)
p69 <- .975
h69 <- 1 + (length(v69)-1)*p69
j69 <- floor(h69)
g69 <- h69-j69
(1-g69)*v69[j69] + g69*v69[j69+1]
quantile(v69, p69, type = 7)
