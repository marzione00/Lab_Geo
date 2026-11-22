# Dati giornalieri completi, ordinati.
x <- demo$tmax
media31 <- as.numeric(
  stats::filter(x, rep(1/31, 31),
                sides = 2))
mediana31 <- runmed(x, k = 31,
                  endrule="constant")
mediana31[c(1:15,
  (length(x)-14):length(x))] <- NA
