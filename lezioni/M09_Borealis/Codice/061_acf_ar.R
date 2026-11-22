k61 <- 0:12
# Curve teoriche, senza errore campionario.
rho61 <- sapply(c(0.65, -0.65, 0.9),
               function(p) p^k61)
matplot(k61, rho61, type = "b",
        xlab = "Ritardo", ylab = "ACF")
abline(h = 0, col = "grey70")
