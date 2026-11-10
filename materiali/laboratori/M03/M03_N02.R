# Frequenza assoluta, relativa e percentuale
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
ctx <- inizia_notebook("M03_N02")
set.seed(1005)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Il campione da descrivere
f <- leggi_dati("fossili_simulati.csv")
richiedi_colonne(f, c("id", "morfotipo", "diametro_tot_um", "spessore_um"))
stopifnot(nrow(f) == 160L, anyDuplicated(f$id) == 0L)
stopifnot(all(is.finite(f$diametro_tot_um)))
str(f)
table(f$morfotipo)


# Analisi principale: Frequenza assoluta, relativa e percentuale
conteggi <- table(f$morfotipo)
frequenze <- data.frame(
  morfotipo = names(conteggi),
  n = as.integer(conteggi),
  proporzione = as.numeric(prop.table(conteggi)),
  percentuale = 100 * as.numeric(prop.table(conteggi)))
frequenze
stopifnot(sum(frequenze$n) == nrow(f))
stopifnot(abs(sum(frequenze$proporzione) - 1) < 1e-12)
