pioggia_es <- c(0, 5, 12, NA, 3)
c(totale_osservato = sum(pioggia_es, na.rm = TRUE),
  media_osservata = mean(pioggia_es, na.rm = TRUE),
  massimo_osservato = max(pioggia_es, na.rm = TRUE),
  giorni_osservati = sum(!is.na(pioggia_es)))
