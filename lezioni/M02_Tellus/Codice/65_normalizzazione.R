stopifnot(all(is.finite(totale)),
          all(totale > 0))
normalizzati <- 100 * sweep(
  microsonda[ossidi], 1, totale, "/")
# Ora la somma e imposta a 100
range(rowSums(normalizzati))
# Il totale originale resta distinto
head(data.frame(totale, qc_totale))
