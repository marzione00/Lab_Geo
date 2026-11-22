# Generatore del laboratorio, tau=3
set.seed(17); n51 <- 30
u51 <- rnorm(n51,0,3)
a51 <- 10+u51+rnorm(n51)
b51 <- 10+u51+.6+rnorm(n51)
c(appaiato=sd(b51-a51)/sqrt(n51),
  indipendente=sqrt(var(a51)/n51+
                    var(b51)/n51))
