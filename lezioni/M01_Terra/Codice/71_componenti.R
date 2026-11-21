# Medie mensili dei dati simulati.
mese <- format(demo$data, "%Y-%m")
mensile <- tapply(demo$tmax,
                  mese, mean)
serie <- ts(mensile,
            start = c(2022, 1),
            frequency = 12)
scomp <- stl(serie,
             s.window = "periodic")
plot(scomp)
