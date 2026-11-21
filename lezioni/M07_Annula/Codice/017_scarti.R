# Retta proposta, prima dell'ottimizzazione.
a <- -0.5
b <- 0.9
e_proposti <- y - (a + b * x)
sum(e_proposti^2)
# Confronto con il minimo trovato da lm.
sum(residuals(m0)^2)
