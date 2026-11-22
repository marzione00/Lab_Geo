x43 <- c(1, 2, 3, 5, 4)
cor(head(x43, -1), tail(x43, -1))
as.numeric(acf(x43, lag.max = 1,
               plot = FALSE)$acf[2])
# cor() ricentra separatamente le due colonne.
# acf() usa la media dell'intera serie.
