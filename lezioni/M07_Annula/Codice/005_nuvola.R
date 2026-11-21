# Colore secondo il morfotipo.
col <- c("#1D7890", "#C57E42")
plot(diametro_int_um ~ diametro_tot_um,
  data = f, col = col[f$morfotipo],
  pch = 16, xlab = "Totale (um)",
  ylab = "Interno (um)")
