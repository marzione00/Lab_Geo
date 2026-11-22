ricostruita_T <- with(temp,
  trend_simulato + stagione_simulata +
    residuo_simulato)
err_T <- max(abs(temp$temperatura_C -
                 ricostruita_T))
stopifnot(err_T < 2e-8)
