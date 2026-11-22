# Anagrafica incompleta di esempio
siti3 <- siti[siti$sito == "A", ]
setdiff(provini$sito, siti3$sito)
# Il provino B resta nel risultato
j3 <- merge(provini, siti3,
  by = "sito", all.x = TRUE)
j3
