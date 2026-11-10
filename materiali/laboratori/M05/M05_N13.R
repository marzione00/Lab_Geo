# N13 — Pooled e quote casuali
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(media_nS=mean(b_pool["quota",]),SD_nS=sd(b_pool["quota",]),SE=sd(b_pool["media",]),q95(b_pool["media",])))
