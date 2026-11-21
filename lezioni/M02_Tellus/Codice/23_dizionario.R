# Controlliamo i nomi attesi
richieste <- c("id", "morfotipo",
 "diametro_tot_um", "diametro_int_um",
 "diaframma_um", "riga_origine")
stopifnot(all(richieste %in%
              names(fossili_raw)))
vapply(fossili_raw, is.character,
       logical(1))
