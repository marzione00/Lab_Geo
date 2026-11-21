f92 <- read.csv(
 "Dati/fossili_simulati.csv")
g92 <- split(f92$diametro_tot_um,
             f92$morfotipo)
t92 <- t.test(g92$Spiky,g92$Rounded)
c(SE=t92$stderr,p=t92$p.value)
t92$conf.int
