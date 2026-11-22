f55 <- read.csv(
  "Dati/fossili_simulati.csv")
g55 <- split(f55$diametro_tot_um,
             f55$morfotipo)
S55 <- g55$Spiky; R55 <- g55$Rounded
mean(S55) - mean(R55)
t.test(S55, R55,
       var.equal = FALSE)$conf.int
