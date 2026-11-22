f10 <- read.csv(
  "Dati/fossili_simulati.csv")
g10 <- split(f10$diametro_tot_um,
             f10$morfotipo)
tt10 <- t.test(g10$Spiky,
 g10$Rounded, var.equal=FALSE)
tt10$conf.int  # IC bilaterale 95%
tt10$stderr    # errore standard
