# Risposta teorica a un impulso unitario.
k59 <- 0:12
effetto59 <- 0.65^k59
data.frame(ritardo = k59,
           effetto = round(effetto59, 4))
