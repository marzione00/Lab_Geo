# Margine stabilito prima dei risultati
delta_min26 <- 0.5
ic26 <- c(0.10, 0.30)
# Tutto l'IC illustrativo e' nel margine?
all(ic26 > -delta_min26 &
    ic26 < delta_min26)
