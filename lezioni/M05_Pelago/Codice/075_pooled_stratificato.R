z75 <- fossili$diametro_tot_um
set.seed(17)
bp75 <- replicate(2000,
  mean(sample(z75, replace = TRUE)))
# b74 usa quote fissate a 80 e 80
c(pooled = sd(bp75),
  stratificato = sd(b74))
mean(z75)  # Media osservata comune
