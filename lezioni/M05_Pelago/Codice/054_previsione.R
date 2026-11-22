# x51: diametri Rounded
n54 <- length(x51)
q54 <- qt(.975, n54-1)
mean(x51) + c(-1,1)*q54 *
  sd(x51)*sqrt(1+1/n54)
# Include la variabilita' futura.
