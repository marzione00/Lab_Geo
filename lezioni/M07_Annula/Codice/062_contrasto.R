# Confrontiamo tre diametri scelti.
x62 <- c(6, 7, 8)
a62 <- data.frame(diametro_tot_um = x62,
                   morfotipo = "Rounded")
b62 <- a62; b62$morfotipo <- "Spiky"
delta62 <- predict(m_int, b62) -
           predict(m_int, a62)
data.frame(diametro = x62, delta = delta62)
