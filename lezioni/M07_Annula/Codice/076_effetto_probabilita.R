# Probabilita' per profili espliciti.
nuovi76 <- data.frame(
  diametro_tot_um = c(6, 7, 8))
p76 <- predict(m_log, nuovi76,
               type = "response")
data.frame(nuovi76, probabilita = p76)
# Differenze per incrementi di 1 um.
diff(p76)
