# Preparare le distanze senza usare l’etichetta
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
ctx <- inizia_notebook("M08_N10")
set.seed(1016)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Preparare le distanze senza usare l’etichetta
r <- leggi_dati("rocce_simulate.csv")
v <- c("SiO2","CaO","MgO","FeO","densita","grana_mm","colore","fossili")
X <- as.matrix(r[v])
stopifnot(all(is.finite(X)),all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z,method="euclidean")
range(D)
stopifnot(nrow(Z)==90L)
