# Ripetere una misura non equivale a cambiare provino
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
ctx <- inizia_notebook("M01_N14")
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


# Preparazione: Simulare una popolazione finita: un’aggiunta esplicita
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


# Preparazione: Casuale, sistematico e di convenienza
set.seed(103)
n <- 12L
id_casuale <- sample(seq_len(nrow(siti)), size = n, replace = FALSE)
id_comodo <- seq_len(n)
partenza <- sample(1:10, 1)
id_sistematico <- seq(partenza, nrow(siti), by = 10)
stime <- data.frame(
  piano = c("Casuale", "Convenienza", "Sistematico"),
  media = c(mean(siti$valore[id_casuale]), mean(siti$valore[id_comodo]),
            mean(siti$valore[id_sistematico])))
stime$errore_rispetto_popolazione <- stime$media - media_popolazione
stime


# Preparazione: Ripetere l’esperimento di campionamento
set.seed(104)
B <- 1000L
medie_casuali <- replicate(B, mean(siti$valore[sample(120, 12)]))
medie_accessibili <- replicate(B, mean(siti$valore[sample(30, 12)]))
confronto <- data.frame(
  piano = c("Intera popolazione", "Solo primi 30 siti"),
  media_delle_stime = c(mean(medie_casuali), mean(medie_accessibili)),
  dispersione_delle_stime = c(sd(medie_casuali), sd(medie_accessibili)))
confronto$bias_simulato <- confronto$media_delle_stime - media_popolazione
confronto
stile_grafico()
boxplot(list(Casuale = medie_casuali, Accessibile = medie_accessibili),
        ylab = "Media di 12 siti (u.c.)", col = palette_geo[1:2])
abline(h = media_popolazione, lty = 2)


# Analisi principale: Ripetere una misura non equivale a cambiare provino
set.seed(105)
repliche <- data.frame(
  id_provino = rep("C01", 5),
  lettura = 1:5,
  densita = d$densita[1] + rnorm(5, 0, 0.005))
repliche
c(righe = nrow(repliche), provini = length(unique(repliche$id_provino)))
sd(repliche$densita)
