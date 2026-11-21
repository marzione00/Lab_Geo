f37 <- read.csv(
  "Dati/fossili_simulati.csv")
p37 <- subset(f37,
              morfotipo == "Rounded")
x37 <- p37$diametro_tot_um
n37 <- length(x37)
s37 <- sd(x37)
c(SD = s37, SE = s37/sqrt(n37))
