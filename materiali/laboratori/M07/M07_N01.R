# Definire risposta e predittore
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
ctx <- inizia_notebook("M07_N01")
set.seed(1013)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Definire risposta e predittore
f <- leggi_dati("fossili_simulati.csv")
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(all(is.finite(x)),all(is.finite(y)),all(y<=x))
stile_grafico()
plot(x,y,pch=19,col=adjustcolor(palette_geo[1],alpha.f=.6),
     xlab="Diametro totale (micrometri)",ylab="Diametro interno (micrometri)",
     main="Due misure dello stesso individuo")
abline(0,1,lty=2)
