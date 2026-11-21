a49 <- as.numeric(acf(proc$rumore_bianco,
  lag.max = 24, plot = FALSE)$acf)[-1]
banda49 <- 1.96 / sqrt(nrow(proc))
which(abs(a49) > banda49)
# Confronti puntuali, fra loro dipendenti.
