# Riferimento didattico: 2022-2023.
mese <- format(demo$data, "%m")
inizio <- as.Date("2024-01-01")
base <- demo$data < inizio
rif <- tapply(demo$tmax[base],
              mese[base], mean)
scarti <- demo$tmax - rif[mese]
# Ciascun giorno usa il proprio mese.
head(scarti)
