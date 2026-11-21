# Analisi di sensibilita', non ricerca del p minimo.
ks87 <- c(1, 4, 8)
stat87 <- sapply(ks87, function(k) {
  tseries::adf.test(as.numeric(y),
                    k = k)$statistic
})
data.frame(k = ks87, statistica = stat87)
