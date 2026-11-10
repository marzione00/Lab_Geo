# N04 — Standardizzazione e dipendenza
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(var_matrice=sum(Sigma)/24^2,var_formula=(1+3*.6)/24,DEFF=V$deff,n_eff=V$neff))
