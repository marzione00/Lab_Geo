# Dataset caricato da setup.R
table(censura$stato)
sel_c <- censura$stato == "censurato"
censura[sel_c, c("testo_originale",
  "valore_osservato", "limite")]
stopifnot(all(is.na(
  censura$valore_osservato[sel_c])))
