# Tellus — dati per la lezione di R e gestione dei dati.
# Eseguire dalla cartella che contiene Tellus_M02.Rproj e Dati/.
# I CSV originali sono letti; nessun file di dati viene modificato.

leggi_csv <- function(nome, ...) {
  percorso <- file.path("Dati", nome)
  if (!file.exists(percorso)) {
    stop("File assente: ", percorso,
         ". Aprire Tellus_M02.Rproj oppure controllare getwd().")
  }
  read.csv(percorso, stringsAsFactors = FALSE,
           fileEncoding = "UTF-8", ...)
}

# Conserva separatamente numero, stato e limite di un valore censurato.
# Accetta punto o virgola decimale; non interpreta separatori delle migliaia.
# Il testo originale resta in fossili_raw.
converti_misura <- function(x) {
  testo <- trimws(as.character(x))
  assente <- is.na(testo) | testo %in% c("", "NA", "ND")
  cens <- !assente & grepl("^[<>]", testo)
  non_finito <- !assente & testo %in% c("Inf", "+Inf", "-Inf", "NaN")
  numerico <- gsub(",", ".", testo, fixed = TRUE)
  grammatica <- "^[+-]?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)([eE][+-]?[0-9]+)?$"
  formato_ok <- !assente & !cens & !non_finito &
    grepl(grammatica, numerico)
  valore <- rep(NA_real_, length(x))
  valore[formato_ok] <- as.numeric(numerico[formato_ok])
  non_finito <- non_finito | (formato_ok & !is.finite(valore))
  stato <- rep("formato_errato", length(x))
  stato[formato_ok] <- "numerico"
  stato[assente] <- "mancante"
  stato[cens] <- "censurato"
  stato[non_finito] <- "non_finito"
  valore[non_finito] <- NA_real_
  limite <- rep(NA_real_, length(x))
  operatore <- rep(NA_character_, length(x))
  if (any(cens)) {
    op <- sub("^([<>]=?).*$", "\\1", testo[cens])
    soglia <- trimws(sub("^[<>]=?", "", testo[cens]))
    soglia <- gsub(",", ".", soglia, fixed = TRUE)
    limite_ok <- grepl(grammatica, soglia)
    valori_limite <- rep(NA_real_, length(soglia))
    valori_limite[limite_ok] <- as.numeric(soglia[limite_ok])
    limite[cens] <- valori_limite
    operatore[cens] <- op
    stato[cens & !is.finite(limite)] <- "formato_errato"
  }
  list(valore = valore, stato = stato, limite = limite,
       operatore = operatore)
}

# Preparazione dichiarata per gli esempi successivi alla sezione importazione.
# Restituisce tutte le righe e aggiunge segnalazioni; nessuna esclusione implicita.
prepara_fossili <- function(raw) {
  misure <- c("diametro_tot_um", "diametro_int_um", "diaframma_um")
  richieste <- c("id", "morfotipo", misure)
  stopifnot(all(richieste %in% names(raw)))
  d <- raw
  for (v in misure) {
    z <- converti_misura(raw[[v]])
    d[[v]] <- z$valore
    d[[paste0(v, "_stato")]] <- z$stato
    d[[paste0(v, "_limite")]] <- z$limite
    d[[paste0(v, "_operatore")]] <- z$operatore
  }
  forma <- tolower(trimws(raw$morfotipo))
  d$morfotipo <- ifelse(forma == "rounded", "Rounded",
                       ifelse(forma == "spiky", "Spiky", NA_character_))
  col_originali <- setdiff(names(raw), "riga_origine")
  d$duplicato_esatto <- duplicated(raw[col_originali])
  d$id_ripetuto <- duplicated(raw$id) | duplicated(raw$id, fromLast = TRUE)
  d$gruppo_sconosciuto <- is.na(d$morfotipo)
  stati <- d[paste0(misure, "_stato")]
  d$misura_mancante <- !complete.cases(d[misure])
  d$conversione_fallita <- rowSums(stati == "formato_errato") > 0
  d$censurato <- rowSums(stati == "censurato") > 0
  d$non_finito <- rowSums(stati == "non_finito") > 0
  d$non_positivo <- Reduce(`|`, lapply(d[misure],
    function(x) is.finite(x) & x <= 0))
  d$interno_superiore <- with(d,
    is.finite(diametro_int_um) & is.finite(diametro_tot_um) &
    diametro_int_um > diametro_tot_um)
  d$utilizzabile <- !(d$misura_mancante | d$conversione_fallita |
    d$censurato | d$non_finito | d$non_positivo | d$interno_superiore |
    d$duplicato_esatto | d$gruppo_sconosciuto)
  # Per lo spessore radiale basta la coppia di diametri. Un diametro interno
  # nullo è compatibile con il modello geometrico; l'esterno deve essere > 0.
  d$usabile_geometria <- with(d,
    is.finite(diametro_tot_um) & is.finite(diametro_int_um) &
    diametro_tot_um > 0 & diametro_int_um >= 0 &
    diametro_int_um <= diametro_tot_um &
    !duplicato_esatto & !gruppo_sconosciuto)
  stopifnot(!anyNA(d$utilizzabile), !anyNA(d$usabile_geometria))
  d
}

campioni <- leggi_csv("campioni_modulo1.csv")
fossili_raw <- leggi_csv("fossili_da_controllare.csv", sep = ";",
                        colClasses = "character", na.strings = character())
fossili_raw$riga_origine <- seq_len(nrow(fossili_raw))
fossili <- prepara_fossili(fossili_raw)
microsonda <- leggi_csv("microsonda_simulata.csv")
censura <- leggi_csv("censura_esempio.csv", na.strings = c("", "NA"))
fossili_simulati <- leggi_csv("fossili_simulati.csv")
stopifnot(nrow(campioni) == 24L, nrow(fossili_raw) == 25L,
          nrow(microsonda) == 75L, nrow(censura) == 4L,
          nrow(fossili_simulati) == 160L)
message("Dati pronti: campioni 24; fossili 25; microsonda 75; censura 4.")
