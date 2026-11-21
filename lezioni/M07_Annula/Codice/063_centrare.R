# Il valore 7 um ha significato nel dominio.
f$x_c <- f$diametro_tot_um - 7
m_c <- lm(diametro_int_um ~
  x_c * morfotipo, data = f)
coef(m_c)
# Le previsioni restano uguali.
max(abs(fitted(m_c) - fitted(m_int)))
