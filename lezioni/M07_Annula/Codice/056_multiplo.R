# Un predittore quantitativo e un gruppo.
m_add <- lm(diametro_int_um ~
  diametro_tot_um + morfotipo,
  data = f)
coef(m_add)
summary(m_add)$sigma
