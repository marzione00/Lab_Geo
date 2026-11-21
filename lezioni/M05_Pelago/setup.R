# Aprire Pelago_M05.Rproj e lavorare dalla cartella del progetto.
# R base: nessun pacchetto esterno richiesto.
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
source("Pelago_laboratori.R", encoding = "UTF-8")
fossili <- read.csv("Dati/fossili_simulati.csv",
                    stringsAsFactors = FALSE)
provini <- read.csv("Dati/campioni_modulo1.csv",
                   stringsAsFactors = FALSE)
provini$densita <- provini$massa_g/provini$volume_cm3
stazioni <- aggregate(densita ~ affioramento + stazione, provini, mean)

