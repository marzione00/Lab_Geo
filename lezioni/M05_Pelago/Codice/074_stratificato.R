g74 <- split(fossili$diametro_tot_um,
             fossili$morfotipo)
rb74 <- function(v)
  mean(sample(v, replace = TRUE))
set.seed(17)
b74 <- replicate(2000,
  .5*rb74(g74$Rounded) +
  .5*rb74(g74$Spiky))
sd(b74)
