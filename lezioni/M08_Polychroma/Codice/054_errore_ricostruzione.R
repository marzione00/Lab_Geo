errore <- sum((Z - Z2)^2)
teoria <- (nrow(Z)-1) * sum(lam[3:8])
c(calcolato = errore, teoria = teoria)
errore / sum(Z^2)
