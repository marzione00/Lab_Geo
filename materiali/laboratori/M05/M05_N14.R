# N14 — Bootstrap stratificato
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(rbind(pooled=c(SE=sd(b_pool["media",]),q95(b_pool["media",])),stratificato=c(SE=sd(b_strat),q95(b_strat))))
