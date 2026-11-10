# N18 — Precisione Monte Carlo e registrazione
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(aggregate(cbind(se,basso,alto)~B,mc,sd))
