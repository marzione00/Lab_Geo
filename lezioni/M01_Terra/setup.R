# Preparazione dei dati per gli esempi della presentazione.
# Aprire R nella cartella principale del materiale e lanciare:
# source("setup.R", encoding = "UTF-8")
# Si usano soltanto funzioni comprese nell'installazione di R.

file_terra <- file.path("Dati", "terra01_anteprima.csv")
file_demo <- file.path("Dati", "meteo_simulati.csv")
if (!all(file.exists(c(file_terra, file_demo)))) {
  stop("Aprire R nella cartella che contiene setup.R e la cartella Dati.")
}

# Terra 01: 40 dati simulati archiviati nel sito del laboratorio.
# Il CSV permette di ripetere l'analisi senza dipendere dal generatore casuale.
terra <- read.csv(file_terra, stringsAsFactors = FALSE)
terra$stazione <- factor(terra$stazione, levels = c("A", "B", "C"))

# Esempio meteorologico DIDATTICO: tutti i valori sono simulati.
# Non sono le osservazioni Meteostat delle figure originali.
demo <- read.csv(file_demo, stringsAsFactors = FALSE)
demo$data <- as.Date(demo$data, format = "%Y-%m-%d")
demo <- demo[order(demo$data), ]
row.names(demo) <- NULL

# Unita': tmin/tmax in gradi Celsius; pioggia in mm al giorno;
# sole in minuti al giorno; nubi come percentuale tra 0 e 100.
# La sequenza giornaliera completa consente finestre espresse in giorni.
stopifnot(
  nrow(terra) == 40L,
  identical(as.integer(table(terra$stazione)), c(20L, 10L, 10L)),
  nrow(demo) == 1096L,
  !anyNA(demo),
  all(diff(demo$data) == 1),
  all(demo$tmax >= demo$tmin),
  all(demo$pioggia >= 0),
  all(demo$nubi >= 0 & demo$nubi <= 100)
)

cat("Dati pronti: terra (40 righe), demo (1096 giorni simulati).\n")
