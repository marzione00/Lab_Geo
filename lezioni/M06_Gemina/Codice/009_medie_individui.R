f09 <- read.csv(
  "Dati/fossili_simulati.csv")
g09 <- split(f09$diametro_tot_um,
             f09$morfotipo)
mean(g09$Spiky)-mean(g09$Rounded)
# Tutti i confronti fra individui
mean(outer(g09$Spiky,
           g09$Rounded, ">"))
