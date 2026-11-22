# Media di n osservazioni N(1,1)
n29 <- 60
se29 <- 1 / sqrt(n29)
# Probabilita' di media fra .8 e 1.2
pnorm(1.2, 1, se29) -
  pnorm(.8, 1, se29)
