# Contrasto Spiky meno Rounded
set.seed(17)
delta76 <- replicate(2000,
  rb74(g74$Spiky) - rb74(g74$Rounded))
mean(g74$Spiky) - mean(g74$Rounded)
quantile(delta76, c(.025, .975),
         type = 7)
