# Aggiungiamo un errore intenzionale
testi <- c("6,4", "errore",
           "ND", "Inf")
z <- converti_misura(testi)
data.frame(testo = testi,
           valore = z$valore,
           stato = z$stato)
