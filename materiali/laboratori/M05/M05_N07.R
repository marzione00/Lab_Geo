# N07 — Copertura della procedura
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(inclusioni=sum(copre),K=length(copre),copertura=mean(copre),SE_MC=V$coverage_mcse))
