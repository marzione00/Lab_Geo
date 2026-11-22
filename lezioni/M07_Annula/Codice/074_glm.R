# Stima descrittiva sul campione.
m_log <- glm(spiky ~ diametro_tot_um,
  data = f, family = binomial())
summary(m_log)$coefficients
m_log$converged
# Probabilita' nella scala 0--1.
p_log <- predict(m_log,
                 type = "response")
range(p_log)
