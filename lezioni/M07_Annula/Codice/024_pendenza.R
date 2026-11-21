# Incremento medio per +0.5 um in X.
delta_x <- 0.5
coef(m0)[2] * delta_x
# Previsione media a diametro totale 7.
predict(m0, newdata = data.frame(
  diametro_tot_um = 7))
