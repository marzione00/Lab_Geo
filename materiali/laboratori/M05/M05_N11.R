# N11 — Una replica osservata negli indici
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(distinti=length(unique(indici)),media_indici=mean(replica),media_pesi=sum(frequenze*x)/n))
