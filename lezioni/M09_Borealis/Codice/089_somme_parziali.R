# Versione Level: si sottrae la media.
e89 <- as.numeric(y) - mean(y)
S89 <- cumsum(e89)
plot(S89, type = "l", ylab = "Somma residui",
     xlab = "Mese")
abline(h = 0, col = "grey70")
