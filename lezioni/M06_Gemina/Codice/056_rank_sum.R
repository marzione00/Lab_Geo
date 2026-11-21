f56 <- read.csv(
  "Dati/fossili_simulati.csv")
g56 <- split(f56$diametro_tot_um,
             f56$morfotipo)
x56 <- g56$Spiky; y56 <- g56$Rounded
wilcox.test(x56,y56,exact=FALSE,
            correct=TRUE)
mean(outer(x56,y56,">")+
     .5*outer(x56,y56,"=="))
