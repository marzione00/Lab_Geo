massa_g <- c(20, 90)
volume_cm3 <- c(10, 30)
rho <- massa_g / volume_cm3
c(media_provini=mean(rho),
  densita_complessiva=sum(massa_g)/sum(volume_cm3))
stopifnot(weighted.mean(rho,volume_cm3)==2.75)
