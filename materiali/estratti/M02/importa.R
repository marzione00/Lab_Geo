raw <- read.csv(
 'dati/fossili_da_controllare.csv',
 sep=';',colClasses='character',
 na.strings=character())
raw$riga_origine <- seq_len(nrow(raw))
stopifnot(nrow(raw)==25L)
head(raw)
