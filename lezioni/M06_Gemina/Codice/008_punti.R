f08 <- read.csv(
  "Dati/fossili_simulati.csv")
stripchart(diametro_tot_um ~ morfotipo,
 data=f08, method="stack", pch=16,
 col=c("#1D7890","#C57E42"),
 xlab="Diametro totale (um)")
tapply(f08$diametro_tot_um,
       f08$morfotipo, mean)
