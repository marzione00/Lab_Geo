r77 <- subset(fossili,
               morfotipo == "Rounded")
d77 <- with(r77,
  diametro_tot_um - diametro_int_um)
set.seed(17)
bd77 <- replicate(2000,
  mean(sample(d77, replace = TRUE)))
c(differenza = mean(d77),
  SE = sd(bd77))
