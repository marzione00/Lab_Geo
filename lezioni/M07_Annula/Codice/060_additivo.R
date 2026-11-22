# Contrasto a diametro totale fissato.
nuovi60 <- data.frame(
  diametro_tot_um = c(7, 7),
  morfotipo = c("Rounded", "Spiky"))
mu60 <- predict(m_add, nuovi60)
diff(mu60)
# Coincide con il coefficiente di gruppo.
coef(m_add)["morfotipoSpiky"]
