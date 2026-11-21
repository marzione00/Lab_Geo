x <- f$diametro_tot_um
y <- f$diametro_int_um
cor(x, y, method = "pearson")
# Cambio di unita positivo: stesso r.
cor(x / 1000, y / 1000)
# L'inversione del segno cambia r.
cor(x, -y)
