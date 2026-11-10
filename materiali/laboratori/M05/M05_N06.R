# N06 — Intervallo di Student
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(list(quantile=critico,IC=ic_t,IC_R=unname(t.test(x)$conf.int),predittivo=ip_t))
