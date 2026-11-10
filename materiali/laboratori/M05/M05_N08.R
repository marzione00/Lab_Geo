# N08 — Precisione, selezione e popolazione finita
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(var_enumerazione=var_design,var_formula=var_fpc,numero_campioni=ncol(combinazioni)))
