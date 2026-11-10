# N03 — Distribuzione delle medie
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(rbind(n5=c(media=mean(medie5),sd=sd(medie5)),n40=c(media=mean(medie40),sd=sd(medie40))))
