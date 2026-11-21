phi60 <- c(0, 0.3, 0.65, 0.9)
# Innovazioni con varianza unitaria.
data.frame(phi = phi60,
  varianza = 1 / (1 - phi60^2))
