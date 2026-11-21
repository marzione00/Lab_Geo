# Aurea M04 - eseguire dalla cartella di Aurea_M04.Rproj.
source("Aurea_laboratori.R", encoding = "UTF-8")
# Specifiche didattiche del provino, non stime ottenute dai nove laboratori.
parametri_densita <- read.csv("Dati/parametri_densita.csv",
                              stringsAsFactors = FALSE, check.names = FALSE)
