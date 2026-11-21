# Pacchetto richiesto dal progetto.
stopifnot(requireNamespace("tseries",
                          quietly = TRUE))
adf88 <- tseries::adf.test(
  as.numeric(y), k = 4)
adf88
# Campi da riportare nel resoconto.
adf88[c("statistic", "parameter",
        "p.value", "alternative")]
