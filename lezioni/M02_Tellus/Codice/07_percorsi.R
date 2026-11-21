# Percorso relativo alla radice
f <- file.path("Dati",
               "campioni_modulo1.csv")
stopifnot(file.exists(f))

# Controlli dopo la lettura
campioni <- read.csv(f)
stopifnot(nrow(campioni) == 24L)
str(campioni)
