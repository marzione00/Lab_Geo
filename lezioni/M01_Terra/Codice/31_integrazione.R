misure <- data.frame(
  id = c("A", "B"), x = c(3.1, 7))
meta <- data.frame(
  id = c("A", "B"), quota = c(120, 280))
# Una sola riga per chiave in meta
stopifnot(!anyDuplicated(meta$id))
uniti <- merge(misure, meta,
  by = "id", all.x = TRUE)
