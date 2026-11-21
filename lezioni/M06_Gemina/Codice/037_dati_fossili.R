f37 <- read.csv("Dati/fossili_simulati.csv")
a37 <- f37$diametro_tot_um[
  f37$morfotipo == "Rounded"]
b37 <- f37$diametro_tot_um[
  f37$morfotipo == "Spiky"]
c(A = length(a37), B = length(b37))
