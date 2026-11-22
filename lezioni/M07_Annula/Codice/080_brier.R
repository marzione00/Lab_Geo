# Valutazione descrittiva sul campione.
brier80 <- mean((p_log - f$spiky)^2)
# Riferimento costante: frequenza osservata.
pbase80 <- mean(f$spiky)
base80 <- mean((pbase80 - f$spiky)^2)
c(modello = brier80, riferimento = base80)
