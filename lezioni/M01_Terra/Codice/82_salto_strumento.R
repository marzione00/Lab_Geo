# Aggiunge un salto fittizio di 2 C.
cambio <- as.Date("2023-07-01")
con_salto <- demo$tmax +
  2 * (demo$data >= cambio)
plot(demo$data, con_salto, type = "l",
     xlab = "Data", ylab = "Tmax [C]")
abline(v = as.numeric(cambio),
       col = "firebrick", lty = 2)
