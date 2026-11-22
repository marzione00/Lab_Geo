# Stessi nomi e livelli del modello.
nuovi65 <- data.frame(
  diametro_tot_um = c(6.5, 7.5),
  morfotipo = c("Rounded", "Spiky"))
predict(m_int, newdata = nuovi65,
        interval = "confidence")
# Nuovi individui: intervallo piu' ampio.
predict(m_int, newdata = nuovi65,
        interval = "prediction")
