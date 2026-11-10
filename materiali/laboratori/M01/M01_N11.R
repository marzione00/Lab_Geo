# Simulare una popolazione finita: un’aggiunta esplicita
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
ctx <- inizia_notebook("M01_N11")
set.seed(1002)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Rileggere il disegno prima dei numeri
d <- leggi_dati("campioni_modulo1.csv")
d$densita <- d$massa_g / d$volume_cm3
conteggi <- as.data.frame(table(affioramento = d$affioramento,
                              stazione = d$stazione))
conteggi[conteggi$Freq > 0, ]
stopifnot(nrow(d) == 24L, length(unique(d$stazione)) == 6L)


# Analisi principale: Simulare una popolazione finita: un’aggiunta esplicita
set.seed(102)
siti <- data.frame(id_sito = sprintf("S%03d", 1:120),
                   distanza_m = seq(0, 1190, by = 10))
siti$valore <- 2.4 + 0.00035 * siti$distanza_m + rnorm(120, 0, 0.04)
media_popolazione <- mean(siti$valore)
media_popolazione
stile_grafico()
plot(siti$distanza_m, siti$valore, pch = 19, col = palette_geo[1],
     xlab = "Distanza convenzionale (m)", ylab = "Proprietà simulata (u.c.)",
     main = "Popolazione finita costruita per l'esercizio")
