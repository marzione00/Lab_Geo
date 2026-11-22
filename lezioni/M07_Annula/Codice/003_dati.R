# Avvio dalla cartella Annula_M07.
source("setup.R", encoding = "UTF-8")
# Una riga corrisponde a un fossile.
head(f[, c("id", "diametro_tot_um",
           "diametro_int_um")])
stopifnot(!anyDuplicated(f$id))
