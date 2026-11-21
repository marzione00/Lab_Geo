# * include effetti principali e prodotto.
m_int <- lm(diametro_int_um ~
  diametro_tot_um * morfotipo,
  data = f)
coef(m_int)
# Le colonne rendono visibile il prodotto.
colnames(model.matrix(m_int))
