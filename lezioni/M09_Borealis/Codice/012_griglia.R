griglia_es <- data.frame(
  data = seq(min(cal_es$data), max(cal_es$data),
             by = "month"))
osservati_es <- cal_es[-4, ]
completo_es <- merge(griglia_es, osservati_es,
                    by = "data", all.x = TRUE)
completo_es
