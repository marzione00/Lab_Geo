# F001: due diametri in micrometri
f1 <- fossili[fossili$id == "F001", ]
d_est <- f1$diametro_tot_um
d_int <- f1$diametro_int_um
spessore <- (d_est - d_int) / 2
spessore                   # 0.5
# Residuo dell'identita geometrica
d_est - d_int - 2 * spessore
