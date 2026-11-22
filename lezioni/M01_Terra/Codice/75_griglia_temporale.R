# Una misura al giorno, senza salti.
date <- demo$data
passi <- as.integer(diff(date))
table(passi)
attese <- seq(min(date), max(date),
              by = "day")
setdiff(attese, date) # giorni assenti
stopifnot(all(passi == 1))
