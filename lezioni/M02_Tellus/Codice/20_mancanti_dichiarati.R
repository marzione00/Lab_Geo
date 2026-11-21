# Riconoscere il codice nella colonna
raw <- fossili_raw$diametro_tot_um
t <- trimws(raw)
assente <- t %in% c("", "NA", "ND")
sum(assente)      # Un esterno assente
fossili_raw$id[assente]

# Lo zero e' un valore numerico
is.na(0)           # FALSE
