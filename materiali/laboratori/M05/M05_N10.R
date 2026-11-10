# N10 — Distribuzione empirica e informazione
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(n=length(x),supporto_distinto=length(unique(x)),distinti_attesi=V$unici_attesi))
