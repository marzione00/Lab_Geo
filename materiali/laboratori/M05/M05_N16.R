# N16 — Provini e medie di stazione
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(stima=V$media_st,SE_righe=sd(b_righe),SE_stazioni=sd(b_stazioni),q95(b_stazioni)))
