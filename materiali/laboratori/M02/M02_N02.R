# Vettori: tipi e operazioni
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M02_N02")
set.seed(1003)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Una tabella ben importata non è scontata
percorso <- file.path(ctx$root, "dati", "fossili_da_controllare.csv")
readLines(percorso, n = 4, encoding = "UTF-8")
# Forziamo testo per non perdere ND, spazi e virgole decimali.
grezzi <- read.csv(percorso, sep = ";", colClasses = "character",
                   na.strings = character(), stringsAsFactors = FALSE,
                   fileEncoding = "UTF-8")
str(grezzi)
head(grezzi, 4)


# Analisi principale: Vettori: tipi e operazioni
numeri <- c(4, 5, 6)
misto <- c(4, "5", "ND")
class(numeri)
class(misto)
valori <- c(4, NA, 6)
is.na(valori)
mean(valori)                # NA: il mancante non viene ignorato per default.
mean(valori, na.rm = TRUE)  # Cambia il denominatore: ora usa due valori.
sum(!is.na(valori))
