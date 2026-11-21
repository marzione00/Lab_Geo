errore <- f
errore$diametro_int_um[2] <- errore$diametro_tot_um[2]+1
fuori <- errore$diametro_int_um>errore$diametro_tot_um
errore[fuori,c("id","diametro_tot_um","diametro_int_um")]
stopifnot(sum(fuori)==1L,nrow(carica_dati("fossili_simulati.csv"))==160L)
