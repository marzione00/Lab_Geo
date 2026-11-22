# Effetto di +1 um sul rapporto degli odds.
b75 <- coef(m_log)["diametro_tot_um"]
c(per_1_um = exp(b75),
  per_0_5_um = exp(0.5*b75))
# Cambiare l'unita' cambia l'incremento.
