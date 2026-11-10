# Funzioni di servizio: file, controlli e output. Nessun modello è nascosto qui.
# Il codice statistico rimane visibile nei notebook.
radice_progetto <- function(inizio = getwd()) {
  p <- normalizePath(inizio, winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(genitore, p)) stop("Aprire Notebook_R_Geologia.Rproj prima di eseguire il notebook.")
    p <- genitore
  }
}
inizia_notebook <- function(codice) {
  root <- radice_progetto()
  out <- file.path(root, "risultati", "R", codice)
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  list(root = root, out = out)
}
leggi_dati <- function(nome, ...) {
  p <- file.path(radice_progetto(), "dati", nome)
  if (!file.exists(p)) stop("Dataset non trovato: ", nome)
  read.csv(p, stringsAsFactors = FALSE, fileEncoding = "UTF-8", ...)
}
richiedi_colonne <- function(dati, colonne) {
  assenti <- setdiff(colonne, names(dati))
  if (length(assenti)) stop("Colonne assenti: ", paste(assenti, collapse = ", "))
  invisible(TRUE)
}
salva_tabella <- function(dati, nome, cartella) {
  if (!is.data.frame(dati)) dati <- as.data.frame(dati)
  if (basename(nome) != nome) stop("Usare un nome semplice, senza cartelle.")
  write.csv(dati, file.path(cartella, nome), row.names = FALSE, na = "", fileEncoding = "UTF-8")
  invisible(file.path(cartella, nome))
}
salva_testo <- function(testo, nome, cartella) {
  writeLines(enc2utf8(testo), file.path(cartella, nome), useBytes = TRUE)
  invisible(file.path(cartella, nome))
}
# Palette del corso. È un supporto visivo, non una codifica della qualità del dato.
palette_geo <- c("#087C74", "#5146A5", "#9B4564", "#A05B10", "#326A9A", "#666666")
stile_grafico <- function() {
  par(mar = c(4.8, 4.8, 3.4, 1.2), las = 1,
      col.axis = "#253344", col.lab = "#253344", col.main = "#253344")
}
# Non termina la sessione e non cancella alcun oggetto.
registra_sessione <- function(cartella) {
  salva_testo(capture.output(sessionInfo()), "sessionInfo.txt", cartella)
  message("File salvati in: ", cartella)
}
