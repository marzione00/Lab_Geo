# Esiti della preparazione documentata
v <- "diametro_tot_um_stato"
table(fossili[[v]], useNA = "ifany")
bad <- fossili$conversione_fallita
sum(bad)            # Zero nel CSV

# Nessuna riga eliminata dal setup
stopifnot(nrow(fossili) ==
          nrow(fossili_raw))
