f51 <- read.csv(
  "Dati/fossili_simulati.csv")
p51 <- subset(f51,
              morfotipo == "Rounded")
x51 <- p51$diametro_tot_um
n51 <- length(x51)
q51 <- qt(.975, n51-1)
se51 <- sd(x51)/sqrt(n51)
mean(x51) + c(-1,1)*q51*se51
t.test(x51)$conf.int
