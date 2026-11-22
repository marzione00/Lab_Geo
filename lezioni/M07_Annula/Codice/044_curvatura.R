# Aggiungiamo un termine quadratico.
m_quad <- lm(diametro_int_um ~
  diametro_tot_um +
  I(diametro_tot_um^2), data = f)
plot(fitted(m_quad), resid(m_quad),
     pch = 19, xlab = "Stima (um)",
     ylab = "Residuo (um)")
abline(h = 0, lty = 2)
