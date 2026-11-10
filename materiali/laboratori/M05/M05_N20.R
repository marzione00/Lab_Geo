# N20 — Mediana e confronto fra statistiche
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(mediana=median(x),SE=sd(b_mediana),q95(b_mediana)))
