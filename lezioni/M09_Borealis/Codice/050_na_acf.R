# Controllo prima di calcolare l'ACF.
stopifnot(!anyNA(y))
# Esempio: un mese rimane NA.
y50 <- y
y50[30] <- NA
sum(complete.cases(head(y50, -1),
                   tail(y50, -1)))
