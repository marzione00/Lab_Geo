# Densita' dei 24 provini [g/cm^3]
c06 <- campioni
c06$rho <- c06$massa_g /
            c06$volume_cm3
# Una media per stazione: sei valori
st06 <- aggregate(rho ~ stazione,
  data = c06, FUN = mean)
nrow(c06)
nrow(st06)
