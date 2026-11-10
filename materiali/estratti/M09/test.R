p <- read.csv('dati/processi_simulati.csv')
stopifnot(requireNamespace('tseries',quietly=TRUE))
x <- p$ar1
tseries::adf.test(x,k=4)
tseries::kpss.test(x,null='Level')
tseries::kpss.test(x,null='Trend')
# Conservare anche gli avvisi sui limiti
# delle probabilità tabulate.
