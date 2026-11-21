# Profilo dentro il dominio osservato.
nuovo55 <- data.frame(
  diametro_tot_um = 7)
eta55 <- predict(m_loglog, nuovo55)
mediana55 <- exp(eta55)
# Media con errori log-normali omogenei.
media55 <- exp(eta55 +
  sigma(m_loglog)^2 / 2)
c(mediana = mediana55, media = media55)
