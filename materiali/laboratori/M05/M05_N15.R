# N15 — Contrasti indipendenti e coppie
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(list(indipendenti=c(stima=V$delta,q95(b_delta)),appaiati=c(stima=mean(diff_coppie),SE=sd(b_paired))))
