# Standardizzare non significa rendere indipendenti
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
ctx <- inizia_notebook("M08_N02")
set.seed(1015)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: La matrice delle misure e le colonne da escludere
r <- leggi_dati("rocce_simulate.csv")
variabili <- c("SiO2","CaO","MgO","FeO","densita","grana_mm","colore","fossili")
richiedi_colonne(r,c("id","litologia_generatrice",variabili))
X <- as.matrix(r[variabili])
stopifnot(nrow(X)==90L,all(is.finite(X)),all(apply(X,2,sd)>0))
dim(X)
apply(X,2,sd)


# Analisi principale: Standardizzare non significa rendere indipendenti
Z <- scale(X,center=TRUE,scale=TRUE)
controllo <- data.frame(variabile=colnames(X),
                        media_originale=colMeans(X),SD_originale=apply(X,2,sd),
                        media_z=colMeans(Z),SD_z=apply(Z,2,sd))
controllo
stopifnot(max(abs(colMeans(Z)))<1e-10,
          max(abs(apply(Z,2,sd)-1))<1e-10)
round(cor(Z),2)
