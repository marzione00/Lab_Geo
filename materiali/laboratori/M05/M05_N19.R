# N19 — Reinserimento e bootstrap enumerato
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(numero=length(medie_esatte),media=mean(medie_esatte),varianza=V$toy_var,formula=3*var(piccolo)/16))
