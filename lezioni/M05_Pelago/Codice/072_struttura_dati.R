# Dati sintetici letti da setup.R
table(fossili$morfotipo)
table(provini$stazione)
# Una riga del fossile contiene
# due misure della stessa unita.
head(fossili[c("id",
  "diametro_tot_um", "diametro_int_um")])
