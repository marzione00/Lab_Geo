# Giorni consecutivi, dati simulati.
demo$giorno <- seq_len(nrow(demo))
locale <- loess(tmax ~ giorno,
                data = demo,
                span=0.2, degree=1)
curva <- predict(locale)
plot(demo$data, curva, type = "l",
     xlab = "Data", ylab = "Tmax [C]")
