# N12 — Bootstrap della media di un gruppo
# Eseguire dalla radice del progetto.
# I calcoli condivisi sono ricostruiti in una sessione locale.
source("R/M05/calcoli.R",local=TRUE)
# Risultati da discutere nel fascicolo dei laboratori.
print(c(media_originale=mean(x),media_boot=mean(b_R),SE=sd(b_R),SE_esatto=V$boot_R_se_esatto,q95(b_R)))
