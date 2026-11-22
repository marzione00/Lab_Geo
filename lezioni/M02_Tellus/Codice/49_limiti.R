# Sottocaso: tre valori non negativi
osservati_c <- c(0.12, 0.08)
limite_c <- 0.05
c(inferiore = sum(osservati_c) / 3,
  superiore = (sum(osservati_c) +
               limite_c) / 3)
