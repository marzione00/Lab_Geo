# N01 — Parametro, campione e statistica
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(parametro=parametro,n=length(campione),stima=stima))
