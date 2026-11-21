# Ordine dichiarato: Spiky-Rounded.
f05 <- read.csv(
  "Dati/fossili_simulati.csv")
g05 <- split(f05$diametro_tot_um,
             f05$morfotipo)
d05 <- mean(g05$Spiky) -
       mean(g05$Rounded)
d05  # micrometri
