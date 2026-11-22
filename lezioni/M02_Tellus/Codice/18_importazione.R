# Conserviamo tutte le scritture
fossili_raw <- read.csv(
 "Dati/fossili_da_controllare.csv",
 sep = ";", colClasses = "character",
 na.strings = character())
fossili_raw$riga_origine <-
 seq_len(nrow(fossili_raw))
head(fossili_raw, 3)
