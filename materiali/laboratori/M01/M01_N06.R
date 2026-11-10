# Dai tipi informatici al significato
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
ctx <- inizia_notebook("M01_N06")
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


# Analisi principale: Dai tipi informatici al significato
d$affioramento <- factor(d$affioramento, levels = c("A", "B"))
d$alterazione <- factor(d$alterazione,
                        levels = c("bassa", "media", "alta"),
                        ordered = TRUE)
levels(d$alterazione)
table(d$alterazione)
# Gli ID devono essere presenti e univoci.
stopifnot(!anyNA(d$id), anyDuplicated(d$id) == 0L)
