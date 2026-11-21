# Una riga = un fossile sintetico.
f04 <- read.csv(
  "Dati/fossili_simulati.csv")
stopifnot(!anyDuplicated(f04$id))
table(f04$morfotipo)
summary(f04$diametro_tot_um)
# um nel nome indica micrometri.
