# Un’alternativa tidyverse, non un secondo corso
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
ctx <- inizia_notebook("M02_N09")
set.seed(1003)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Una tabella ben importata non è scontata
percorso <- file.path(ctx$root, "dati", "fossili_da_controllare.csv")
readLines(percorso, n = 4, encoding = "UTF-8")
# Forziamo testo per non perdere ND, spazi e virgole decimali.
grezzi <- read.csv(percorso, sep = ";", colClasses = "character",
                   na.strings = character(), stringsAsFactors = FALSE,
                   fileEncoding = "UTF-8")
str(grezzi)
head(grezzi, 4)


# Preparazione: Vettori: tipi e operazioni
numeri <- c(4, 5, 6)
misto <- c(4, "5", "ND")
class(numeri)
class(misto)
valori <- c(4, NA, 6)
is.na(valori)
mean(valori)                # NA: il mancante non viene ignorato per default.
mean(valori, na.rm = TRUE)  # Cambia il denominatore: ora usa due valori.
sum(!is.na(valori))


# Preparazione: Scegliere righe e colonne in modo esplicito
d <- leggi_dati("campioni_modulo1.csv")
d$densita <- d$massa_g / d$volume_cm3
scelti <- d[d$affioramento == "A" & d$alterazione %in% c("bassa", "media"), ]
nrow(scelti)
scelti[c("id", "stazione", "alterazione", "densita")]
# Un ordinamento agisce sulla tabella intera.
ordinati <- d[order(d$densita, decreasing = TRUE), ]
head(ordinati, 5)
stopifnot(setequal(ordinati$id, d$id))


# Preparazione: Raggruppare: cambia l’unità della tabella
medie <- aggregate(densita ~ stazione, d, mean)
conteggi <- aggregate(id ~ stazione, d, length)
names(conteggi)[2] <- "n_provini"
riassunto <- merge(medie, conteggi, by = "stazione", all.x = TRUE, sort = FALSE)
riassunto
stopifnot(nrow(riassunto) == length(unique(d$stazione)))
stopifnot(sum(riassunto$n_provini) == nrow(d))


# Preparazione: Join molti-a-uno con controllo delle chiavi
stazioni <- unique(d[c("stazione", "affioramento")])
stopifnot(anyDuplicated(stazioni$stazione) == 0L)
# Colleghiamo la media della stazione a ogni provino.
d$ordine_originale <- seq_len(nrow(d))
medie_st <- aggregate(densita ~ stazione, d, mean)
names(medie_st)[2] <- "media_stazione"
uniti <- merge(d, medie_st, by = "stazione", all.x = TRUE, sort = FALSE)
uniti <- uniti[order(uniti$ordine_originale), ]
stopifnot(nrow(uniti) == nrow(d), identical(uniti$id, d$id))
head(uniti[c("id", "stazione", "densita", "media_stazione")])


# Preparazione: Un esempio di tabella lunga
lunga <- reshape(d[c("id", "massa_g", "volume_cm3")],
                  varying = c("massa_g", "volume_cm3"),
                  v.names = "valore", timevar = "variabile",
                  times = c("massa_g", "volume_cm3"),
                  idvar = "id", direction = "long")
rownames(lunga) <- NULL
head(lunga)
table(lunga$variabile)
stopifnot(nrow(lunga) == 2L * nrow(d))


# Preparazione: Una funzione con un contratto chiaro
densita_controllata <- function(massa, volume) {
  if (!is.numeric(massa) || !is.numeric(volume)) {
    stop("Massa e volume devono essere numerici.")
  }
  if (length(massa) != length(volume)) stop("Le lunghezze devono coincidere.")
  if (any(!is.finite(massa)) || any(!is.finite(volume)) ||
      any(massa <= 0) || any(volume <= 0)) {
    stop("Sono ammesse soltanto misure finite e positive.")
  }
  massa / volume
}
rho <- densita_controllata(d$massa_g, d$volume_cm3)
stopifnot(isTRUE(all.equal(rho, d$densita)))
# Mostriamo un errore intenzionale senza interrompere il notebook.
tryCatch(densita_controllata(c(10, 20), c(2, 0)),
         error = function(e) message("Errore atteso: ", conditionMessage(e)))


# Preparazione: Applicare una sintesi a più variabili
sintesi <- function(x) {
  disponibili <- is.finite(x)
  if (!any(disponibili)) return(c(n = length(x), validi = 0, media = NA, sd = NA))
  c(n = length(x), validi = sum(disponibili),
    media = mean(x[disponibili]), sd = sd(x[disponibili]))
}
colonne <- c("massa_g", "volume_cm3", "densita")
lista <- lapply(d[colonne], sintesi)
tabella <- as.data.frame(do.call(rbind, lista))
tabella$variabile <- rownames(tabella)
rownames(tabella) <- NULL
tabella


# Analisi principale: Un’alternativa tidyverse, non un secondo corso
if (requireNamespace("dplyr", quietly = TRUE)) {
  gruppi <- dplyr::group_by(d, affioramento)
  tab_dplyr <- dplyr::summarise(gruppi,
                               n = dplyr::n(),
                               media_densita = mean(densita),
                               .groups = "drop")
  print(tab_dplyr)
} else {
  message("Approfondimento non eseguito: dplyr non installato. Il percorso base è completo.")
}
