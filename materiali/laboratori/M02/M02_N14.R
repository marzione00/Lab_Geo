# Controlli geometrici e disponibilità
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
ctx <- inizia_notebook("M02_N14")
set.seed(1004)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Importazione conservativa
raw <- leggi_dati("fossili_da_controllare.csv", sep = ";",
                  colClasses = "character", na.strings = character())
raw$riga_origine <- seq_len(nrow(raw))
head(raw, 7)
stopifnot(nrow(raw) == 25L)
misure <- c("diametro_tot_um", "diametro_int_um", "diaframma_um")
richiedi_colonne(raw, c("id", "morfotipo", misure))


# Preparazione: Convertire il testo senza nascondere gli errori
converti_numero <- function(x) {
  testo <- trimws(x)
  assente <- testo %in% c("", "NA", "ND")
  censurato <- grepl("^[<>]", testo)
  if (any(censurato)) stop("Valori censurati: separarli in valore, limite e stato.")
  testo[assente] <- NA_character_
  numero <- suppressWarnings(as.numeric(gsub(",", ".", testo, fixed = TRUE)))
  fallito <- !assente & is.na(numero)
  list(valore = numero, mancante_dichiarato = assente, conversione_fallita = fallito)
}
d <- raw
registro_conversione <- list()
for (v in misure) {
  z <- converti_numero(raw[[v]])
  d[[v]] <- z$valore
  registro_conversione[[v]] <- data.frame(
    variabile = v, mancanti = sum(z$mancante_dichiarato),
    falliti = sum(z$conversione_fallita))
}
do.call(rbind, registro_conversione)


# Preparazione: Categorie e duplicati richiedono regole diverse
forma <- tolower(trimws(raw$morfotipo))
d$morfotipo <- ifelse(forma == "rounded", "Rounded",
                      ifelse(forma == "spiky", "Spiky", NA_character_))
col_originali <- setdiff(names(raw), "riga_origine")
d$duplicato_esatto <- duplicated(raw[col_originali])
d$id_ripetuto <- duplicated(d$id) | duplicated(d$id, fromLast = TRUE)
d$gruppo_sconosciuto <- is.na(d$morfotipo)
d[d$id_ripetuto, c("riga_origine", "id", "duplicato_esatto")]
table(d$morfotipo, useNA = "ifany")


# Analisi principale: Controlli geometrici e disponibilità
d$misura_mancante <- !complete.cases(d[misure])
d$non_positivo <- Reduce(`|`, lapply(d[misure], function(x) is.finite(x) & x <= 0))
d$interno_superiore <- with(d, is.finite(diametro_int_um) &
                            is.finite(diametro_tot_um) &
                            diametro_int_um > diametro_tot_um)
# Se un confronto produce NA, non è classificato come geometria valida:
# il flag misura_mancante ne conserva già la ragione.
d$interno_superiore[is.na(d$interno_superiore)] <- FALSE
d$utilizzabile <- !(d$misura_mancante | d$non_positivo |
                    d$interno_superiore | d$duplicato_esatto | d$gruppo_sconosciuto)
stopifnot(!anyNA(d$utilizzabile))
d[!d$utilizzabile, c("id", "misura_mancante", "non_positivo",
                      "interno_superiore", "duplicato_esatto")]
table(d$utilizzabile)
