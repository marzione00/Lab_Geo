# Percorso obbligatorio e approfondimento
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
ctx <- inizia_notebook("M10_N10")
set.seed(1020)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Percorso obbligatorio e approfondimento
f <- leggi_dati("fossili_simulati.csv")
richiedi_colonne(f,c("id","morfotipo","diametro_tot_um","diametro_int_um"))
audit <- data.frame(
  controllo=c("ID unici","Diametri completi","Totale positivo","Interno entro totale"),
  esito=c(!anyDuplicated(f$id),!anyNA(f[c("diametro_tot_um","diametro_int_um")]),
          all(f$diametro_tot_um>0),all(f$diametro_int_um>0 & f$diametro_int_um<=f$diametro_tot_um)))
audit
stopifnot(all(audit$esito))
