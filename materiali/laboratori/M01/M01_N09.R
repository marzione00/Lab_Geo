# Salvare un risultato che un altro studente possa leggere
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
ctx <- inizia_notebook("M01_N09")
set.seed(1001)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Prima di digitare: definire la domanda
# Un oggetto di testo può registrare la domanda, non soltanto i numeri.
domanda <- "Confrontare la densità dei 24 provini simulati di A e B"
popolazione_accessibile <- "Provini delle sei stazioni del caso didattico"
domanda
popolazione_accessibile


# Preparazione: Una funzione, un argomento, un risultato
# Massa in grammi e volume in centimetri cubi di un singolo provino.
massa_g <- 107.2
volume_cm3 <- 40
rho <- massa_g / volume_cm3
rho
round(rho, digits = 2)
# 1 g/cm^3 equivale a 1000 kg/m^3.
rho_kg_m3 <- rho * 1000
rho_kg_m3


# Preparazione: Aprire il dataset senza modificarlo
d <- leggi_dati("campioni_modulo1.csv")
dim(d)             # Prima dimensione: righe; seconda: colonne.
names(d)           # Nomi esatti da utilizzare nel codice.
head(d, 6)         # Solo sei righe, per non affollare l'output.
str(d)             # Tipo di ciascuna colonna.
stopifnot(nrow(d) == 24L, ncol(d) == 6L)


# Preparazione: Leggere una colonna e selezionare una riga
d$massa_g
# Il terzo elemento della colonna massa.
d$massa_g[3]
# La terza riga, con tutte le sue informazioni.
d[3, ]
# Tre colonne per tutti i provini dell'affioramento A.
in_A <- d$affioramento == "A"
d[in_A, c("id", "massa_g", "volume_cm3")]
sum(in_A)          # TRUE conta come 1 nella somma.


# Preparazione: Quanti campioni abbiamo davvero?
unita <- data.frame(
  livello = c("Provini", "Stazioni", "Affioramenti"),
  numero = c(nrow(d), length(unique(d$stazione)),
             length(unique(d$affioramento)))
)
unita
table(d$affioramento)
table(d$stazione)
# La tabella incrociata verifica a quale affioramento appartiene ogni stazione.
table(d$affioramento, d$stazione)


# Preparazione: Dai tipi informatici al significato
d$affioramento <- factor(d$affioramento, levels = c("A", "B"))
d$alterazione <- factor(d$alterazione,
                        levels = c("bassa", "media", "alta"),
                        ordered = TRUE)
levels(d$alterazione)
table(d$alterazione)
# Gli ID devono essere presenti e univoci.
stopifnot(!anyNA(d$id), anyDuplicated(d$id) == 0L)


# Preparazione: Calcolare e verificare la densità di tutti i provini
stopifnot(is.numeric(d$massa_g), is.numeric(d$volume_cm3))
stopifnot(all(is.finite(d$massa_g)), all(is.finite(d$volume_cm3)))
stopifnot(all(d$massa_g > 0), all(d$volume_cm3 > 0))
d$densita_g_cm3 <- d$massa_g / d$volume_cm3
head(d[c("id", "massa_g", "volume_cm3", "densita_g_cm3")])
range(d$densita_g_cm3)
# Verifica di un calcolo già controllato a mano.
stopifnot(abs(d$densita_g_cm3[1] - 2.68) < 1e-10)


# Preparazione: Confrontare senza anticipare un test
medie <- aggregate(densita_g_cm3 ~ affioramento, data = d, FUN = mean)
medie
delta_AB <- with(medie, densita_g_cm3[affioramento == "A"] -
                         densita_g_cm3[affioramento == "B"])
delta_AB
stile_grafico()
stripchart(densita_g_cm3 ~ affioramento, data = d, vertical = TRUE,
           method = "stack", pch = 19, col = palette_geo[1:2],
           xlab = "Affioramento simulato", ylab = "Densità (g/cm^3)",
           main = "Punti individuali: 12 provini per affioramento")
points(1:2, medie$densita_g_cm3, pch = 18, cex = 1.6)


# Analisi principale: Salvare un risultato che un altro studente possa leggere
salva_tabella(d, "provini_con_densita.csv", ctx$out)
salva_tabella(medie, "medie_affioramenti.csv", ctx$out)
nota <- c("Dataset simulato: 24 provini, sei stazioni, due affioramenti.",
          sprintf("Differenza descrittiva A-B: %.4f g/cm^3.", delta_AB),
          "Non è stato eseguito un test inferenziale.",
          "I provini della stessa stazione non sono repliche di nuovi affioramenti.")
salva_testo(nota, "conclusione.txt", ctx$out)
nota
