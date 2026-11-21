x_g <- fossili$diametro_tot_um
y_g <- fossili$diametro_int_um
ok_g <- is.finite(x_g) &
        is.finite(y_g)
col_g <- ifelse(viol,
  "firebrick", "steelblue")
plot(x_g[ok_g], y_g[ok_g], asp = 1,
  pch = 19, col = col_g[ok_g],
  xlab = "D esterno [um]",
  ylab = "D interno [um]")
abline(0, 1, lty = 2)
