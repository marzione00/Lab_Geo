# Lo stesso campione, piu permutazioni
z79 <- lab_permutazione(B=200)
w79 <- lab_permutazione(B=1000)
rbind(B200=z79$metrics,
      B1000=w79$metrics)
# Nessun nuovo individuo aggiunto.
