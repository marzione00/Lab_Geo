# Diametri in micrometri, dati del corso
x106 <- fossili$diametro_tot_um
g106 <- split(x106,fossili$morfotipo)
set.seed(17)
b106 <- replicate(2000,
  mean(sample(x106,replace=TRUE)))
s106 <- replicate(2000,mean(vapply(
  g106,function(z)
    mean(sample(z,replace=TRUE)),0.0)))
c(pooled=sd(b106),strati=sd(s106))
