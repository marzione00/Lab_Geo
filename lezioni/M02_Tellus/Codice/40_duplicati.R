cc <- setdiff(names(fossili_raw),
              "riga_origine")
esatti <- duplicated(fossili_raw[cc])
ids <- fossili_raw$id # Chiave
ripetuti <- duplicated(ids) |
  duplicated(ids, fromLast = TRUE)
c(esatti = sum(esatti),
  righe_id = sum(ripetuti))
