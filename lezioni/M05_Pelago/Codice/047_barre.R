f47 <- read.csv(
  "Dati/fossili_simulati.csv")
p47 <- subset(f47,
              morfotipo == "Rounded")
x47 <- p47$diametro_tot_um
s47 <- sd(x47); n47 <- length(x47)
c(SD = s47, SE = s47/sqrt(n47),
  IC95 = qt(.975,n47-1)*s47/sqrt(n47))
