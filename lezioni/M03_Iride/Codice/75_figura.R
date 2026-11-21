# Coppie riferite allo stesso fossile
col75 <- c("#1D7890", "#C57E42")
i75 <- as.integer(fossili$morfotipo)
plot(fossili$diametro_tot_um,
     fossili$diametro_int_um,
     col = col75[i75], pch = 16,
     xlab = "D totale [micrometri]",
     ylab = "D interno [micrometri]")
legend("topleft",
  legend = levels(fossili$morfotipo),
  col = col75, pch = 16, bty = "n")
