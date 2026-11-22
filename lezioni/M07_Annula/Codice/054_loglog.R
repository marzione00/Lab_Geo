# I logaritmi richiedono valori > 0.
stopifnot(all(f$diametro_int_um > 0),
          all(f$diametro_tot_um > 0))
m_loglog <- lm(log(diametro_int_um) ~
  log(diametro_tot_um), data = f)
coef(m_loglog)
plot(m_loglog, which = 1)
