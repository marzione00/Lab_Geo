m0 <- 106; V0 <- 40
cm69 <- 1/V0
cV69 <- -m0/V0^2
c(sensibilita_massa = cm69,
  sensibilita_volume = cV69)
# Effetto di +1 g e di +0.6 cm^3
c(cm69*1, cV69*.6)
