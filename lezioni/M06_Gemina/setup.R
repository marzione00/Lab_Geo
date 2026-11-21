# Eseguire dalla cartella che contiene Gemina_M06.Rproj.
# Non servono pacchetti aggiuntivi o connessione Internet.
if (!file.exists("R/laboratori_gemina.R")) {
  stop("Aprire Gemina_M06.Rproj e rieseguire dalla cartella del progetto.")
}
options(stringsAsFactors = FALSE)
source("R/laboratori_gemina.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
