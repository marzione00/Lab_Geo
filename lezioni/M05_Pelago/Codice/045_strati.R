f45 <- read.csv(
  "Dati/fossili_simulati.csv")
g45 <- split(f45$diametro_tot_um,
             f45$morfotipo)
w45 <- c(Rounded = .5, Spiky = .5)
se45 <- sqrt(sum(w45^2 *
  sapply(g45, var)/lengths(g45)))
se45
