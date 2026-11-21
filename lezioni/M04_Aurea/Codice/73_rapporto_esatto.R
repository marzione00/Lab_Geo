s73 <- .1; c73 <- .7
t273 <- 2*s73^2*(1-c73)
c(mediana = 2,
  media = 2*exp(t273/2),
  SD = 2*sqrt(expm1(t273) *
                 exp(t273)))
