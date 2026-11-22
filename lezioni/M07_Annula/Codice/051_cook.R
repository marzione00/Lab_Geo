# Una misura del cambiamento globale.
D51 <- cooks.distance(m0)
plot(D51, type = "h",
     xlab = "Indice del fossile",
     ylab = "Distanza di Cook")
j51 <- which.max(D51)
f[j51, c("id", "morfotipo")]
