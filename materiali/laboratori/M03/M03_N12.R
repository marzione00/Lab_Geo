# Istogramma: il ruolo delle classi
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
ctx <- inizia_notebook("M03_N12")
set.seed(1006)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Dati e domanda prima del tipo di grafico
f <- leggi_dati("fossili_simulati.csv")
r <- leggi_dati("rocce_simulate.csv")
f$morfotipo <- factor(f$morfotipo, levels = c("Rounded", "Spiky"))
stopifnot(all(is.finite(f$diametro_tot_um)), all(r$grana_mm > 0))
x <- f$diametro_tot_um
table(f$morfotipo)


# Analisi principale: Istogramma: il ruolo delle classi
stile_grafico()
hist(x, breaks = 8, col = palette_geo[1], border = "white",
     xlab = "Diametro totale (micrometri)", ylab = "Numero di individui",
     main = "Istogramma: richiesta di circa 8 classi")
stile_grafico()
hist(x, breaks = 25, col = palette_geo[2], border = "white",
     xlab = "Diametro totale (micrometri)", ylab = "Numero di individui",
     main = "Stessi 160 individui: più classi")
