f57 <- read.csv(
  "Dati/fossili_simulati.csv")
p57 <- subset(f57,
              morfotipo == "Rounded")
d57 <- p57$diametro_tot_um -
       p57$diametro_int_um
c(media = mean(d57), n = length(d57))
t.test(d57)$conf.int
