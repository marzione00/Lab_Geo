# Scegliamo il gruppo di riferimento.
f$morfotipo <- relevel(
  factor(f$morfotipo), ref = "Rounded")
levels(f$morfotipo)
contrasts(f$morfotipo)
# La scelta entra nella parametrizzazione.
m_add <- lm(diametro_int_um ~
  diametro_tot_um + morfotipo, data = f)
