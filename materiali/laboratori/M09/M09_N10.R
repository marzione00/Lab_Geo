# Tre processi, tre domande
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
ctx <- inizia_notebook("M09_N10")
set.seed(1018)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Tre processi, tre domande
p <- leggi_dati("processi_simulati.csv")
richiedi_colonne(p,c("passo","rumore_bianco","ar1","random_walk"))
stopifnot(nrow(p)==300,!anyNA(p))
stile_grafico()
matplot(p$passo,p[c("rumore_bianco","ar1","random_walk")],type="l",lty=1,
        col=palette_geo[1:3],xlab="Passo",ylab="Unità simulate",main="Realizzazioni simulate")
legend("topleft",c("Rumore bianco","AR(1)","Random walk"),col=palette_geo[1:3],lty=1,bty="n")
